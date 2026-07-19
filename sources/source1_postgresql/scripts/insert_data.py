import psycopg2
import csv


# =====================================================
# Connexion PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    dbname="edusmart_academic",
    user="postgres",
    password="5853500",
    port=5432
)

cursor = conn.cursor()



# =====================================================
# Fonction générale d'insertion CSV
def insert_csv(file_path, table, columns):
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            values = ",".join([f"%({col})s" for col in columns])

            query = f"""
            INSERT INTO {table}
            (
                {','.join(columns)}
            )
            VALUES
            (
                {values}
            )
            """
            cursor.execute(
                query,
                row
            )


# Chemins des CSV
BASE_PATH = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source1_postgresql/data"



# =====================================================
# 1) FILIERES
insert_csv(

    f"{BASE_PATH}/filieres.csv",

    "filieres",

    [
        "id_filiere",
        "code_filiere",
        "nom_filiere",
        "departement",
        "niveau",
        "duree_mois",
        "cout_total",
        "statut"
    ]
)



# =====================================================
# 2) CLASSES
insert_csv(

    f"{BASE_PATH}/classes.csv",

    "classes",

    [
        "id_classe",
        "code_classe",
        "nom_classe",
        "id_filiere",
        "annee_academique",
        "capacite",
        "salle",
        "responsable"
    ]
)



# =====================================================
# 3) ETUDIANTS
insert_csv(

    f"{BASE_PATH}/etudiants.csv",

    "etudiants",

    [
        "id_etudiant",
        "matricule",
        "nom",
        "prenom",
        "sexe",
        "date_naissance",
        "telephone",
        "email",
        "adresse",
        "ville",
        "region",
        "pays",
        "date_creation"
    ]
)



# =====================================================
# 4) INSCRIPTIONS
insert_csv(

    f"{BASE_PATH}/inscriptions.csv",

    "inscriptions",

    [
        "id_inscription",
        "id_etudiant",
        "id_classe",
        "date_inscription",
        "statut",
        "type_inscription",
        "bourse",
        "reduction"
    ]
)



# =====================================================
# 5) PAIEMENTS
insert_csv(

    f"{BASE_PATH}/paiements.csv",

    "paiements",

    [
        "id_paiement",
        "id_inscription",
        "reference",
        "date_paiement",
        "montant",
        "mode_paiement",
        "statut",
        "tranche"
    ]
)



# =====================================================
# Validation
conn.commit()
cursor.close()
conn.close()
print("Toutes les données ont été insérées avec succès")