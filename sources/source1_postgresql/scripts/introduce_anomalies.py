import pandas as pd
import random
import uuid



# =====================================================
# chemins données propres et donnees avec anomalies
DATA_PATH = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source1_postgresql/data/"
OUTPUT_PATH = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source1_postgresql/data_anomalies/"


ETUDIANTS_INPUT = DATA_PATH + "etudiants.csv"
FILIERES_INPUT = DATA_PATH + "filieres.csv"
CLASSES_INPUT = DATA_PATH + "classes.csv"
INSCRIPTIONS_INPUT = DATA_PATH + "inscriptions.csv"
PAIEMENTS_INPUT = DATA_PATH + "paiements.csv"


ETUDIANTS_OUTPUT = OUTPUT_PATH + "etudiants_anomalies.csv"
FILIERES_OUTPUT = OUTPUT_PATH + "filieres_anomalies.csv"
CLASSES_OUTPUT = OUTPUT_PATH + "classes_anomalies.csv"
INSCRIPTIONS_OUTPUT = OUTPUT_PATH + "inscriptions_anomalies.csv"
PAIEMENTS_OUTPUT = OUTPUT_PATH + "paiements_anomalies.csv"


# ============================
# étudiants
def anomalies_etudiants():
    # Charger les données propres
    df = pd.read_csv(ETUDIANTS_INPUT)
    print("Données originales :", len(df))

    # Valeurs manquantes
    # prévoir des valeurs manquantes téléphone/adresse
    nb_missing = int(len(df) * 0.05)  # 5% des étudiants
    lignes_missing = random.sample(
        list(df.index),
        nb_missing
    )
    for index in lignes_missing:
        df.loc[index, "telephone"] = None

    nb_missing_adresse = int(len(df) * 0.03)

    lignes_adresse = random.sample(
        list(df.index),
        nb_missing_adresse
    )

    for index in lignes_adresse:
        df.loc[index, "adresse"] = None

    # Sexe mal standardisé
    # M/F Homme/Femme Garçon/Fille 1/0
    nb_sexe = int(len(df) * 0.02)
    lignes_sexe = random.sample(
        list(df.index),
        nb_sexe
    )
    for index in lignes_sexe:
        valeur_actuelle = df.loc[index, "sexe"]
        if valeur_actuelle == "M":
            df.loc[index, "sexe"] = random.choice([
                "Homme",
                "Garçon",
                "1"
            ])
        else:
            df.loc[index, "sexe"] = random.choice([
                "Femme",
                "Fille",
                "0"
            ])
    
    # Doublons étudiants
    # On copie quelques étudiants existants
    nb_duplicates = 100
    doublons = df.sample(
        nb_duplicates,
        random_state=42
    )
    df = pd.concat(
        [
            df,
            doublons
        ],
        ignore_index=True
    )

    # =====================================================
    # Export
    df.to_csv(ETUDIANTS_OUTPUT, index=False, encoding="utf-8")
    print("Etudiants avec anomalies générés :", len(df))

# ============================
# filières
# ============================

def anomalies_filieres():

    df = pd.read_csv(FILIERES_INPUT)
    print("Filières originales :", len(df))

    # Catégories mal standardisées
    # IA Intelligence Artificielle Ingénierie IA
    # =====================================================
    nb_anomalies = int(len(df) * 0.30)  # 30% des filières
    lignes = random.sample(
        list(df.index),
        nb_anomalies
    )
    for index in lignes:
        nom = df.loc[index, "nom_filiere"]
        if "Intelligence" in nom or "IA" in nom:
            df.loc[index, "nom_filiere"] = random.choice([
                "IA",
                "Intelligence Artificielle",
                "Ingénierie IA"
            ])

    # Statut mal standardisé
    # ACTIVE / active / Actif
    # =====================================================
    nb_statut = int(len(df) * 0.20)
    lignes_statut = random.sample(
        list(df.index),
        nb_statut
    )
    for index in lignes_statut:
        if df.loc[index, "statut"] == "ACTIVE":
            df.loc[index, "statut"] = random.choice([
                "active",
                "Active",
                "Actif"
            ])
        else:
            df.loc[index, "statut"] = random.choice([
                "inactive",
                "Inactive",
                "Inactif"
            ])

     # Export
    # =====================================================
    df.to_csv(FILIERES_OUTPUT, index=False, encoding="utf-8")
    print("Filières avec anomalies générées :", len(df))

# ============================
# classes
# ============================

def anomalies_classes():
    df = pd.read_csv(CLASSES_INPUT)
    print("Classes originales :", len(df))

    # Salle mal standardisée
    # Salle A101, A101, A-101
    nb_salles = int(len(df) * 0.40)
    lignes = random.sample(
        list(df.index),
        nb_salles
    )
    for index in lignes:
        salle = df.loc[index, "salle"]
        if "A101" in salle or "Salle A101" in salle:
            df.loc[index, "salle"] = random.choice([
                "Salle A101",
                "A101",
                "A-101"
            ])
    
    # Responsable manquant
    nb_responsable = int(len(df) * 0.05)
    lignes_responsable = random.sample(
        list(df.index),
        nb_responsable
    )
    for index in lignes_responsable:
        df.loc[index, "responsable"] = None

    # Export
    df.to_csv(CLASSES_OUTPUT, index=False, encoding="utf-8")
    print("Classes avec anomalies générées :", len(df))

# ============================
# inscriptions
# ============================

def anomalies_inscriptions():
    df = pd.read_csv(INSCRIPTIONS_INPUT)
    print("Inscriptions originales :", len(df))
    
    # Réductions incorrectes
    #créduction > 100%
    nb_reduction = int(len(df) * 0.02)
    lignes_reduction = random.sample(
        list(df.index),
        nb_reduction
    )
    for index in lignes_reduction:
        df.loc[index, "reduction"] = random.choice([
            120,
            150,
            200
        ])

    # Dates incohérentes
    nb_dates = int(len(df) * 0.01)
    lignes_dates = random.sample(
        list(df.index),
        nb_dates
    )
    for index in lignes_dates:
        df.loc[index, "date_inscription"] = random.choice([
            "2030-01-15",
            "2035-06-20",
            "2040-09-01"
        ])

    # Doublons d'inscriptions
    nb_duplicates = 100
    doublons = df.sample(
        nb_duplicates,
        random_state=42
    )
    df = pd.concat(
        [
            df,
            doublons
        ],
        ignore_index=True
    )

    # Export
    df.to_csv(INSCRIPTIONS_OUTPUT, index=False, encoding="utf-8")
    print("Inscriptions avec anomalies générées :", len(df))

# ============================
# paiements
# ============================

def anomalies_paiements():
    df = pd.read_csv(PAIEMENTS_INPUT)
    print("Paiements originaux :", len(df))

    # Références dupliquées
    nb_duplicates = 100
    doublons = df.sample(
        nb_duplicates,
        random_state=42
    )
    df = pd.concat(
        [
            df,
            doublons
        ],
        ignore_index=True
    )

    # Montants négatifs
    nb_negatifs = int(len(df) * 0.02)
    lignes_negatives = random.sample(
        list(df.index),
        nb_negatifs
    )
    for index in lignes_negatives:
        df.loc[index, "montant"] = random.choice([
            -50000,
            -100000,
            -200000
        ])

    # Modes paiement non standardisés
    # OM Orange Money orange money
    nb_mode = int(len(df) * 0.05)
    lignes_mode = random.sample(
        list(df.index),
        nb_mode
    )
    for index in lignes_mode:
        df.loc[index, "mode_paiement"] = random.choice([
            "OM",
            "Orange Money",
            "orange money",
            "orangeMoney"
        ])

    # Paiements orphelins
    # id_inscription inexistante
    nb_orphelins = 50
    lignes_orphelins = random.sample(
        list(df.index),
        nb_orphelins
    )
    for index in lignes_orphelins:
        df.loc[index, "id_inscription"] = str(uuid.uuid4())

    # Export
    df.to_csv(PAIEMENTS_OUTPUT, index=False, encoding="utf-8")
    print("Paiements avec anomalies générés :", len(df))

if __name__ == "__main__":

    anomalies_etudiants()
    anomalies_filieres()
    anomalies_classes()
    anomalies_inscriptions()
    anomalies_paiements()

    print("Anomalies générées")