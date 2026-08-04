import os
import pandas as pd
from pandas import json_normalize

from utils import (
    remove_duplicates,
    remove_missing_values,
    count_missing_values,
)

from quality_report import save_quality_report


def transform_table(source, table):
    """
    Nettoie une table et génère :
    - le fichier propre (CSV)
    - le rapport qualité (JSON)
    """

    # ------------------------------------------------------------
    # 1) LECTURE DU FICHIER SOURCE (depuis staging/raw_anomalies)
    # ------------------------------------------------------------
    # Deux cas différents selon le format d'origine :
    # - MongoDB produit du JSON, avec des champs parfois imbriqués
    #   (ex: "metadata": {"score": 16, "attempt": 2})
    # - Les autres sources (postgres, mysql, csv) produisent du CSV classique.
    if source == "mongodb":
        input_file = f"etl/staging/raw_anomalies/{source}/{table}_anomalies.json"

        # pd.read_json charge le JSON tel quel : les champs imbriqués
        # (comme "metadata") restent des dictionnaires Python dans les cellules.
        df = pd.read_json(input_file)

        # json_normalize "aplatit" ces dictionnaires en colonnes séparées :
        # metadata.score, metadata.attempt, metadata.network, etc.
        # C'est INDISPENSABLE avant tout traitement pandas classique (doublons,
        # valeurs manquantes...), car pandas ne sait pas comparer des dict entre eux.
        df = pd.json_normalize(df.to_dict(orient="records"))

    elif source == "redis": 
        input_file = f"etl/staging/raw_anomalies/{source}/{table}_data_anomalies.json"
        df = pd.read_json(input_file)

    else:
        input_file = f"etl/staging/raw_anomalies/{source}/{table}_anomalies.csv"
        df = pd.read_csv(input_file)

    # ------------------------------------------------------------
    # ⚠️ CORRECTION IMPORTANTE :
    # L'ancien code relisait le fichier une deuxième fois ici avec
    # un nouveau bloc "if source == mongodb: df = pd.read_json(...)".
    # Ce deuxième bloc ÉCRASAIT le df déjà normalisé ci-dessus et
    # rechargeait le JSON brut, avec les dictionnaires imbriqués
    # encore intacts. C'est CA qui causait l'erreur
    # "TypeError: unhashable type: 'dict'" plus loin, au moment de
    # drop_duplicates() (impossible de comparer des dictionnaires).
    # Ce bloc en double a été supprimé — on ne lit le fichier
    # source qu'UNE seule fois, juste au-dessus.
    # ------------------------------------------------------------

    # ------------------------------------------------------------
    # 2) PRÉPARATION DU DOSSIER ET DU FICHIER DE SORTIE
    # ------------------------------------------------------------
    output_dir = f"etl/staging/clean/{source}"
    output_file = f"{output_dir}/{table}.csv"

    # Crée le dossier de sortie s'il n'existe pas encore
    # (exist_ok=True évite une erreur s'il existe déjà)
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print(f"Transformation : {table}")
    print("=" * 60)

    # ------------------------------------------------------------
    # 3) MESURE DE LA QUALITÉ "AVANT" NETTOYAGE
    # ------------------------------------------------------------
    # On garde ces chiffres pour comparer avant/après dans le rapport qualité.
    rows_before = len(df)
    missing_before = count_missing_values(df)

    # ------------------------------------------------------------
    # 4) NETTOYAGE : SUPPRESSION DES DOUBLONS
    # ------------------------------------------------------------
    df = remove_duplicates(df)
    duplicates_removed = rows_before - len(df)

    # ------------------------------------------------------------
    # 5) NETTOYAGE : GESTION DES VALEURS MANQUANTES
    # ------------------------------------------------------------
    df = remove_missing_values(df)

    rows_after = len(df)
    rejected_rows = rows_before - rows_after

    # ------------------------------------------------------------
    # 6) ÉCRITURE DU FICHIER PROPRE
    # ------------------------------------------------------------
    df.to_csv(output_file, index=False)
    print(f"Fichier propre créé : {output_file}")

    # ------------------------------------------------------------
    # 7) GÉNÉRATION DU RAPPORT QUALITÉ (traçabilité — voir Phase 5/6 du cours)
    # ------------------------------------------------------------
    stats = {
        "rows_before": int(rows_before),
        "rows_after": int(rows_after),
        "duplicates_removed": int(duplicates_removed),
        "missing_values_before": int(missing_before),
        "rejected_rows": int(rejected_rows),
    }

    save_quality_report(
        source=source,
        table=table,
        stats=stats,
    )

    print(f"Rapport qualité généré pour : {table}\n")


def normalize_mongodb(df):
    """
    Transforme les colonnes JSON imbriquées en colonnes simples.

    NOTE : cette fonction fait le même travail que le
    pd.json_normalize(...) déjà utilisé dans transform_table()
    pour la source mongodb. Elle n'est appelée nulle part dans le
    script actuellement — elle est gardée ici en réserve (utile si
    un jour un JSON a une structure plus complexe où json_normalize
    seul ne suffit pas), mais n'a aucun effet tant qu'elle n'est
    pas appelée explicitement.
    """
    for column in df.columns:
        # Vérifie si au moins une valeur de la colonne est un dictionnaire
        if df[column].apply(lambda x: isinstance(x, dict)).any():

            # Aplati cette colonne en plusieurs colonnes séparées
            expanded = pd.json_normalize(df[column])

            # Renomme les nouvelles colonnes pour garder une trace
            # de leur origine (ex: "metadata_score" plutôt que juste "score")
            expanded.columns = [
                f"{column}_{col}"
                for col in expanded.columns
            ]

            # Retire l'ancienne colonne (celle qui contenait les dict)
            df = df.drop(columns=[column])

            # Recolle le tableau original (sans la colonne dict)
            # avec les nouvelles colonnes aplaties
            df = pd.concat(
                [
                    df.reset_index(drop=True),
                    expanded.reset_index(drop=True)
                ],
                axis=1
            )

    return df


if __name__ == "__main__":

    # Dictionnaire : pour chaque source, la liste des tables/collections à transformer
    sources = {

        "postgres": [
            "etudiants",
            "filieres",
            "classes",
            "inscriptions",
            "paiements",
        ],

        "mysql": [
            "modules",
            "cours",
            "quiz",
            "progression",
            "notes",
            "temps_connexion",
        ],

        "csv": [
            "absences",
            "departements",
            "enseignants",
            "salaires",
        ],

        "mongodb": [
            "events",
        ],

        "redis": [
            "redis"
        ]

    }

    # Boucle principale : pour chaque source, pour chaque table, on transforme
    for source, tables in sources.items():

        print("=" * 60)
        print(f"Transformation source : {source}")
        print("=" * 60)

        for table in tables:
            transform_table(source, table)

    print("=" * 60)
    print("Transformation ETL terminée.")
    print("=" * 60)