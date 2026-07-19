import mysql.connector
import csv


# =====================================================
# Connexion MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="5853500",
    database="edusmart_learning"
)

cursor = conn.cursor()


# =====================================================
# Chemins CSV

DATA_PATH = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source2_mysql/data/"

MODULES_FILE = DATA_PATH + "modules.csv"
COURS_FILE = DATA_PATH + "cours.csv"
QUIZ_FILE = DATA_PATH + "quiz.csv"
NOTES_FILE = DATA_PATH + "notes.csv"
PROGRESSION_FILE = DATA_PATH + "progression.csv"
CONNEXIONS_FILE = DATA_PATH + "temps_connexion.csv"


# =====================================================
# Insertion modules
def insert_modules():

    with open(MODULES_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute(
                """
                INSERT INTO modules
                (
                    id_module,
                    code_module,
                    nom_module,
                    categorie,
                    niveau,
                    duree_heures,
                    actif
                )
                VALUES
                (
                    %(id_module)s,
                    %(code_module)s,
                    %(nom_module)s,
                    %(categorie)s,
                    %(niveau)s,
                    %(duree_heures)s,
                    %(actif)s
                )
                """,
                row
            )

    conn.commit()
    print("Modules insérés")


# =====================================================
# Insertion cours
def insert_cours():
    with open(COURS_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute(
                """
                INSERT INTO cours
                (
                    id_cours,
                    id_module,
                    titre,
                    ordre,
                    duree_minutes,
                    type_cours,
                    statut
                )
                VALUES
                (
                    %(id_cours)s,
                    %(id_module)s,
                    %(titre)s,
                    %(ordre)s,
                    %(duree_minutes)s,
                    %(type_cours)s,
                    %(statut)s
                )
                """,
                row
            )
    conn.commit()
    print("Cours insérés")

# =====================================================
# Insertion des quiz
def insert_quiz():
    with open(QUIZ_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        sql = """
        INSERT INTO quiz(
            id_quiz,
            id_cours,
            titre,
            nb_questions,
            score_max,
            duree_minutes
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        for row in reader:
            cursor.execute(
                sql,
                (
                    row["id_quiz"],
                    row["id_cours"],
                    row["titre"],
                    int(row["nb_questions"]),
                    float(row["score_max"]),
                    int(row["duree_minutes"])
                )
            )

    conn.commit()
    print("Quiz insérés")

# =====================================================
# Insertion notes
def insert_notes():
    with open(NOTES_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        sql = """
        INSERT INTO notes
        (
            id_note,
            id_quiz,
            student_code,
            date_passage,
            score,
            tentative,
            valide
        )
        VALUES
        (%s, %s, %s, %s, %s, %s, %s)
        """
        for row in reader:
            cursor.execute(
                sql,
                (
                    row["id_note"],
                    row["id_quiz"],
                    row["student_code"],
                    row["date_passage"],
                    float(row["score"]),
                    int(row["tentative"]),
                    row["valide"] == "True"
                )
            )
    conn.commit()
    print("Notes insérées")


# =====================================================
# Insertion progression
def insert_progression():
    with open(PROGRESSION_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        sql = """
        INSERT INTO progression
        (
            id_progression,
            student_code,
            id_module,
            pourcentage,
            dernier_cours,
            date_maj
        )
        VALUES
        (%s, %s, %s, %s, %s, %s)
        """

        for row in reader:
            cursor.execute(
                sql,
                (
                    row["id_progression"],
                    row["student_code"],
                    row["id_module"],
                    float(row["pourcentage"]),
                    row["dernier_cours"],
                    row["date_maj"]
                )
            )
    conn.commit()
    print("Progressions insérées")


# =====================================================
# Insertion temps_connexion
def insert_connexions():
    with open(CONNEXIONS_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        sql = """
        INSERT INTO temps_connexion
        (
            id_connexion,
            student_code,
            date_connexion,
            date_deconnexion,
            duree_minutes,
            appareil,
            navigateur,
            adresse_ip
        )
        VALUES
        (%s, %s, %s, %s, %s, %s, %s,%s
        )
        """
        for row in reader:
            cursor.execute(
                sql,
                (
                    row["id_connexion"],
                    row["student_code"],
                    row["date_connexion"],
                    row["date_deconnexion"],
                    int(row["duree_minutes"]),
                    row["appareil"],
                    row["navigateur"],
                    row["adresse_ip"]
                )
            )
    conn.commit()
    print("Temps de connexion insérés")

# =====================================================
# Execution

insert_modules()
insert_cours()
insert_quiz()
insert_notes()
insert_progression()
insert_connexions()


cursor.close()
conn.close()

print("Insertion terminée avec succès")