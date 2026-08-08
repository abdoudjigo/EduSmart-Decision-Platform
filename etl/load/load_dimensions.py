"""
load_dimensions.py
==================

Chargement des dimensions du Data Warehouse edusmart_dw.

Sources utilisées :
- PostgreSQL : etudiants, filieres, classes
- MySQL      : modules, cours, quiz, notes, progression, temps_connexion
- CSV        : enseignants, departements
- MongoDB    : events

Important :
Les fichiers lus sont toujours ceux de :
etl/staging/clean/
"""

from datetime import datetime

from config import get_connection
from utils import read_clean_csv, to_pg_value


# ============================================================
# DIM TEMPS
# ============================================================

def load_dim_temps(cur):
    """
    Construit dim_temps à partir des dates réellement présentes
    dans les différentes sources.
    """

    dates = set()

    sources = [
        ("postgres", "inscriptions", "date_inscription"),
        ("postgres", "paiements", "date_paiement"),
        ("mysql", "notes", "date_passage"),
        ("mysql", "progression", "date_maj"),
        ("mysql", "temps_connexion", "date_connexion"),
        ("csv", "absences", "date_absence"),
        ("mongodb", "events", "timestamp"),
    ]

    for source, table, column in sources:

        try:
            df = read_clean_csv(source, table)
        except FileNotFoundError:
            print(f"[WARN] Fichier absent : {source}/{table}.csv")
            continue

        if column not in df.columns:
            print(
                f"[WARN] Colonne {column} absente de "
                f"{source}/{table}.csv"
            )
            continue

        for value in df[column].dropna():

            value = str(value)

            try:
                # Cas timestamp ISO
                date_value = datetime.fromisoformat(
                    value.replace("Z", "")
                ).date()

            except ValueError:

                try:
                    # Cas date simple YYYY-MM-DD
                    date_value = datetime.strptime(
                        value[:10],
                        "%Y-%m-%d"
                    ).date()

                except ValueError:
                    continue

            dates.add(date_value)

    # Salaires : mois + année
    try:
        df = read_clean_csv("csv", "salaires")

        for _, row in df.iterrows():

            try:
                annee = int(row["annee"])
                mois = int(row["mois"])

                dates.add(
                    datetime(
                        annee,
                        mois,
                        1
                    ).date()
                )

            except (ValueError, TypeError):
                continue

    except FileNotFoundError:
        print("[WARN] salaires.csv absent.")

    # Insertion
    for date_value in sorted(dates):

        cur.execute(
            """
            INSERT INTO dim_temps (
                date_complete,
                jour,
                mois,
                nom_mois,
                trimestre,
                annee,
                jour_semaine,
                week_end
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (date_complete) DO NOTHING
            """,
            (
                date_value,
                date_value.day,
                date_value.month,
                date_value.strftime("%B"),
                ((date_value.month - 1) // 3) + 1,
                date_value.year,
                date_value.strftime("%A"),
                date_value.weekday() >= 5,
            )
        )

    print(f"[OK] dim_temps : {len(dates)} dates.")


# ============================================================
# DIM ETUDIANT ACADEMIQUE
# ============================================================

def load_dim_etudiant_academique(cur):

    df = read_clean_csv(
        "postgres",
        "etudiants"
    )

    for _, row in df.iterrows():

        cur.execute(
            """
            INSERT INTO dim_etudiant_academique (
                matricule,
                prenom,
                nom,
                sexe,
                date_naissance,
                ville,
                pays,
                email
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (matricule) DO NOTHING
            """,
            (
                to_pg_value(row["matricule"]),
                to_pg_value(row["prenom"]),
                to_pg_value(row["nom"]),
                to_pg_value(row["sexe"]),
                to_pg_value(row["date_naissance"]),
                to_pg_value(row["ville"]),
                to_pg_value(row["pays"]),
                to_pg_value(row["email"]),
            )
        )

    print(
        f"[OK] dim_etudiant_academique : "
        f"{len(df)} lignes."
    )


# ============================================================
# DIM FILIERE
# ============================================================

def load_dim_filiere(cur):

    df = read_clean_csv(
        "postgres",
        "filieres"
    )

    for _, row in df.iterrows():

        cur.execute(
            """
            INSERT INTO dim_filiere (
                code_filiere,
                nom_filiere,
                niveau,
                duree
            )
            VALUES (%s,%s,%s,%s)
            ON CONFLICT (code_filiere) DO NOTHING
            """,
            (
                to_pg_value(row["code_filiere"]),
                to_pg_value(row["nom_filiere"]),
                to_pg_value(row["niveau"]),
                to_pg_value(row["duree_mois"]),
            )
        )

    print(
        f"[OK] dim_filiere : {len(df)} lignes."
    )


# ============================================================
# DIM CLASSE
# ============================================================

def load_dim_classe(cur):

    df = read_clean_csv(
        "postgres",
        "classes"
    )

    for _, row in df.iterrows():

        cur.execute(
            """
            INSERT INTO dim_classe (
                code_classe,
                nom_classe,
                capacite
            )
            VALUES (%s,%s,%s)
            ON CONFLICT (code_classe) DO NOTHING
            """,
            (
                to_pg_value(row["code_classe"]),
                to_pg_value(row["nom_classe"]),
                to_pg_value(row["capacite"]),
            )
        )

    print(
        f"[OK] dim_classe : {len(df)} lignes."
    )


# ============================================================
# DIM ETUDIANT LMS
# ============================================================

def load_dim_etudiant_lms(cur):

    codes = set()

    # Sources MySQL
    for table in [
        "notes",
        "progression",
        "temps_connexion"
    ]:

        try:
            df = read_clean_csv(
                "mysql",
                table
            )
        except FileNotFoundError:
            continue

        if "student_code" in df.columns:

            codes.update(
                df["student_code"]
                .dropna()
                .astype(str)
            )

    # Source MongoDB
    try:

        df = read_clean_csv(
            "mongodb",
            "events"
        )

        if "student_code" in df.columns:

            codes.update(
                df["student_code"]
                .dropna()
                .astype(str)
            )

    except FileNotFoundError:
        pass

    for code in sorted(codes):

        cur.execute(
            """
            INSERT INTO dim_etudiant_lms (
                student_code
            )
            VALUES (%s)
            ON CONFLICT (student_code) DO NOTHING
            """,
            (code,)
        )

    print(
        f"[OK] dim_etudiant_lms : "
        f"{len(codes)} étudiants LMS."
    )


# ============================================================
# DIM MODULE
# ============================================================

def load_dim_module(cur):

    df = read_clean_csv(
        "mysql",
        "modules"
    )

    for _, row in df.iterrows():

        cur.execute(
            """
            INSERT INTO dim_module (
                module_code,
                nom_module,
                categorie,
                niveau,
                duree_heures
            )
            VALUES (%s,%s,%s,%s,%s)
            ON CONFLICT (module_code) DO NOTHING
            """,
            (
                to_pg_value(row["code_module"]),
                to_pg_value(row["nom_module"]),
                to_pg_value(row["categorie"]),
                to_pg_value(row["niveau"]),
                to_pg_value(row["duree_heures"]),
            )
        )

    print(
        f"[OK] dim_module : {len(df)} lignes."
    )


# ============================================================
# DIM COURS
# ============================================================

def load_dim_cours(cur):

    df = read_clean_csv(
        "mysql",
        "cours"
    )

    for _, row in df.iterrows():

        cur.execute(
            """
            INSERT INTO dim_cours (
                id_cours_source,
                titre,
                type_cours,
                duree_minutes
            )
            VALUES (%s,%s,%s,%s)
            ON CONFLICT (id_cours_source) DO NOTHING
            """,
            (
                to_pg_value(row["id_cours"]),
                to_pg_value(row["titre"]),
                to_pg_value(row["type_cours"]),
                to_pg_value(row["duree_minutes"]),
            )
        )

    print(
        f"[OK] dim_cours : {len(df)} lignes."
    )


# ============================================================
# DIM QUIZ
# ============================================================

def load_dim_quiz(cur):

    df = read_clean_csv(
        "mysql",
        "quiz"
    )

    for _, row in df.iterrows():

        cur.execute(
            """
            INSERT INTO dim_quiz (
                id_quiz_source,
                titre,
                score_max
            )
            VALUES (%s,%s,%s)
            ON CONFLICT (id_quiz_source) DO NOTHING
            """,
            (
                to_pg_value(row["id_quiz"]),
                to_pg_value(row["titre"]),
                to_pg_value(row["score_max"]),
            )
        )

    print(
        f"[OK] dim_quiz : {len(df)} lignes."
    )


# ============================================================
# DIM ENSEIGNANT
# ============================================================

def load_dim_enseignant(cur):

    df = read_clean_csv(
        "csv",
        "enseignants"
    )

    for _, row in df.iterrows():

        cur.execute(
            """
            INSERT INTO dim_enseignant (
                matricule_enseignant,
                prenom,
                nom,
                grade
            )
            VALUES (%s,%s,%s,%s)
            ON CONFLICT (matricule_enseignant) DO NOTHING
            """,
            (
                to_pg_value(row["teacher_code"]),
                to_pg_value(row["prenom"]),
                to_pg_value(row["nom"]),
                to_pg_value(row["grade"]),
            )
        )

    print(
        f"[OK] dim_enseignant : {len(df)} lignes."
    )


# ============================================================
# DIM DEPARTEMENT
# ============================================================

def load_dim_departement(cur):

    df = read_clean_csv(
        "csv",
        "departements"
    )

    for _, row in df.iterrows():

        cur.execute(
            """
            INSERT INTO dim_departement (
                code_departement,
                nom_departement
            )
            VALUES (%s,%s)
            ON CONFLICT (code_departement) DO NOTHING
            """,
            (
                to_pg_value(row["id_departement"]),
                to_pg_value(row["nom_departement"]),
            )
        )

    print(
        f"[OK] dim_departement : {len(df)} lignes."
    )


# ============================================================
# DIM APPAREIL
# ============================================================

def load_dim_appareil(cur):

    combinations = set()

    # --------------------------------------------------------
    # MySQL temps_connexion
    # --------------------------------------------------------

    df = read_clean_csv(
        "mysql",
        "temps_connexion"
    )

    for _, row in df.iterrows():

        combinations.add(
            (
                to_pg_value(row["appareil"]),
                to_pg_value(row["navigateur"]),
                None,
                None,
            )
        )

    # --------------------------------------------------------
    # Mongo events
    # --------------------------------------------------------

    df = read_clean_csv(
        "mongodb",
        "events"
    )

    for _, row in df.iterrows():

        combinations.add(
            (
                to_pg_value(row["device"]),
                None,
                to_pg_value(row["operating_system"]),
                to_pg_value(row["app_version"]),
            )
        )

    for values in combinations:

        cur.execute(
            """
            INSERT INTO dim_appareil (
                type_appareil,
                navigateur,
                systeme_exploitation,
                version_application
            )
            VALUES (%s,%s,%s,%s)
            ON CONFLICT DO NOTHING
            """,
            values
        )

    print(
        f"[OK] dim_appareil : "
        f"{len(combinations)} combinaisons."
    )


# ============================================================
# MAIN
# ============================================================

def main():

    conn = get_connection()
    cur = conn.cursor()

    try:

        print("=" * 60)
        print("CHARGEMENT DES DIMENSIONS")
        print("=" * 60)

        load_dim_temps(cur)

        load_dim_etudiant_academique(cur)

        load_dim_filiere(cur)

        load_dim_classe(cur)

        load_dim_etudiant_lms(cur)

        load_dim_module(cur)

        load_dim_cours(cur)

        load_dim_quiz(cur)

        load_dim_enseignant(cur)

        load_dim_departement(cur)

        load_dim_appareil(cur)

        conn.commit()

        print("=" * 60)
        print("DIMENSIONS CHARGEES AVEC SUCCES")
        print("=" * 60)

    except Exception as e:

        conn.rollback()

        print("=" * 60)
        print("ERREUR CHARGEMENT DIMENSIONS")
        print("=" * 60)

        raise e

    finally:

        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
