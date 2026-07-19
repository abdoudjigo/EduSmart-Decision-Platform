import csv
import uuid
import random
from datetime import datetime

from faker import Faker
fake = Faker("fr_FR")

# Nombres d'elements à générer
NB_ETUDIANTS = 120000
NB_FILIERES = 20
NB_CLASSES = 100
NB_INSCRIPTIONS = 15000
NB_PAIEMENTS = 25000

# Chemin du fichier de sortie
ETUDIANTS_FILE  = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source1_postgresql/data/etudiants.csv"
FILIERES_FILE = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source1_postgresql/data/filieres.csv"
CLASSES_FILE = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source1_postgresql/data/classes.csv"
INSCRIPTIONS_FILE = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source1_postgresql/data/inscriptions.csv"
PAIEMENTS_FILE = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source1_postgresql/data/paiements.csv"


# =====================================================
# fonction génération des étudiants
def generate_students():
    students = []
    for i in range(1, NB_ETUDIANTS + 1):
        student = {
            "id_etudiant": str(uuid.uuid4()),
            "matricule": f"EDU{i:06d}",
            "nom": fake.last_name(),
            "prenom": fake.first_name(),
            "sexe": random.choice(["M", "F"]),
            "date_naissance": fake.date_of_birth(
                minimum_age=18,
                maximum_age=35
            ),
            "telephone": fake.phone_number(),
            "email": fake.unique.email(),
            "adresse": fake.address(),
            "ville": fake.city(),
            "region": random.choice([
                "Dakar",
                "Thiès",
                "Saint-Louis",
                "Kaolack",
                "Saint-Louis",
                "Kébémer",
                "Kaffrine",
                "Diamniadio",
                "Touba",
                "Tivaouane",
                "Fatick",
                "Ziguinchor"
            ]),
            "pays": "Sénégal",
            "date_creation": datetime.now()
        }
        students.append(student)
    return students


# =====================================================
# fonction génération de filiere
def generate_filieres():
    filieres = []
    noms = [
        "Informatique",
        "Developpeur Data",
        "Intelligence Artificielle",
        "Réseaux",
        "Cybersécurité",
        "Développement Web",
        "AWS",
        "Referent Digital"
    ]
    for i in range(1, NB_FILIERES + 1):
        filiere = {
            "id_filiere": str(uuid.uuid4()),
            "code_filiere": f"FIL{i:03d}",
            "nom_filiere": random.choice(noms),
            "departement": random.choice([
                "Informatique",
                "Sciences",
                "Technologie"
            ]),
            "niveau": random.choice([
                "Licence1",
                "Licence2",
                "Licence3",
                "Master1",
                "Master2"
            ]),
            "duree_mois": random.choice([
                24,
                36,
                48
            ]),
            "cout_total": random.randint(
                300000,
                1500000
            ),
            "statut": random.choice([
                "ACTIVE",
                "INACTIVE"
            ])
        }
        filieres.append(filiere)
    return filieres

# =====================================================
# fonction génération des classes
def generate_classes(filieres):
    classes = []
    for i in range(1, NB_CLASSES + 1):
        filiere = random.choice(filieres)
        classe = {
            "id_classe": str(uuid.uuid4()),
            "code_classe": f"CLS{i:04d}",
            "nom_classe": f"Classe {i}",
            # Relation avec filiere
            "id_filiere": filiere["id_filiere"],
            "annee_academique": random.choice([
                "2024-2025",
                "2025-2026",
                "2026-2027"
            ]),
            "capacite": random.randint(
                20,
                60
            ),
            "salle": random.choice([
                "A101",
                "Salle A101",
                "A-101",
                "B202",
                "C303"
            ]),
            "responsable": fake.name()
        }
        classes.append(classe)
    return classes

# =====================================================
# Fonction génération des inscriptions
# ETUDIANTS
#      |
#      | 1,N
#      |
# INSCRIPTIONS
#      |
#      | N,1
#      |
# CLASSES
# Une inscription relie un étudiant à une classe existante.
# =====================================================
def generate_inscriptions(students, classes):
    inscriptions = []
    for i in range(1, NB_INSCRIPTIONS + 1):
        # On récupère un étudiant existant
        student = random.choice(students)
        # On récupère une classe existante
        classe = random.choice(classes)
        inscription = {
            "id_inscription": str(uuid.uuid4()),
            # Clé étrangère vers etudiants
            "id_etudiant": student["id_etudiant"],
            # Clé étrangère vers classes
            "id_classe": classe["id_classe"],
            "date_inscription": fake.date_between(
                start_date="-2y",
                end_date="today"
            ),
            "statut": random.choice([
                "INSCRIT",
                "ANNULE",
                "TERMINE"
            ]),
            "type_inscription": random.choice([
                "Nouvelle",
                "Réinscription"
            ]),
            "bourse": random.choice([
                True,
                False
            ]),
            "reduction": random.choice([
                0,
                10,
                25,
                50
            ])
        }
        inscriptions.append(inscription)
    return inscriptions

# =====================================================
# Fonction génération des paiements
# INSCRIPTIONS
#       |
#       | 1,N
#       |
#  PAIEMENTS
# Chaque paiement appartient à une inscription existante
# =====================================================
def generate_paiements(inscriptions):
    paiements = []
    for i in range(1, NB_PAIEMENTS + 1):
        # Choisir une inscription existante
        inscription = random.choice(inscriptions)
        paiement = {
            "id_paiement": str(uuid.uuid4()),
            # Clé étrangère vers inscriptions
            "id_inscription": inscription["id_inscription"],
            "reference": f"PAY{i:07d}",
            "date_paiement": fake.date_between(
                start_date="-2y",
                end_date="today"
            ),
            "montant": random.choice([
                50000,
                100000,
                150000,
                200000,
                300000
            ]),
            "mode_paiement": random.choice([
                "Espèces",
                "OM",
                "Wave",
                "Orange Money"
            ]),
            "statut": random.choice([
                "VALIDE",
                "EN_ATTENTE",
                "ANNULE"
            ]),
            "tranche": random.choice([
                "1ère",
                "2ème",
                "3ème"
            ])
        }
        paiements.append(paiement)
    return paiements


# =====================================================
# fonction export CSV
def export_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file,fieldnames=data[0].keys())

        writer.writeheader()
        writer.writerows(data)


# =====================================================
# Exécution
if __name__ == "__main__":

    students = generate_students()
    export_csv(students, ETUDIANTS_FILE)

    # Conservation des IDs pour les relations futures
    #student_ids = [
    #    student["id_etudiant"]
    #    for student in students
    #]

    filieres = generate_filieres()
    export_csv(filieres, FILIERES_FILE)

    classes = generate_classes(filieres)
    export_csv(classes, CLASSES_FILE)

    inscriptions = generate_inscriptions(students, classes)
    export_csv(inscriptions, INSCRIPTIONS_FILE)

    paiements = generate_paiements(inscriptions)
    export_csv(paiements, PAIEMENTS_FILE)

    print(f"{len(students)} étudiants générés")
    print(f"{len(filieres)} filieres générés")
    print(f"{len(classes)} classes générés")
    print(f"{len(inscriptions)} inscriptions générés")
    print(f"{len(paiements)} paiements générés")
   # print(f"{len(student_ids)} identifiants étudiants disponibles")