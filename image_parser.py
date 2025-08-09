from PIL import Image
import pytesseract
import re

def extract_boss_kills_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)

    lines = text.split('\n')
    result = []

    for line in lines:
        match = re.match(r'(\d{2}:\d{2})\s+([A-Za-z]+)', line.strip())
        if match:
            time = match.group(1)
            name = match.group(2)
            result.append((name.lower(), time))

    return result
