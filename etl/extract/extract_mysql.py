import os
import pandas as pd
import pymysql


# =====================================================
# CONFIGURATION
# =====================================================

HOST = os.getenv("DB_HOST", "localhost")
PORT = 3306
DATABASE = "edusmart_learning"

USER = "root"
PASSWORD = "5853500"

OUTPUT_DIR = "etl/staging/raw/mysql"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =====================================================
# CONNEXION MYSQL
# =====================================================

connection = pymysql.connect(
    host=HOST,
    port=PORT,
    user=USER,
    password= PASSWORD,
    database=DATABASE
)
cursor = connection.cursor()


# =====================================================
# RECUPERATION DES TABLES
# =====================================================

cursor.execute("SHOW TABLES;")

tables = [table[0] for table in cursor.fetchall()]


print("=" * 60)
print("Extraction MySQL")
print("=" * 60)


# =====================================================
# EXTRACTION
# =====================================================

for table in tables:

    print(f"Extraction : {table}")

    query = f"SELECT * FROM {table};"

    df = pd.read_sql(query, connection)

    output_file = os.path.join(
        OUTPUT_DIR,
        f"{table}.csv"
    )

    df.to_csv(
        output_file,
        index=False,
        encoding="utf-8"
    )

    print(f"   -> {len(df)} lignes exportées")


# =====================================================
# FERMETURE
# =====================================================

cursor.close()
connection.close()


print("=" * 60)
print("Extraction MySQL terminée avec succès.")
print("=" * 60)