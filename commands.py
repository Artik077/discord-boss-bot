
def parse_command(content):
    content = content.strip()
    if content.startswith("rest "):
        try:
            time = content[5:]
            return ("reset", {"time": time})
        except:
            return None
    else:
        parts = content.split()
        if len(parts) == 2:
            name, time = parts
            return ("kill", {"boss_name": name, "time": time})
    return None
