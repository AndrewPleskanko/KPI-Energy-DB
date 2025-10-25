import matplotlib.pyplot as plt
import pandas as pd
from cassandra.cluster import Cluster

cluster = Cluster(["cassandra"])
session = cluster.connect()
session.set_keyspace("solar_kv")

# Витягнемо дві станції (перші дві із daily_generation_by_station)
rows = session.execute("SELECT station_id, day, energy_kwh FROM daily_generation_by_station LIMIT 200")
df = pd.DataFrame(rows, columns=["station_id", "day", "energy_kwh"])
if df.empty:
    print("No daily data found.")
    exit(1)

# Виберемо перші два station_id
st_ids = df['station_id'].unique()[:2]
if len(st_ids) < 2:
    print("Not enough stations for comparison.")
    exit(1)

st1, st2 = st_ids[0], st_ids[1]
g1 = df[df.station_id == st1].energy_kwh
g2 = df[df.station_id == st2].energy_kwh
avg1 = g1.mean() if not g1.empty else 0
avg2 = g2.mean() if not g2.empty else 0

print(f"Станція 1 ({st1}) – {avg1:.2f} kWh, Станція 2 ({st2}) – {avg2:.2f} kWh", end=" -> ")
if avg1 > avg2:
    print("Станція 1 ефективніша")
else:
    print("Станція 2 ефективніша")

# Побудуємо графік
df_plot = df[df.station_id.isin([st1, st2])]
# перетворимо day на datetime для графіка
df_plot['day'] = pd.to_datetime(df_plot['day'].astype(str))
pivot = df_plot.pivot_table(index='day', columns='station_id', values='energy_kwh', aggfunc='sum')
pivot.plot(title="Daily energy comparison", ylabel="energy_kwh")
plt.tight_layout()
plt.savefig("comparison.png")
print("Saved comparison.png")