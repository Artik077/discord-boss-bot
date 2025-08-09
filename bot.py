import discord
from discord.ext import commands, tasks
import datetime
import pytz
from boss_data import get_boss_statuses, register_kill, reset_all_bosses
from config import PREFIX  # Токен тепер беремо з os.getenv нижче

import os
import re
import threading
from flask import Flask

# ==== Фейковий веб-сервер для Render ====
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web).start()
# ========================================

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

channel_id = 1401743260036104192  # ← заміни на свій ID каналу
status_message_ids = []

MAX_MESSAGE_LENGTH = 2000

KNOWN_BOSSES = [
    "Shila", "Moof", "Ukanba", "Normus", "Talakin", "Cabrio", "PanNarod", "Hisilrome", "Felis", "Valefar", "Flynt",
    "Repiro", "Stonegeist", "Timitris", "Matura", "Medusa", "Contaminated Cruma", "Katan", "Chertuba", "Enkura",
    "Talkin", "Timiniel", "Breka", "Queen Ant", "Behemoth", "Basila", "Mutated Cruma", "Black Lily", "Sarka", "Landor",
    "Gahareth", "Andras", "Samuel", "Core Susceptor", "Tromba", "Glaki", "Balbo", "Selu", "Pan Dra'eed", "Savan",
    "Coroon", "Dragon Beast", "Kelsus", "Mirror of Oblivion", "Orfen", "Haff", "Cyrax", "Modeus", "Naiad", "Valak",
    "Olkuth", "Rahha", "Phoenix", "Thanatos"
]

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

token = os.getenv("DISCORD_TOKEN")
bot.run(token)