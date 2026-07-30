import os
import shutil


# =====================================================
# CONFIGURATION
# =====================================================

SOURCE_DIR = "sources/source3_csv/generated_csv"

OUTPUT_DIR = "etl/staging/raw/csv"


# =====================================================
# CREATION DU DOSSIER DESTINATION
# =====================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)


print("=" * 60)
print("Extraction CSV")
print("=" * 60)


# =====================================================
# EXTRACTION DES FICHIERS CSV
# =====================================================

for file in os.listdir(SOURCE_DIR):

    if file.endswith(".csv"):

        source_file = os.path.join(
            SOURCE_DIR,
            file
        )

        destination_file = os.path.join(
            OUTPUT_DIR,
            file
        )


        shutil.copy2(
            source_file,
            destination_file
        )


        print(f"{file} extrait")


# =====================================================
# FIN
# =====================================================

print("=" * 60)
print("Extraction CSV terminée avec succès.")
print("=" * 60)