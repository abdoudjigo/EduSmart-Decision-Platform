import csv
import random
import os


# =====================================================
# Chemins


SOURCE_PATH = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source3_csv/generated_csv/"
ANOMALIES_PATH = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source3_csv/generated_csv_anomalies/"


ENSEIGNANTS_FILE = SOURCE_PATH + "enseignants.csv"
DEPARTEMENTS_FILE = SOURCE_PATH + "departements.csv"
SALAIRES_FILE = SOURCE_PATH + "salaires.csv"
ABSENCES_FILE = SOURCE_PATH + "absences.csv"


ENSEIGNANTS_ANOMALIES = ANOMALIES_PATH + "enseignants_anomalies.csv"
DEPARTEMENTS_ANOMALIES = ANOMALIES_PATH + "departements_anomalies.csv"
SALAIRES_ANOMALIES = ANOMALIES_PATH + "salaires_anomalies.csv"
ABSENCES_ANOMALIES = ANOMALIES_PATH + "absences_anomalies.csv"



# =====================================================
# Lecture CSV
def read_csv(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


# =====================================================
# Export CSV
def export_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=data[0].keys()
        )
        writer.writeheader()
        writer.writerows(data)


# =====================================================
# Anomalies enseignants
def introduce_enseignants_anomalies():
    data = read_csv(ENSEIGNANTS_FILE)

    for row in data:
        hasard = random.random()
        # Email manquant
        if hasard < 0.05:
            row["email"] = ""

        # Téléphones mal formatés
        if hasard < 0.05:
            row["telephone"] = random.choice([
                "771234567",
                "77-123-45-67",
                "+221771234567"
            ])

        # Spécialités différentes
        if hasard < 0.05:
            row["specialite"] = random.choice([
                "IA",
                "Intelligence Artificielle",
                "Data Science"
            ])

        # Grades incohérents
        if hasard < 0.03:
            row["grade"] = random.choice([
                "Prof",
                "Professeur Senior",
                "Assistant?"
            ])
    export_csv(data, ENSEIGNANTS_ANOMALIES)
    print("Anomalies enseignants terminées")


# =====================================================
# Anomalies départements
def introduce_departements_anomalies():
    data = read_csv(DEPARTEMENTS_FILE)

    for row in data:
        if random.random() < 0.1:
            row["nom_departement"] = random.choice([
                "Data",
                "Data Engineering",
                "Développement Data"
            ])

        if random.random() < 0.05:
            row["budget_annuel"] = ""

    export_csv(data, DEPARTEMENTS_ANOMALIES)
    print("Anomalies départements terminées")


# =====================================================
# Anomalies salaires
def introduce_salaires_anomalies():
    data = read_csv(SALAIRES_FILE)

    for row in data:
        if random.random() < 0.02:
            row["salaire_base"] = "-50000"

        if random.random() < 0.05:
            row["mode_paiement"] = random.choice([
                "Banque",
                "bank transfer",
                "Virement",
                "Wave"
            ])

        if random.random() < 0.02:
            row["primes"] = "999999"

    # ajouter quelques doublons
    data.extend(
        random.sample(data, 100)
    )

    export_csv(data, SALAIRES_ANOMALIES)
    print("Anomalies salaires terminées")


# =====================================================
# Anomalies absences
def introduce_absences_anomalies():
    data = read_csv(ABSENCES_FILE)

    for row in data:
        if random.random() < 0.05:
            row["motif"] = ""

        if random.random() < 0.03:
            row["duree_heures"] = "200"

        if random.random() < 0.02:
            row["date_absence"] = "2035-01-01"

    # doublons
    data.extend(random.sample(data, 100))
    export_csv(data, ABSENCES_ANOMALIES)

    print("Anomalies absences terminées")


# =====================================================
# Execution
if __name__ == "__main__":
    introduce_enseignants_anomalies()
    introduce_departements_anomalies()
    introduce_salaires_anomalies()
    introduce_absences_anomalies()
    print("Création des fichiers avec anomalies terminée")