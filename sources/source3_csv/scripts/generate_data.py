import csv
import random
import uuid
from faker import Faker
from datetime import datetime, timedelta


fake = Faker("fr_FR")


# =====================================================
# Volumes
NB_ENSEIGNANTS = 5000
NB_DEPARTEMENTS = 30
NB_SALAIRES = 60000
NB_ABSENCES = 30000


# =====================================================
# Chemins fichiers

DATA_PATH = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source3_csv/generated_csv/"

ENSEIGNANTS_FILE = DATA_PATH + "enseignants.csv"
DEPARTEMENTS_FILE = DATA_PATH + "departements.csv"
SALAIRES_FILE = DATA_PATH + "salaires.csv"
ABSENCES_FILE = DATA_PATH + "absences.csv"


# =====================================================
# Génération enseignants
def generate_enseignants():
    enseignants = []
    specialites = [
        "Data Science",
        "Intelligence Artificielle",
        "IA",
        "Python",
        "Cybersécurité",
        "Cloud",
        "Base de données"
    ]
    grades = [
        "Assistant",
        "Maître Assistant",
        "Professeur",
        "Vacataire"
    ]
    statuts = [
        "Permanent",
        "Vacataire"
    ]
    for i in range(1, NB_ENSEIGNANTS + 1):
        enseignant = {
            "teacher_code": f"TEACH-{i:05d}",
            "nom": fake.last_name(),
            "prenom": fake.first_name(),
            "sexe": random.choice(["M", "F"]),
            "date_naissance": fake.date_of_birth(
                minimum_age=25,
                maximum_age=65
            ),
            "telephone": fake.phone_number(),
            "email": fake.email(),
            "specialite": random.choice(specialites),
            "grade": random.choice(grades),
            "date_embauche": fake.date_between(
                start_date="-20y",
                end_date="-1y"
            ),
            "statut": random.choice(statuts)
        }
        enseignants.append(enseignant)
    return enseignants


# =====================================================
# Génération départements
def generate_departements():
    departements = []
    noms = [
        "Data",
        "Informatique",
        "Développement",
        "Cybersécurité",
        "Cloud",
        "Réseaux",
        "Intelligence Artificielle"
    ]
    for i in range(1, NB_DEPARTEMENTS + 1):
        departement = {
            "id_departement": i,
            "nom_departement": random.choice(noms),
            "responsable": fake.name(),
            "budget_annuel": round(
                random.uniform(500000,5000000),
                2
            ),
            "batiment": f"Bâtiment {random.randint(1,10)}"
        }
        departements.append(departement)
    return departements

# =====================================================
# Génération salaires
def generate_salaires(enseignants):
    salaires = []
    modes = [
        "Banque",
        "Virement",
        "Wave",
        "Orange Money"
    ]
    id_salaire = 1
    for enseignant in enseignants:
        for mois in range(1,13):

            salaire_base = random.randint(
                250000,
                800000
            )
            primes = random.randint(
                0,
                200000
            )
            retenues = random.randint(
                0,
                50000
            )
            salaire = {
                "id_salaire": id_salaire,
                "teacher_code": enseignant["teacher_code"],
                "mois": mois,
                "annee": 2025,
                "salaire_base": salaire_base,
                "primes": primes,
                "retenues": retenues,
                "salaire_net": salaire_base + primes - retenues,
                "mode_paiement": random.choice(modes)
            }
            salaires.append(salaire)
            id_salaire += 1
    return salaires


# =====================================================
# Génération absences
def generate_absences(enseignants):
    absences = []
    motifs = [
        "Maladie",
        "Congé",
        "Mission",
        "Personnel",
        None
    ]
    for i in range(1, NB_ABSENCES + 1):
        enseignant = random.choice(enseignants)
        absence = {
            "id_absence": i,
            "teacher_code": enseignant["teacher_code"],
            "date_absence": fake.date_between(
                start_date="-2y",
                end_date="today"
            ),
            "motif": random.choice(motifs),
            "justifiee": random.choice(
                [True, False]
            ),
            "duree_heures": random.randint(
                1,
                24
            ),
            "remplace": random.choice(
                [True, False]
            )
        }
        absences.append(absence)
    return absences


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
# Execution

if __name__ == "__main__":

    enseignants = generate_enseignants()
    departements = generate_departements()
    salaires = generate_salaires(enseignants)
    absences = generate_absences(enseignants)


    export_csv(enseignants, ENSEIGNANTS_FILE)

    export_csv(departements, DEPARTEMENTS_FILE)

    export_csv(salaires, SALAIRES_FILE)

    export_csv(absences, ABSENCES_FILE)

    print("Enseignants :", len(enseignants))
    print("Départements :", len(departements))
    print("Salaires :", len(salaires))
    print("Absences :", len(absences))