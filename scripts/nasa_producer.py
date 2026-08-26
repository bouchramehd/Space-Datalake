import json
import time
import requests
from kafka import KafkaProducer

NASA_URL = "https://api.nasa.gov/neo/rest/v1/feed"
TOPIC = "nasa-neows"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

print("NASA NeoWs producer started")
print(f"Sending data to Kafka topic: {TOPIC}")

while True:
    try:
        response = requests.get(
            NASA_URL,
            params={"api_key": "DEMO_KEY"},
            timeout=30
        )
        response.raise_for_status()

        data = response.json()

        sent = 0

        for date, asteroids in data["near_earth_objects"].items():
            for asteroid in asteroids:

                close_approach = asteroid.get("close_approach_data", [])

                approach = close_approach[0] if close_approach else {}

                message = {
                    "id": asteroid["id"],
                    "name": asteroid["name"],
                    "date": date,
                    "absolute_magnitude": asteroid.get("absolute_magnitude_h"),
                    "estimated_diameter_min_km":
                        asteroid["estimated_diameter"]["kilometers"][
                            "estimated_diameter_min"
                        ],
                    "estimated_diameter_max_km":
                        asteroid["estimated_diameter"]["kilometers"][
                            "estimated_diameter_max"
                        ],
                    "potentially_hazardous":
                        asteroid["is_potentially_hazardous_asteroid"],
                    "close_approach_date":
                        approach.get("close_approach_date"),
                    "relative_velocity_kmh":
                        approach.get("relative_velocity", {}).get(
                            "kilometers_per_hour"
                        ),
                    "miss_distance_km":
                        approach.get("miss_distance", {}).get("kilometers")
                }

                producer.send(TOPIC, value=message)

                sent += 1

                print(
                    f"Sent #{sent}: {message['name']} | "
                    f"Hazardous={message['potentially_hazardous']}"
                )

        producer.flush()

        print(f"Batch complete: {sent} events sent")
        print("Waiting 60 seconds...\n")

        time.sleep(60)

    except Exception as error:
        print("ERROR:", error)
        print("Retrying in 60 seconds...\n")
        time.sleep(60)