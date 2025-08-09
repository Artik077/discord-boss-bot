from datetime import timedelta
import datetime
import pytz

# Updated boss data with missed_cycles
BOSSES = {
    "Shila": {"respawn": timedelta(hours=12), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Moof": {"respawn": timedelta(hours=12), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Ukanba": {"respawn": timedelta(hours=18), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Normus": {"respawn": timedelta(hours=18), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Talakin": {"respawn": timedelta(hours=7), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Cabrio": {"respawn": timedelta(hours=12), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Pan Narod": {"respawn": timedelta(hours=3), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Hisilrome": {"respawn": timedelta(hours=6), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Felis": {"respawn": timedelta(hours=2), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Valefar": {"respawn": timedelta(hours=3, minutes=30), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Flynt": {"respawn": timedelta(hours=8), "chance": 33, "last_killed": None, "missed_cycles": 0},
    "Repiro": {"respawn": timedelta(hours=5), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Stonegeist": {"respawn": timedelta(hours=4), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Timitris": {"respawn": timedelta(hours=5), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Matura": {"respawn": timedelta(hours=4), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Medusa": {"respawn": timedelta(hours=7), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Contaminated Cruma": {"respawn": timedelta(hours=8), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Katan": {"respawn": timedelta(hours=8), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Chertuba": {"respawn": timedelta(hours=3), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Enkura": {"respawn": timedelta(hours=3, minutes=30), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Talkin": {"respawn": timedelta(hours=5), "chance": 33, "last_killed": None, "missed_cycles": 0},
    "Timiniel": {"respawn": timedelta(hours=8), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Breka": {"respawn": timedelta(hours=4), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Queen Ant": {"respawn": timedelta(hours=6), "chance": 33, "last_killed": None, "missed_cycles": 0},
    "Behemoth": {"respawn": timedelta(hours=6), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Basila": {"respawn": timedelta(hours=2, minutes=30), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Mutated Cruma": {"respawn": timedelta(hours=8), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Black Lily": {"respawn": timedelta(hours=12), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Sarka": {"respawn": timedelta(hours=7), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Landor": {"respawn": timedelta(hours=8), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Gahareth": {"respawn": timedelta(hours=6), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Andras": {"respawn": timedelta(hours=12), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Samuel": {"respawn": timedelta(hours=12), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Core Susceptor": {"respawn": timedelta(hours=12), "chance": 33, "last_killed": None, "missed_cycles": 0},
    "Tronba": {"respawn": timedelta(hours=4, minutes=30), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Glaki": {"respawn": timedelta(hours=8), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Balbo": {"respawn": timedelta(hours=8), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Selu": {"respawn": timedelta(hours=7, minutes=30), "chance": 33, "last_killed": None, "missed_cycles": 0},
    "Pan Dra'eed": {"respawn": timedelta(hours=8), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Savan": {"respawn": timedelta(hours=12), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Coroon": {"respawn": timedelta(hours=10), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Dragon Beast": {"respawn": timedelta(hours=12), "chance": 33, "last_killed": None, "missed_cycles": 0},
    "Kelsus": {"respawn": timedelta(hours=6), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Mirror of Oblivion": {"respawn": timedelta(hours=12), "chance": 100, "last_killed": None, "missed_cycles": 0},
    "Orfen": {"respawn": timedelta(hours=24), "chance": 33, "last_killed": None, "missed_cycles": 0},
    "Haff": {"respawn": timedelta(hours=24), "chance": 33, "last_killed": None, "missed_cycles": 0},
    "Cyrax": {"respawn": timedelta(hours=24), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Modeus": {"respawn": timedelta(hours=24), "chance": 33, "last_killed": None, "missed_cycles": 0},
    "Naiad": {"respawn": timedelta(hours=12), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Valak": {"respawn": timedelta(hours=24), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Olkuth": {"respawn": timedelta(hours=24), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Rahha": {"respawn": timedelta(hours=33), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Phoenix": {"respawn": timedelta(hours=24), "chance": 50, "last_killed": None, "missed_cycles": 0},
    "Thanatos": {"respawn": timedelta(hours=24), "chance": 50, "last_killed": None, "missed_cycles": 0},
}

def get_boss_statuses():
    now = datetime.datetime.now(pytz.timezone("Europe/Kyiv"))
    bosses_with_time = []
    bosses_without_time = []

    for name, info in BOSSES.items():
        if info["last_killed"]:
            # ⏱️ Обробка пропущених циклів
            next_spawn = info["last_killed"]
            while next_spawn + info["respawn"] < now:
                next_spawn += info["respawn"]
                info["missed_cycles"] += 1
                info["last_killed"] = next_spawn  # переносимо респ

            next_spawn = info["last_killed"] + info["respawn"]
            bosses_with_time.append((name, next_spawn, info["missed_cycles"]))
        else:
            bosses_without_time.append(name)

    bosses_with_time.sort(key=lambda x: x[1], reverse=True)
    statuses = []

    for name, next_spawn, missed in bosses_with_time:
        remain = next_spawn - now
        timestamp = int(next_spawn.timestamp())
        discord_time = f"<t:{timestamp}:t>"
        minutes_total = max(int(remain.total_seconds() // 60), 0)
        hours = minutes_total // 60
        minutes = minutes_total % 60

        if missed > 0:
            status = f"❓ (x{missed})"
        else:
            status = "✅"

        statuses.append(f"`{name:<18}` | {discord_time} | ⏳ {hours:>2}h {minutes:02}m {status}")

    for name in bosses_without_time:
        statuses.append(f"`{name:<18}` | `??:??`       | ⏳ ???? min ❓")

    return statuses

def register_kill(name, kill_time):
    dt = datetime.datetime.strptime(kill_time, "%H%M")
    now = datetime.datetime.now(pytz.timezone("Europe/Kyiv"))
    kill_dt = now.replace(hour=dt.hour, minute=dt.minute, second=0, microsecond=0)
    if name in BOSSES:
        BOSSES[name]["last_killed"] = kill_dt
        BOSSES[name]["missed_cycles"] = 0  # скидаємо лічильник пропусків

def reset_all_bosses(time_str):
    dt = datetime.datetime.strptime(time_str, "%H%M")
    now = datetime.datetime.now(pytz.timezone("Europe/Kyiv"))
    reset_dt = now.replace(hour=dt.hour, minute=dt.minute, second=0, microsecond=0)
    for k in BOSSES:
        BOSSES[k]["last_killed"] = reset_dt
        BOSSES[k]["missed_cycles"] = 0