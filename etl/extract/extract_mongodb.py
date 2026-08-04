from pymongo import MongoClient
import json
import os


# =====================================================
# CONFIGURATION MONGODB
# =====================================================

HOST = os.getenv("DB_HOST", "localhost")
PORT = 27017

DATABASE = "edusmart_mobile"
COLLECTION = "events"


# Destination staging RAW

OUTPUT_DIR = "etl/staging/raw/mongodb"
OUTPUT_FILE = "events.json"


# =====================================================
# CREATION DU DOSSIER
# =====================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


output_path = os.path.join(
    OUTPUT_DIR,
    OUTPUT_FILE
)


# =====================================================
# CONNEXION MONGODB
# =====================================================

client = MongoClient(
    HOST,
    PORT
)


db = client[DATABASE]

collection = db[COLLECTION]


print("=" * 60)
print("Extraction MongoDB")
print("=" * 60)


# =====================================================
# EXTRACTION DES DOCUMENTS
# =====================================================

events = []


for document in collection.find():

    # Conversion ObjectId MongoDB en texte
    document["_id"] = str(document["_id"])

    events.append(document)



# =====================================================
# ECRITURE JSON
# =====================================================

with open(
    output_path,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        events,
        file,
        ensure_ascii=False,
        indent=4
    )


print(f"{len(events)} événements extraits")

print(f"Fichier créé : {output_path}")


client.close()


print("=" * 60)
print("Extraction MongoDB terminée")
print("=" * 60)