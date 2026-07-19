import json
import random
from faker import Faker
from datetime import datetime


fake = Faker("fr_FR")


# Nombre de données
NB_ETUDIANTS = 10000
NB_PROGRESSIONS = 50000


# Fichier sortie
OUTPUT_FILE = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source5_redis/data/redis_data.json"


def generate_student_code():
    return f"LMS-{random.randint(1, NB_ETUDIANTS):06d}"


def generate_sessions():
    data = {}
    for i in range(NB_ETUDIANTS):
        student = generate_student_code()
        key = f"session:{student}"
        data[key] = {
            "status": random.choice(
                [
                    "online",
                    "offline"
                ]
            ),
            "last_activity": str(
                fake.date_time_between(
                    start_date="-1d",
                    end_date="now"
                )
            ),
            "device": random.choice(
                [
                    "Mobile",
                    "PC",
                    "Tablette"
                ]
            )
        }
    return data


def generate_progressions():
    data = {}
    for i in range(NB_PROGRESSIONS):
        student = generate_student_code()
        module = f"MOD-{random.randint(1,100):03d}"
        key = f"progress:{student}:{module}"
        data[key] = {
            "module": module,
            "percentage": round(
                random.uniform(0,100),
                2
            )
        }
    return data


def generate_statistics():

    return {
        "stats:platform": {
            "connected_users": random.randint(100,5000),
            "courses_opened": random.randint(1000,50000),
            "quiz_completed": random.randint(500,30000)
        }
    }



def generate_data():
    data = {}
    data.update(generate_sessions())
    data.update(generate_progressions())
    data.update(generate_statistics())
    return data



if __name__ == "__main__":
    redis_data = generate_data()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        json.dump(
            redis_data,
            file,
            indent=4,
            ensure_ascii=False
        )


    print(len(redis_data), "clés Redis générées")