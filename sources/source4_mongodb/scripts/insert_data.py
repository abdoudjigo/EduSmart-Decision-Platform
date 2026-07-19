from pymongo import MongoClient
import json


# =====================================================
# Connexion MongoDB Docker

client = MongoClient("mongodb://localhost:27017")
db = client["edusmart_mobile"]
collection = db["events"]

# =====================================================
# Fichier JSON
EVENTS_FILE = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source4_mongodb/json/events.json"


# =====================================================
# Insertion des événements
def insert_events():
    with open(EVENTS_FILE, "r", encoding="utf-8") as file:
        events = json.load(file)
    collection.insert_many(events)
    print(f"{len(events)} événements insérés")


# =====================================================
# Execution
insert_events()
client.close()
print("Insertion MongoDB terminée")