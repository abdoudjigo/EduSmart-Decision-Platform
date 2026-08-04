import os
import pandas as pd
import psycopg2

# ==============================
# Configuration PostgreSQL
# ==============================

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": 5432,
    "database": "edusmart_academic",
    "user": "postgres",
    "password": "5853500"
}

# ==============================
# Dossier de sortie
# ==============================

OUTPUT_DIR = "etl/staging/raw/postgres"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================
# Tables à extraire
# ==============================

TABLES = [
    "etudiants",
    "filieres",
    "classes",
    "inscriptions",
    "paiements"
]

# ==============================
# Connexion
# ==============================

print("Connexion à PostgreSQL...")

conn = psycopg2.connect(**DB_CONFIG)

print("Connexion réussie.\n")

# ==============================
# Extraction
# ==============================

for table in TABLES:

    print(f"Extraction de : {table}")

    query = f"SELECT * FROM {table};"

    df = pd.read_sql(query, conn)

    output_file = os.path.join(
        OUTPUT_DIR,
        f"{table}.csv"
    )

    df.to_csv(output_file, index=False)

    print(f"   {len(df)} lignes exportées")
    print(f"   Fichier : {output_file}\n")

conn.close()

print("Extraction PostgreSQL terminée avec succès.")