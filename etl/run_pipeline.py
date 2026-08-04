import subprocess
import sys

# Liste des étapes, dans l'ordre exact du pipeline
STEPS = [
    "etl/extract/extract_postgres.py",
    "etl/extract/extract_mysql.py",
    "etl/extract/extract_mongodb.py",
    "etl/extract/extract_redis.py",
    "etl/transform/transform.py",
]

for step in STEPS:
    print("=" * 60)
    print(f"Exécution : {step}")
    print("=" * 60)

    result = subprocess.run([sys.executable, step])

    # Si une étape échoue, on arrête tout de suite (pas de sens à continuer sur des données corrompues)
    if result.returncode != 0:
        print(f"ÉCHEC à l'étape : {step}")
        sys.exit(1)

print("=" * 60)
print("Pipeline ETL complet terminé avec succès.")
print("=" * 60)
