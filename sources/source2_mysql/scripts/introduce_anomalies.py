import csv
import random
import os
import uuid



# =====================================================
# Chemins
DATA_PATH = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source2_mysql/data/"
ANOMALIES_PATH = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source2_mysql/data_anomalies/"


MODULES_FILE = DATA_PATH + "modules.csv"
COURS_FILE = DATA_PATH + "cours.csv"
QUIZ_FILE = DATA_PATH + "quiz.csv"
NOTES_FILE = DATA_PATH + "notes.csv"
PROGRESSION_FILE = DATA_PATH + "progression.csv"
CONNEXIONS_FILE = DATA_PATH + "temps_connexion.csv"

# Création du dossier anomalies
os.makedirs(ANOMALIES_PATH, exist_ok=True)


MODULES_ANOMALIES = ANOMALIES_PATH + "modules_anomalies.csv"
COURS_ANOMALIES = ANOMALIES_PATH + "cours_anomalies.csv"
QUIZ_ANOMALIES = ANOMALIES_PATH + "quiz_anomalies.csv"
NOTES_ANOMALIES = ANOMALIES_PATH + "notes_anomalies.csv"
PROGRESSION_ANOMALIES = ANOMALIES_PATH + "progression_anomalies.csv"
CONNEXIONS_ANOMALIES = ANOMALIES_PATH + "temps_connexion_anomalies.csv"




# =====================================================
# Anomalies modules
def introduce_modules_anomalies():
    with open(MODULES_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        modules = list(reader)
    for module in modules:
        # Anomalie catégorie
        if random.random() < 0.15:
            module["categorie"] = random.choice([
                "data",
                "DATA",
                "Data Science",
                "data engineering"
            ])
    with open(MODULES_ANOMALIES, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=modules[0].keys()
        )
        writer.writeheader()
        writer.writerows(modules)
    print("Anomalies modules terminées")


# =====================================================
# Anomalies cours
def introduce_cours_anomalies():
    with open(COURS_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        cours = list(reader)
    # Création de doublons de titres
    for i in range(10):
        cours_copie = cours[random.randint(0, len(cours)-1)].copy()
        cours.append(cours_copie)

    with open(COURS_ANOMALIES, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=cours[0].keys()
        )
        writer.writeheader()
        writer.writerows(cours)
    print("Anomalies cours terminées")


# =====================================================
# Anomalies quiz
def introduce_quiz_anomalies():
    with open(QUIZ_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        quiz = list(reader)

    for q in quiz:
        if random.random() < 0.05:
            q["duree_minutes"] = random.choice([
                "-10",
                "500",
                "1000"
            ])
    with open(QUIZ_ANOMALIES, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=quiz[0].keys()
        )
        writer.writeheader()
        writer.writerows(quiz)
    print("Anomalies quiz terminées")


# =====================================================
# Anomalies notes
def introduce_notes_anomalies():
    with open(NOTES_FILE, "r", encoding="utf-8") as file,\
         open(NOTES_ANOMALIES, "w", newline="", encoding="utf-8") as outfile:
        reader = csv.DictReader(file)
        writer = csv.DictWriter(
            outfile,
            fieldnames=reader.fieldnames
        )
        writer.writeheader()
        for row in reader:
            # Score incorrect
            if random.random() < 0.03:
                row["score"] = random.choice([
                    "-5",
                    "120",
                    "150"
                ])
            # Tentative incorrecte
            if random.random() < 0.02:

                row["tentative"] = random.choice([
                    "0",
                    "10"
                ])
            # Date future
            if random.random() < 0.01:
                row["date_passage"] = "2030-01-01 12:00:00"
            writer.writerow(row)

    print("Anomalies notes terminées")


# =====================================================
# Anomalies progression
def introduce_progression_anomalies():
    with open(PROGRESSION_FILE, "r", encoding="utf-8") as file,\
         open(PROGRESSION_ANOMALIES, "w", newline="", encoding="utf-8") as outfile:
        reader = csv.DictReader(file)
        writer = csv.DictWriter(
            outfile,
            fieldnames=reader.fieldnames
        )
        writer.writeheader()

        for row in reader:
            # Pourcentage incorrect
            if random.random() < 0.03:
                row["pourcentage"] = random.choice([
                    "-20",
                    "120",
                    "150"
                ])
            # Module inexistant
            if random.random() < 0.01:

                row["id_module"] = str(uuid.uuid4())
            writer.writerow(row)
    print("Anomalies progression terminées")

# Anomalies connexion
def introduce_connexions_anomalies():
    with open(CONNEXIONS_FILE, "r", encoding="utf-8") as file,\
         open(CONNEXIONS_ANOMALIES, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(file)
        writer = csv.DictWriter(
            outfile,
            fieldnames=reader.fieldnames
        )
        writer.writeheader()
        for row in reader:
            # Déconnexion manquante
            if random.random() < 0.02:

                row["date_deconnexion"] = ""

            # Durée négative
            if random.random() < 0.01:

                row["duree_minutes"] = "-50"

            # IP invalide
            if random.random() < 0.01:

                row["adresse_ip"] = random.choice([
                    "999.999.999.999",
                    "abc.ip",
                    "123"
                ])
            # Appareil non standard
            if random.random() < 0.05:

                row["appareil"] = random.choice([
                    "mobile",
                    "TEL",
                    "ordinateur"
                ])
            writer.writerow(row)
    print("Anomalies connexions terminées")



# =====================================================
# Execution
if __name__ == "__main__":
    introduce_modules_anomalies()
    introduce_cours_anomalies()
    introduce_quiz_anomalies()
    introduce_notes_anomalies()
    introduce_progression_anomalies()
    introduce_connexions_anomalies()
    print("Toutes les anomalies sont générées")