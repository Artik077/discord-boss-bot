import easyocr
reader = easyocr.Reader(['en'])

import discord
from discord.ext import commands, tasks
import datetime
import pytz
from boss_data import get_boss_statuses, register_kill, reset_all_bosses
from config import TOKEN, PREFIX

from PIL import Image
import io
import numpy as np
import cv2
import os
import difflib
import re

os.makedirs("temp", exist_ok=True)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

channel_id = 1401743260036104192  # ← replace with your channel ID
status_message_ids = []

MAX_MESSAGE_LENGTH = 2000

def split_message(text, max_length=MAX_MESSAGE_LENGTH):
    lines = text.split('\n')
    chunks = []
    current_chunk = ""

    for line in lines:
        if len(current_chunk) + len(line) + 1 > max_length:
            chunks.append(current_chunk)
            current_chunk = line
        else:
            current_chunk += ("\n" + line) if current_chunk else line
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def preprocess_image_for_ocr(np_image):
    gray = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
    processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, 11, 2)
    processed = cv2.medianBlur(processed, 3)
    return processed

KNOWN_BOSSES = [
    "Shila", "Moof", "Ukanba", "Normus", "Talakin", "Cabrio", "PanNarod", "Hisilrome", "Felis", "Valefar", "Flynt",
    "Repiro", "Stonegeist", "Timitris", "Matura", "Medusa", "Contaminated Cruma", "Katan", "Chertuba", "Enkura",
    "Talkin", "Timiniel", "Breka", "Queen Ant", "Behemoth", "Basila", "Mutated Cruma", "Black Lily", "Sarka", "Landor",
    "Gahareth", "Andras", "Samuel", "Core Susceptor", "Tromba", "Glaki", "Balbo", "Selu", "Pan Dra'eed", "Savan",
    "Coroon", "Dragon Beast", "Kelsus", "Mirror of Oblivion", "Orfen", "Haff", "Cyrax", "Modeus", "Naiad", "Valak",
    "Olkuth", "Rahha", "Phoenix", "Thanatos"
]

def extract_boss_times_from_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    open_cv_image = np.array(image)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

    processed_image = preprocess_image_for_ocr(open_cv_image)
    results = reader.readtext(processed_image, detail=0)

    text = "\n".join(results)
    print("===== EasyOCR RAW TEXT =====")
    print(text)
    print("============================")

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    boss_entries = []
    pattern = re.compile(r'(\d{4}/\d{2}/\d{2})[\s,]?(\d{2})[:.]?(\d{2})')

    i = 0
    while i < len(lines):
        line = lines[i]

        possible_name = line.split()[0]
        match = difflib.get_close_matches(possible_name, KNOWN_BOSSES, n=1, cutoff=0.6)

        if match:
            boss_name = match[0]
            time_found = False

            for j in range(i + 1, min(i + 4, len(lines))):
                time_line = lines[j]
                time_match = pattern.search(time_line)

                if time_match:
                    date, hh, mm = time_match.groups()
                    boss_entries.append((boss_name, f"{hh}{mm}"))  # no colon in time_str for register_kill
                    time_found = True
                    break

            if not time_found:
                print(f"⚠️ No time found for {boss_name}")

            i += 1
        else:
            i += 1

    return boss_entries

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    update_status.start()

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if not message.content.startswith('!') and len(message.attachments) == 0:
        parts = message.content.lower().split()
        if not parts:
            return

        query = parts[0]
        normalized_query = query.replace("'", "").replace(" ", "")
        matches = [boss for boss in KNOWN_BOSSES if boss.lower().replace(" ", "").replace("'", "").startswith(normalized_query)]
        
        if not matches:
            await message.add_reaction("💩")
            return

        boss_name = matches[0]

        if len(parts) >= 2 and re.match(r'^\d{4}$', parts[1]):
            time_str = parts[1]
        else:
            now = datetime.datetime.now(pytz.timezone("Europe/Kyiv"))
            time_str = now.strftime("%H%M")

        register_kill(boss_name, time_str)
        await message.add_reaction("🫡")
        await message.channel.send(f"✅ {boss_name} recorded at {time_str[:2]}:{time_str[2:]}")
        await update_status_func()
        return

    if len(message.attachments) == 2:
        # Your existing 2 attachments handling code
        ...

    if message.attachments:
        recognized_any = False
        for attachment in message.attachments:
            if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_bytes = await attachment.read()
                boss_list = extract_boss_times_from_image(img_bytes)
                if boss_list:
                    recognized_any = True
                    reply_lines = []
                    for boss_name, time_str in boss_list:
                        register_kill(boss_name, time_str)
                        reply_lines.append(f"✅ {boss_name} recorded at {time_str[:2]}:{time_str[2:]}")
                    msg = await message.channel.send("\n".join(reply_lines))
                    await msg.add_reaction("🫡")
                else:
                    await message.add_reaction("💩")
                    await message.channel.send("❌ No valid boss times found in the image.")

        if recognized_any:
            await update_status_func()
            return

    content = message.content.strip()
    parts = content.split()

    if len(parts) == 1:
        boss_name = parts[0]
        now = datetime.datetime.now(pytz.timezone("Europe/Kyiv"))
        register_kill(boss_name, now.strftime("%H%M"))
        await message.add_reaction("🫡")
        await message.channel.send(f"✅ {boss_name} recorded as killed at {now.strftime('%H:%M')} (Kyiv time)")
        await update_status_func()

    elif len(parts) == 2 and parts[1].isdigit() and len(parts[1]) == 4:
        boss_name, time_str = parts
        register_kill(boss_name, time_str)
        await message.add_reaction("🫡")
        await message.channel.send(f"✅ {boss_name} recorded as killed at {time_str[:2]}:{time_str[2:]} (manual)")
        await update_status_func()

    elif content.lower().startswith("reset"):
        if len(parts) == 2 and parts[1].isdigit() and len(parts[1]) == 4:
            time_str = parts[1]
            reset_all_bosses(time_str)
            await message.add_reaction("🫡")
            await message.channel.send(f"🔄 All bosses reset to {time_str[:2]}:{time_str[2:]}")
            await update_status_func()

    await bot.process_commands(message)

@tasks.loop(minutes=1)
async def update_status():
    await update_status_func()

async def update_status_func():
    global status_message_ids
    channel = bot.get_channel(channel_id)

    if not channel:
        print("❌ Channel not found. Check channel_id.")
        return

    statuses = get_boss_statuses()
    header = "**📅🗡️ Boss Respawn Timer (Local time)**"
    
    cleaned_statuses = [line.replace("⏳", "") for line in statuses]

    content = "\n".join([header] + cleaned_statuses)
    message_chunks = split_message(content)

    for msg_id in status_message_ids:
        try:
            msg = await channel.fetch_message(msg_id)
            await msg.delete()
        except Exception as e:
            print(f"⚠️ Could not delete message {msg_id}: {e}")

    status_message_ids = []
    for chunk in message_chunks:
        try:
            msg = await channel.send(chunk)
            status_message_ids.append(msg.id)
        except Exception as e:
            print(f"❌ Failed to send status: {e}")

