from kafka import KafkaProducer
import json, random, time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_solar_data(i):
    return {
        "device_id": f"SOLAR_KV_{i:03d}",
        "power_output": round(random.uniform(0.5, 25.0), 2),
        "efficiency": round(random.uniform(15.0, 22.0), 2),
        "temperature": round(random.uniform(25.0, 65.0), 1),
        "voltage": round(random.uniform(350.0, 450.0), 2),
        "current": round(random.uniform(10.0, 60.0), 2),
        "status": random.choice(["generating", "standby", "maintenance"]),
        "irradiance": round(random.uniform(100.0, 1200.0), 1),
        "cloud_factor": round(random.uniform(0.0, 1.0), 2)
    }

for i in range(1000):
    record = generate_solar_data(random.randint(1, 50))
    producer.send("solar-main", record)
    time.sleep(0.2)

producer.flush()
print("Data sent successfully!")