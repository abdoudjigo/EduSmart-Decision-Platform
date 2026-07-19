import csv
import uuid
import random
from datetime import datetime
from faker import Faker
from datetime import timedelta

fake = Faker("fr_FR")

# =====================================================
# nbre d'elements à générer
NB_MODULES = 15
NB_COURS = 300
NB_QUIZ = 900
NB_NOTES = 150000
NB_PROGRESSION = 120000
NB_CONNEXIONS = 300000
NB_ETUDIANTS = 120000

# =====================================================
# Fichiers de sortie
MODULES_FILE = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source2_mysql/data/modules.csv"
COURS_FILE = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source2_mysql/data/cours.csv"
QUIZ_FILE = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source2_mysql/data/quiz.csv"
NOTES_FILE = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source2_mysql/data/notes.csv"
PROGRESSION_FILE = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source2_mysql/data/progression.csv"
CONNEXIONS_FILE = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source2_mysql/data/temps_connexion.csv"

# =====================================================
# Génération des modules
def generate_modules():
    modules = []
    noms = [
        "Python",
        "SQL",
        "Power BI",
        "Machine Learning",
        "Deep Learning",
        "Data Engineering",
        "Docker",
        "Linux",
        "Git",
        "Spark",
        "Kafka",
        "NoSQL",
        "Cloud AWS",
        "Azure",
        "Cybersécurité"
    ]
    for i in range(1, NB_MODULES + 1):
        module = {
            "id_module": str(uuid.uuid4()),
            "code_module": f"MOD{i:03d}",
            "nom_module": noms[i-1],
            "categorie": random.choice([
                "Data",
                "Développement",
                "Cloud",
                "Infrastructure"
            ]),
            "niveau": random.choice(["Débutant", "Intermédiaire", "Avancé"]),
            "duree_heures": random.choice([20, 30, 40, 60, 80]),
            "actif": random.choice([1, 0])
        }
        modules.append(module)
    return modules

# =====================================================
# Génération des cours
# Un module possède plusieurs cours
def generate_cours(modules):
    cours = []
    titres = [
        "Introduction",
        "Les fondamentaux",
        "Concepts avancés",
        "Travaux pratiques",
        "Projet guidé",
        "Étude de cas",
        "Bonnes pratiques",
        "Optimisation",
        "Déploiement",
        "Conclusion"
    ]
    types = [
        "VIDEO",
        "PDF",
        "ARTICLE",
        "LIVE"
    ]
    for i in range(1, NB_COURS + 1):
        module = random.choice(modules)
        cours_data = {
            "id_cours": str(uuid.uuid4()),
            "id_module": module["id_module"],
            "titre": f"{random.choice(titres)} - {module['nom_module']}",
            "ordre": random.randint(1,10),
            "duree_minutes": random.randint(15,180),
            "type_cours": random.choice(types),
            "statut": "PUBLIE"
        }
        cours.append(cours_data)
    return cours

# =====================================================
# Génération des quiz
# Un cours possède plusieurs quiz
def generate_quiz(cours):
    quiz = []
    titres = [
        "Quiz d'introduction",
        "Quiz intermédiaire",
        "Quiz final",
        "Évaluation pratique",
        "Test de connaissances"
    ]
    for i in range(1, NB_QUIZ + 1):
        cours_data = random.choice(cours)
        quiz_data = {
            "id_quiz": str(uuid.uuid4()),
            "id_cours": cours_data["id_cours"],
            "titre": random.choice(titres),
            "nb_questions": random.randint(5,30),
            "score_max":100,
            "duree_minutes": random.randint(10,60)
        }
        quiz.append(quiz_data)
    return quiz

# =====================================================
# Génération des notes
# Un étudiant peut passer plusieurs quiz
def generate_notes(quiz):
    notes = []
    for i in range(1, NB_NOTES + 1):
        quiz_data = random.choice(quiz)
        note = {
            "id_note": str(uuid.uuid4()),
            # Même étudiant logique que PostgreSQL
            "student_code": f"LMS-{random.randint(1, NB_ETUDIANTS):06d}",           # Relation avec QUIZ
            "id_quiz": quiz_data["id_quiz"],
            "score": round(
                random.uniform(0, 100),
                2
            ),
            "tentative": random.randint(1, 3),
            "date_passage": fake.date_time_between(
                start_date="-2y",
                end_date="now"
            ),
            "valide": random.choice([True, False])
        }
        notes.append(note)
    return notes

# =====================================================
# Génération de la progression
# Un étudiant suit plusieurs modules
def generate_progression(modules, cours):
    progressions = []
    deja_crees = set()
    while len(progressions) < NB_PROGRESSION:
        student_code = f"LMS-{random.randint(1, NB_ETUDIANTS):06d}"
        module = random.choice(modules)
        cle_unique = (
            student_code,
            module["id_module"]
        )
        # éviter doublon étudiant + module
        if cle_unique in deja_crees:
            continue
        deja_crees.add(cle_unique)
        cours_module = [
            c for c in cours
            if c["id_module"] == module["id_module"]
        ]
        cours_data = random.choice(cours_module)
        progression = {
            "id_progression": str(uuid.uuid4()),
            "student_code": student_code,
            "id_module": module["id_module"],
            "pourcentage": round(random.uniform(0,100),2),
            "dernier_cours": cours_data["id_cours"],
            "date_maj": datetime.now()
        }
        progressions.append(progression)
    return progressions

# =====================================================
# Génération des temps de connexion
# Historique d'activité des étudiants
def generate_connexions():
    connexions = []
    for i in range(1, NB_CONNEXIONS + 1):
        date_connexion = fake.date_time_between(
            start_date="-1y",
            end_date="now"
        )
        date_deconnexion = date_connexion + timedelta(
            minutes=random.randint(5,300)
        )
        connexion = {
            "id_connexion": str(uuid.uuid4()),
            "student_code": f"LMS-{random.randint(1, NB_ETUDIANTS):06d}",
            "date_connexion": date_connexion,
            "date_deconnexion": date_deconnexion,
            "duree_minutes": int((date_deconnexion - date_connexion).total_seconds()/60),
            "appareil":random.choice([
                "Mobile",
                "PC",
                "Tablette"
            ]),
            "navigateur":random.choice([
                "Chrome",
                "Firefox",
                "Edge",
                "Safari"
            ]),
            "adresse_ip":
            fake.ipv4()
        }
        connexions.append(connexion)
    return connexions 

#======================================================
#Export en csv
def export_csv(data, filename):
    with open(filename,"w",newline="",encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=data[0].keys()
        )
        writer.writeheader()
        writer.writerows(data)

#fonction d'execution
if __name__ == "__main__":
    modules = generate_modules()
    cours = generate_cours(modules)
    quiz = generate_quiz(cours)
    notes = generate_notes(quiz)
    progressions = generate_progression(
        modules,
        cours
    )
    connexions = generate_connexions()
    export_csv(modules, MODULES_FILE)
    export_csv(cours, COURS_FILE)
    export_csv(quiz, QUIZ_FILE)
    export_csv(notes, NOTES_FILE)
    export_csv(progressions, PROGRESSION_FILE)
    export_csv(connexions, CONNEXIONS_FILE)

    print("Modules :", len(modules))
    print("Cours :", len(cours))
    print("Quiz :", len(quiz))
    print("Notes :", len(notes))
    print("Progressions :", len(progressions))
    print("Connexions :", len(connexions))