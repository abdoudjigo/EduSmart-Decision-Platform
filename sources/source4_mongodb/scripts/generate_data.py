import json
import uuid
import random
from faker import Faker
from datetime import datetime, timedelta
import os


fake = Faker("fr_FR")


# =====================================================
# Nombre de documents
NB_EVENTS = 200000


# =====================================================
# Chemins
BASE_PATH = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source4_mongodb/"
JSON_FILE = BASE_PATH + "json/events.json"


# =====================================================
# Types événements

EVENT_TYPES = [
    "LOGIN",
    "LOGOUT",
    "COURSE_OPENED",
    "COURSE_COMPLETED",
    "VIDEO_STARTED",
    "VIDEO_FINISHED",
    "QUIZ_STARTED",
    "QUIZ_SUBMITTED",
    "RESOURCE_DOWNLOADED",
    "SEARCH",
    "PROFILE_UPDATED",
    "PAYMENT_STARTED",
    "PAYMENT_SUCCESS",
    "PAYMENT_FAILED"
]

# =====================================================
# Génération événements
def generate_events():
    events = []
    for i in range(NB_EVENTS):
        event_type = random.choice(EVENT_TYPES)
        event = {
            "event_id": str(uuid.uuid4()),
            "student_code": f"LMS-{random.randint(1,15000):06d}",
            "timestamp": fake.date_time_between(
                start_date="-1y",
                end_date="now"
            ).isoformat(),
            "event_type": event_type,
            "module_code": f"MOD-{random.randint(1,30):02d}",
            "course_code": f"COURSE-{random.randint(1,300):03d}",
            "device": random.choice([
                "Samsung Galaxy A54",
                "iPhone 15",
                "PC",
                "Tablet"
            ]),
            "operating_system": random.choice([
                "Android",
                "iOS",
                "Windows"
            ]),
            "app_version": random.choice([
                "2.4.1",
                "2.4.0",
                "2.3.5"
            ]),
            "ip_address": fake.ipv4(),
            "city": random.choice([
                "Dakar",
                "Thiès",
                "Saint-Louis",
                "Touba"
            ]),
            "country": "Sénégal",
            "session_id": str(uuid.uuid4()),
            "duration_seconds": random.randint(
                10,
                3600
            ),
            "success": random.choice([
                True,
                False
            ])
        }

        # =============================================
        # Documents flexibles MongoDB
        if event_type == "QUIZ_SUBMITTED":
            event["quiz_code"] = f"QUIZ-{random.randint(1,900):03d}"
            event["metadata"] = {
                "score": random.randint(0,20),
                "attempt": random.randint(1,3),
                "network": random.choice([
                    "4G",
                    "Wifi",
                    "5G"
                ])
            }

        elif event_type in [
            "VIDEO_STARTED",
            "VIDEO_FINISHED"
        ]:
            event["metadata"] = {
                "video_quality": random.choice([
                    "720p",
                    "1080p",
                    "480p"
                ]),
                "buffer_time": random.randint(
                    0,
                    20
                )
            }

        elif event_type == "SEARCH":
            event["metadata"] = {
                "keyword": random.choice([
                    "Python",
                    "SQL",
                    "Machine Learning"
                ])
            }

        events.append(event)
    return events


# =====================================================
# Export JSON
def export_json(data, filename):
    os.makedirs(
        os.path.dirname(filename),
        exist_ok=True
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )

# =====================================================
# Execution
if __name__ == "__main__":
    events = generate_events()
    export_json(events, JSON_FILE)
    print("Events :", len(events))