"""
load_facts.py — Charge toutes les tables de faits du Data Warehouse.

À exécuter après load_dimensions.py. Chaque fait doit résoudre ses clés
étrangères (clés de substitution) à partir des clés métier présentes dans
les fichiers sources — d'où les nombreuses jointures/dictionnaires ici.

Stratégie de performance : on précharge chaque dimension nécessaire en
dictionnaire Python UNE FOIS, puis on résout chaque ligne en mémoire
(rapide), plutôt que de faire un SELECT SQL par ligne (beaucoup trop lent
à l'échelle de 100 000+ lignes).
"""

import pandas as pd
from datetime import date

from config import get_connection
from utils import read_clean_csv, to_pg_value


# ============================================================
# Helpers génériques
# ============================================================

def fetch_key_map(cur, table, key_column, natural_key_column):
    """
    Précharge une dimension entière en dictionnaire {clé_métier: clé_substitut}.
    Exemple : {"EDU000001": 1, "EDU000002": 2, ...}
    """
    cur.execute(f"SELECT {natural_key_column}, {key_column} FROM {table}")
    return {row[0]: row[1] for row in cur.fetchall()}


def fetch_appareil_map(cur):
    """
    dim_appareil a une clé composite (4 colonnes) -> le dictionnaire est
    indexé par un tuple. Les valeurs manquantes sont None ici (lues
    depuis la table), donc le tuple de recherche doit aussi utiliser None
    pour les mêmes positions — cohérence gérée dans chaque fonction
    fact_* ci-dessous.
    """
    cur.execute(
        "SELECT type_appareil, navigateur, systeme_exploitation, "
        "version_application, appareil_key FROM dim_appareil"
    )
    return {(r[0], r[1], r[2], r[3]): r[4] for r in cur.fetchall()}


def bulk_insert(cur, table, columns, rows):
    if not rows:
        print(f"  Aucune ligne à insérer pour {table}.")
        return
    col_names = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))
    cur.executemany(
        f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})", rows
    )
    print(f"  {table} : {len(rows)} lignes insérées.")


def to_date(value):
    """Convertit une valeur de date/datetime en objet date pur (pour
    correspondre à dim_temps.date_complete)."""
    if pd.isna(value):
        return None
    return pd.to_datetime(value).date()


# ============================================================
# fact_inscriptions — PostgreSQL
# ============================================================
# Chaîne de jointures nécessaire :
#   inscriptions.id_etudiant -> etudiants.matricule -> student_key
#   inscriptions.id_classe   -> classes.code_classe  -> classe_key
#   classes.id_filiere       -> filieres.code_filiere -> filiere_key
#   inscriptions.date_inscription -> time_key

def load_fact_inscriptions(cur):
    print("Chargement fact_inscriptions...")

    inscriptions = read_clean_csv("postgres", "inscriptions")
    etudiants = read_clean_csv("postgres", "etudiants")
    classes = read_clean_csv("postgres", "classes")

    # id_etudiant (UUID) -> matricule
    id_etudiant_to_matricule = dict(
        zip(etudiants["id_etudiant"], etudiants["matricule"])
    )
    # id_classe (UUID) -> code_classe, et id_classe -> id_filiere
    id_classe_to_code = dict(zip(classes["id_classe"], classes["code_classe"]))
    id_classe_to_id_filiere = dict(zip(classes["id_classe"], classes["id_filiere"]))

    filieres = read_clean_csv("postgres", "filieres")
    id_filiere_to_code = dict(zip(filieres["id_filiere"], filieres["code_filiere"]))

    student_key_map = fetch_key_map(cur, "dim_etudiant_academique", "student_key", "matricule")
    classe_key_map = fetch_key_map(cur, "dim_classe", "classe_key", "code_classe")
    filiere_key_map = fetch_key_map(cur, "dim_filiere", "filiere_key", "code_filiere")
    time_key_map = fetch_key_map(cur, "dim_temps", "time_key", "date_complete")

    rows = []
    skipped = 0

    for _, r in inscriptions.iterrows():
        matricule = id_etudiant_to_matricule.get(r["id_etudiant"])
        code_classe = id_classe_to_code.get(r["id_classe"])
        id_filiere = id_classe_to_id_filiere.get(r["id_classe"])
        code_filiere = id_filiere_to_code.get(id_filiere) if id_filiere else None

        student_key = student_key_map.get(matricule)
        classe_key = classe_key_map.get(code_classe)
        filiere_key = filiere_key_map.get(code_filiere)
        time_key = time_key_map.get(to_date(r["date_inscription"]))

        # On exige au minimum l'étudiant et la date pour garder la ligne.
        if student_key is None or time_key is None:
            skipped += 1
            continue

        rows.append((
            student_key,
            filiere_key,
            classe_key,
            time_key,
            to_pg_value(r["statut"]),
            to_pg_value(r["type_inscription"]),
            to_pg_value(r["bourse"]),
            to_pg_value(r["reduction"]),
        ))

    bulk_insert(
        cur,
        "fact_inscriptions",
        ["student_key", "filiere_key", "classe_key", "time_key",
         "statut", "type_inscription", "bourse", "reduction"],
        rows,
    )
    print(f"  Lignes ignorées (clé introuvable) : {skipped}")


# ============================================================
# fact_paiements — PostgreSQL
# ============================================================
# paiements.id_inscription -> inscriptions.id_etudiant -> matricule -> student_key

def load_fact_paiements(cur):
    print("Chargement fact_paiements...")

    paiements = read_clean_csv("postgres", "paiements")
    inscriptions = read_clean_csv("postgres", "inscriptions")
    etudiants = read_clean_csv("postgres", "etudiants")

    id_inscription_to_id_etudiant = dict(
        zip(inscriptions["id_inscription"], inscriptions["id_etudiant"])
    )
    id_etudiant_to_matricule = dict(
        zip(etudiants["id_etudiant"], etudiants["matricule"])
    )

    student_key_map = fetch_key_map(cur, "dim_etudiant_academique", "student_key", "matricule")
    time_key_map = fetch_key_map(cur, "dim_temps", "time_key", "date_complete")

    rows = []
    skipped = 0

    for _, r in paiements.iterrows():
        id_etudiant = id_inscription_to_id_etudiant.get(r["id_inscription"])
        matricule = id_etudiant_to_matricule.get(id_etudiant) if id_etudiant else None
        student_key = student_key_map.get(matricule)
        time_key = time_key_map.get(to_date(r["date_paiement"]))

        if student_key is None or time_key is None:
            skipped += 1
            continue

        rows.append((
            student_key,
            time_key,
            to_pg_value(r["montant"]),
            to_pg_value(r.get("reduction")),
        ))

    bulk_insert(
        cur,
        "fact_paiements",
        ["student_key", "time_key", "montant", "reduction"],
        rows,
    )
    print(f"  Lignes ignorées (clé introuvable) : {skipped}")


# ============================================================
# fact_notes — MySQL
# ============================================================
# notes.student_code -> student_lms_key
# notes.id_quiz -> dim_quiz.id_quiz_source -> quiz_key

def load_fact_notes(cur):
    print("Chargement fact_notes...")

    notes = read_clean_csv("mysql", "notes")

    student_key_map = fetch_key_map(cur, "dim_etudiant_lms", "student_lms_key", "student_code")
    quiz_key_map = fetch_key_map(cur, "dim_quiz", "quiz_key", "id_quiz_source")
    time_key_map = fetch_key_map(cur, "dim_temps", "time_key", "date_complete")

    rows = []
    skipped = 0

    for _, r in notes.iterrows():
        student_lms_key = student_key_map.get(r["student_code"])
        quiz_key = quiz_key_map.get(r["id_quiz"])
        time_key = time_key_map.get(to_date(r["date_passage"]))

        if student_lms_key is None or quiz_key is None or time_key is None:
            skipped += 1
            continue

        rows.append((
            student_lms_key,
            quiz_key,
            time_key,
            to_pg_value(r["score"]),
            to_pg_value(r["tentative"]),
            to_pg_value(r["valide"]),
        ))

    bulk_insert(
        cur,
        "fact_notes",
        ["student_lms_key", "quiz_key", "time_key", "score", "tentative", "valide"],
        rows,
    )
    print(f"  Lignes ignorées (clé introuvable) : {skipped}")


# ============================================================
# fact_progression — MySQL
# ============================================================
# progression.student_code -> student_lms_key
# progression.id_module -> modules.code_module -> module_key

def load_fact_progression(cur):
    print("Chargement fact_progression...")

    progression = read_clean_csv("mysql", "progression")
    modules = read_clean_csv("mysql", "modules")

    id_module_to_code = dict(zip(modules["id_module"], modules["code_module"]))

    student_key_map = fetch_key_map(cur, "dim_etudiant_lms", "student_lms_key", "student_code")
    module_key_map = fetch_key_map(cur, "dim_module", "module_key", "module_code")
    time_key_map = fetch_key_map(cur, "dim_temps", "time_key", "date_complete")

    rows = []
    skipped = 0

    for _, r in progression.iterrows():
        student_lms_key = student_key_map.get(r["student_code"])
        code_module = id_module_to_code.get(r["id_module"])
        module_key = module_key_map.get(code_module)
        time_key = time_key_map.get(to_date(r["date_maj"]))

        if student_lms_key is None or module_key is None or time_key is None:
            skipped += 1
            continue

        rows.append((
            student_lms_key,
            module_key,
            time_key,
            to_pg_value(r["pourcentage"]),
        ))

    bulk_insert(
        cur,
        "fact_progression",
        ["student_lms_key", "module_key", "time_key", "pourcentage"],
        rows,
    )
    print(f"  Lignes ignorées (clé introuvable) : {skipped}")


# ============================================================
# fact_connexions — MySQL
# ============================================================
# temps_connexion.student_code -> student_lms_key
# temps_connexion.(appareil, navigateur) -> dim_appareil (os/version = None,
# cohérent avec la façon dont dim_appareil a été peuplée depuis cette même
# source dans load_dimensions.py)

def load_fact_connexions(cur):
    print("Chargement fact_connexions...")

    connexions = read_clean_csv("mysql", "temps_connexion")

    student_key_map = fetch_key_map(cur, "dim_etudiant_lms", "student_lms_key", "student_code")
    appareil_map = fetch_appareil_map(cur)
    time_key_map = fetch_key_map(cur, "dim_temps", "time_key", "date_complete")

    rows = []
    skipped = 0

    for _, r in connexions.iterrows():
        student_lms_key = student_key_map.get(r["student_code"])
        appareil_key = appareil_map.get((
            to_pg_value(r.get("appareil")),
            to_pg_value(r.get("navigateur")),
            None,
            None,
        ))
        time_key = time_key_map.get(to_date(r["date_connexion"]))

        if student_lms_key is None or time_key is None:
            skipped += 1
            continue

        rows.append((
            student_lms_key,
            appareil_key,
            time_key,
            to_pg_value(r["duree_minutes"]),
        ))

    bulk_insert(
        cur,
        "fact_connexions",
        ["student_lms_key", "appareil_key", "time_key", "duree_minutes"],
        rows,
    )
    print(f"  Lignes ignorées (clé introuvable) : {skipped}")


# ============================================================
# fact_events — MongoDB
# ============================================================
# events.student_code -> student_lms_key
# events.(device, operating_system, app_version) -> dim_appareil
# (navigateur = None, cohérent avec load_dimensions.py)
# module_code / course_code : dimensions dégénérées, conservées en texte
# brut (aucun lien fiable avec dim_module / dim_cours, voir discussion).

def load_fact_events(cur):
    print("Chargement fact_events...")

    events = read_clean_csv("mongodb", "events")

    student_key_map = fetch_key_map(cur, "dim_etudiant_lms", "student_lms_key", "student_code")
    appareil_map = fetch_appareil_map(cur)
    time_key_map = fetch_key_map(cur, "dim_temps", "time_key", "date_complete")

    rows = []
    skipped = 0

    for _, r in events.iterrows():
        student_lms_key = student_key_map.get(r["student_code"])
        appareil_key = appareil_map.get((
            to_pg_value(r.get("device")),
            None,
            to_pg_value(r.get("operating_system")),
            to_pg_value(r.get("app_version")),
        ))
        time_key = time_key_map.get(to_date(r["timestamp"]))

        if student_lms_key is None or time_key is None:
            skipped += 1
            continue

        rows.append((
            student_lms_key,
            to_pg_value(r.get("module_code")),
            to_pg_value(r.get("course_code")),
            appareil_key,
            time_key,
            to_pg_value(r.get("duration_seconds")),
            to_pg_value(r.get("success")),
        ))

    bulk_insert(
        cur,
        "fact_events",
        ["student_lms_key", "module_code", "course_code", "appareil_key",
         "time_key", "duree_secondes", "succes"],
        rows,
    )
    print(f"  Lignes ignorées (clé introuvable) : {skipped}")


# ============================================================
# fact_absences — CSV RH
# ============================================================
# absences.teacher_code -> dim_enseignant.matricule_enseignant -> enseignant_key
# Pas de departement_key (lien inexistant dans les sources, cf. décision
# prise avec create_dw.py).

def load_fact_absences(cur):
    print("Chargement fact_absences...")

    absences = read_clean_csv("csv", "absences")

    enseignant_key_map = fetch_key_map(cur, "dim_enseignant", "enseignant_key", "matricule_enseignant")
    time_key_map = fetch_key_map(cur, "dim_temps", "time_key", "date_complete")

    rows = []
    skipped = 0

    for _, r in absences.iterrows():
        enseignant_key = enseignant_key_map.get(r["teacher_code"])
        time_key = time_key_map.get(to_date(r["date_absence"]))

        if enseignant_key is None or time_key is None:
            skipped += 1
            continue

        rows.append((
            enseignant_key,
            time_key,
            to_pg_value(r["duree_heures"]),
        ))

    bulk_insert(
        cur,
        "fact_absences",
        ["enseignant_key", "time_key", "duree_heures"],
        rows,
    )
    print(f"  Lignes ignorées (clé introuvable) : {skipped}")


# ============================================================
# fact_salaires — CSV RH
# ============================================================
# salaires.teacher_code -> enseignant_key
# salaires.(mois, annee) -> date(annee, mois, 1) -> time_key
# Anomalie connue (non nettoyée par transform.py) : salaire_base négatif
# -> lignes rejetées ici plutôt que de fausser les agrégats du DW.

def load_fact_salaires(cur):
    print("Chargement fact_salaires...")

    salaires = read_clean_csv("csv", "salaires")

    enseignant_key_map = fetch_key_map(cur, "dim_enseignant", "enseignant_key", "matricule_enseignant")
    time_key_map = fetch_key_map(cur, "dim_temps", "time_key", "date_complete")

    rows = []
    skipped = 0
    rejected_negative = 0

    for _, r in salaires.iterrows():
        enseignant_key = enseignant_key_map.get(r["teacher_code"])

        try:
            d = date(int(r["annee"]), int(r["mois"]), 1)
        except (ValueError, TypeError):
            skipped += 1
            continue

        time_key = time_key_map.get(d)

        if enseignant_key is None or time_key is None:
            skipped += 1
            continue

        salaire_base = to_pg_value(r["salaire_base"])
        if salaire_base is not None and salaire_base < 0:
            rejected_negative += 1
            continue

        rows.append((
            enseignant_key,
            time_key,
            salaire_base,
            to_pg_value(r["primes"]),
            to_pg_value(r["retenues"]),
            to_pg_value(r["salaire_net"]),
        ))

    bulk_insert(
        cur,
        "fact_salaires",
        ["enseignant_key", "time_key", "salaire_base", "primes", "retenues", "salaire_net"],
        rows,
    )
    print(f"  Lignes ignorées (clé introuvable) : {skipped}")
    print(f"  Lignes rejetées (salaire_base négatif, anomalie) : {rejected_negative}")


# ============================================================
# Orchestration
# ============================================================

if __name__ == "__main__":
    conn = get_connection()
    cur = conn.cursor()

    try:
        load_fact_inscriptions(cur)
        load_fact_paiements(cur)
        load_fact_notes(cur)
        load_fact_progression(cur)
        load_fact_connexions(cur)
        load_fact_events(cur)
        load_fact_absences(cur)
        load_fact_salaires(cur)

        conn.commit()
        print("=" * 60)
        print("Toutes les tables de faits ont été chargées.")
        print("=" * 60)

    except Exception as e:
        conn.rollback()
        print("=" * 60)
        print("ERREUR — chargement annulé (rollback).")
        print("=" * 60)
        raise e

    finally:
        cur.close()
        conn.close()