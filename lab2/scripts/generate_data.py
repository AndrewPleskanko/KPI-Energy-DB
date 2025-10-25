import uuid, random, datetime, time
import math
from cassandra.cluster import Cluster
from cassandra.query import PreparedStatement
from collections import defaultdict

# Параметри генерації
N_STATIONS = 50
MINUTES_INTERVAL = 15
DAYS = 2  # можна змінити
REGIONS = ["Kyiv-North", "Kyiv-South", "Kyiv-East", "Kyiv-West"]

# Підключення
cluster = Cluster(["cassandra"])
session = cluster.connect()
session.set_keyspace("solar_kv")

# Підготувати заяви
ins_readings = session.prepare("""
                               INSERT INTO readings_by_station (station_id, ts, power_kw, voltage, current, panel_temp, region)
                               VALUES (?, ?, ?, ?, ?, ?, ?)
                               """)
ins_weather = session.prepare("""
                              INSERT INTO weather_by_station (station_id, ts, solar_radiation, air_temp, cloudiness)
                              VALUES (?, ?, ?, ?, ?)
                              """)
ins_daily = session.prepare("""
                            INSERT INTO daily_generation_by_station (station_id, day, energy_kwh, max_power_kw, min_power_kw)
                            VALUES (?, ?, ?, ?, ?)
                            """)
ins_analytics = session.prepare("""
                                INSERT INTO analytics_by_region_date (region, date, station_id, total_energy_kwh, avg_power_kw)
                                VALUES (?, ?, ?, ?, ?)
                                """)

# Створюємо список станцій з регіоном
stations = []
for i in range(N_STATIONS):
    st = {"id": uuid.uuid4(), "region": random.choice(REGIONS)}
    stations.append(st)

print(f"Generated {len(stations)} stations.")

# Генеруємо миттєві виміри
start_dt = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=DAYS)
end_dt = datetime.datetime.now(datetime.timezone.utc)
current_dt = start_dt

# Збираємо добові підсумки локально, потім запишемо
daily_acc = defaultdict(lambda: {"energy": 0.0, "max_p": 0.0, "min_p": float("inf")})

ts = start_dt
while ts <= end_dt:
    for st in stations:
        # згенеруємо потужність в кВт (імітую добовий цикл)
        hour = ts.hour + ts.minute / 60.0
        # простий синусоїдальний профіль (більше вде��ь)
        solar_factor = max(0.0, ((1.0 + math.sin((hour - 6) / 24 * 2 * math.pi)) / 2.0))
        base_power = random.uniform(10, 100)  # макс потужність установки kW
        power_kw = round(base_power * solar_factor * random.uniform(0.85, 1.05), 3)
        voltage = round(random.uniform(600, 800), 2)  # в вольт для прикладу
        current = round((power_kw * 1000) / voltage if voltage > 0 else 0, 3)
        panel_temp = round(random.uniform(15, 45), 2)

        # запишемо readings
        session.execute(ins_readings, (st["id"], ts, power_kw, voltage, current, panel_temp, st["region"]))

        # згенеруємо метео
        solar_rad = round(max(0.0, 1000 * solar_factor * random.uniform(0.7, 1.1)), 2)
        air_temp = round(random.uniform(5, 30), 2)
        cloudiness = random.randint(0, 100)
        session.execute(ins_weather, (st["id"], ts, solar_rad, air_temp, cloudiness))

        # акумуляція для доби
        day = ts.date()
        energy_kwh = power_kw * (MINUTES_INTERVAL / 60.0)  # енергія за інтервал
        key = (st["id"], day)
        daily_acc[key]["energy"] += energy_kwh
        daily_acc[key]["max_p"] = max(daily_acc[key]["max_p"], power_kw)
        daily_acc[key]["min_p"] = min(daily_acc[key]["min_p"], power_kw)

    ts = ts + datetime.timedelta(minutes=MINUTES_INTERVAL)

# Запис добових підсумків і аналітики по регіонах
for (st_id, day), vals in daily_acc.items():
    energy = round(vals["energy"], 3)
    max_p = round(vals["max_p"], 3)
    min_p = round(vals["min_p"], 3 if vals["min_p"] != float("inf") else 0.0)
    session.execute(ins_daily, (st_id, day, energy, max_p, min_p))

    # дізнаємось регіон станції - простий SELECT (можна кешувати)
    # SELECT region from readings_by_station where station_id = st_id LIMIT 1
    r = session.execute("SELECT region FROM readings_by_station WHERE station_id=%s LIMIT 1", (st_id,)).one()
    region = r.region if r and r.region else "Unknown"
    avg_power = round(energy / 24.0 if 24.0 > 0 else 0.0, 3)
    session.execute(ins_analytics, (region, day, st_id, energy, avg_power))

print("Data generation completed.")
