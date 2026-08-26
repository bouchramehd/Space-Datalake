import json
import time
import requests
from kafka import KafkaProducer

# Connection to Kafka from Windows
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

# NASA NeoWs API
NASA_URL = "https://api.nasa.gov/neo/rest/v1/feed"

params = {
    "api_key": "DEMO_KEY"
}

print("🚀 NASA NeoWs producer started")
print("📡 Sending asteroid data to Kafka topic: nasa-neows")

while True:
    try:
        response = requests.get(
            NASA_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        for date, asteroids in data["near_earth_objects"].items():

            for asteroid in asteroids:

                message = {
                    "date": date,
                    "id": asteroid["id"],
                    "name": asteroid["name"],
                    "absolute_magnitude": asteroid.get(
                        "absolute_magnitude_h"
                    ),
                    "estimated_diameter_km": asteroid[
                        "estimated_diameter"
                    ]["kilometers"]["estimated_diameter_max"],
                    "potentially_hazardous": asteroid[
                        "is_potentially_hazardous_asteroid"
                    ]
                }

                producer.send(
                    "nasa-neows",
                    value=message
                )

                print(
                    f"☄️ Sent: {message['name']} | "
                    f"Hazardous: {message['potentially_hazardous']}"
                )

        producer.flush()

        print("✅ Batch sent to Kafka. Waiting 60 seconds...")
        time.sleep(60)

    except Exception as error:
        print("❌ Error:", error)
        print("Trying again in 60 seconds...")
        time.sleep(60)