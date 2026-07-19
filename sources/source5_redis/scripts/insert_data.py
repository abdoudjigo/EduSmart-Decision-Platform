import redis
import json


# =====================================================
# Connexion Redis Docker

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


# =====================================================
# Fichier JSON
DATA_FILE = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source5_redis/data/redis_data.json"


# =====================================================
# Insertion Redis
def insert_redis_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    for key, value in data.items():
        r.set(
            key,
            json.dumps(value, ensure_ascii=False)
        )
    print(len(data), "clés Redis insérées")


# =====================================================
# Execution
insert_redis_data()
print("Insertion Redis terminée")