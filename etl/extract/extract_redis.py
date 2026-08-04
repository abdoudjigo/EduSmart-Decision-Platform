import redis
import json
import os


# =====================================================
# CONFIGURATION REDIS
# =====================================================

HOST = os.getenv("DB_HOST", "localhost")
PORT = 6379
DB = 0


# Destination RAW

OUTPUT_DIR = "etl/staging/raw/redis"
OUTPUT_FILE = "redis_data.json"


# =====================================================
# CREATION DOSSIER
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
# CONNEXION REDIS
# =====================================================

client = redis.Redis(
    host=HOST,
    port=PORT,
    db=DB,
    decode_responses=True
)


print("=" * 60)
print("Extraction Redis")
print("=" * 60)


# Vérification connexion

client.ping()

print("Connexion Redis OK")


# =====================================================
# EXTRACTION DES CLES
# =====================================================

data = {}

keys = client.keys("*")


for key in keys:

    value = client.get(key)

    data[key] = value



# =====================================================
# ECRITURE JSON
# =====================================================

with open(
    output_path,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        data,
        file,
        ensure_ascii=False,
        indent=4
    )


print(f"{len(keys)} clés extraites")

print(f"Fichier créé : {output_path}")


print("=" * 60)
print("Extraction Redis terminée")
print("=" * 60)