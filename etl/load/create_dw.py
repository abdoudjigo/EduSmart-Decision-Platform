"""
create_dw.py — Création de la base edusmart_dw et de son schéma en étoile.
"""

from psycopg2 import sql
from config import get_connection, DW_DATABASE


def create_database_if_not_exists():
    # NOTE : on doit se connecter à la base système "postgres" pour créer
    # edusmart_dw — impossible de faire CREATE DATABASE depuis la base cible.
    conn = get_connection(dbname="postgres")
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DW_DATABASE,))
    exists = cur.fetchone()

    if exists:
        print(f"Base '{DW_DATABASE}' déjà existante — pas de recréation.")
    else:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DW_DATABASE)))
        print(f"Base '{DW_DATABASE}' créée.")

    cur.close()
    conn.close()


SCHEMA_SQL = """
-- ============================================================
-- DIMENSIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_temps (
    time_key SERIAL PRIMARY KEY,
    date_complete DATE UNIQUE NOT NULL,
    jour INT NOT NULL,
    mois INT NOT NULL,
    nom_mois VARCHAR(20) NOT NULL,
    trimestre INT NOT NULL,
    annee INT NOT NULL,
    jour_semaine VARCHAR(20) NOT NULL,
    week_end BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_etudiant_academique (
    student_key SERIAL PRIMARY KEY,
    matricule VARCHAR(20) UNIQUE NOT NULL,
    prenom VARCHAR(100),
    nom VARCHAR(100),
    sexe CHAR(1),
    date_naissance DATE,
    ville VARCHAR(100),
    pays VARCHAR(100),
    email VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS dim_filiere (
    filiere_key SERIAL PRIMARY KEY,
    code_filiere VARCHAR(20) UNIQUE NOT NULL,
    nom_filiere VARCHAR(150),
    niveau VARCHAR(50),
    duree INT
);

CREATE TABLE IF NOT EXISTS dim_classe (
    classe_key SERIAL PRIMARY KEY,
    code_classe VARCHAR(20) UNIQUE NOT NULL,
    nom_classe VARCHAR(100),
    capacite INT
);

CREATE TABLE IF NOT EXISTS dim_etudiant_lms (
    student_lms_key SERIAL PRIMARY KEY,
    student_code VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_module (
    module_key SERIAL PRIMARY KEY,
    module_code VARCHAR(20) UNIQUE NOT NULL,
    nom_module VARCHAR(150),
    categorie VARCHAR(100),
    niveau VARCHAR(50),
    duree_heures INT
);

CREATE TABLE IF NOT EXISTS dim_cours (
    cours_key SERIAL PRIMARY KEY,
    id_cours_source VARCHAR(40) UNIQUE NOT NULL,
    titre VARCHAR(200),
    type_cours VARCHAR(50),
    duree_minutes INT
);

CREATE TABLE IF NOT EXISTS dim_quiz (
    quiz_key SERIAL PRIMARY KEY,
    id_quiz_source VARCHAR(40) UNIQUE NOT NULL,
    titre VARCHAR(200),
    score_max NUMERIC(5,2)
);

CREATE TABLE IF NOT EXISTS dim_enseignant (
    enseignant_key SERIAL PRIMARY KEY,
    matricule_enseignant VARCHAR(20) UNIQUE NOT NULL,
    prenom VARCHAR(100),
    nom VARCHAR(100),
    grade VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_departement (
    departement_key SERIAL PRIMARY KEY,
    code_departement VARCHAR(20) UNIQUE NOT NULL,
    nom_departement VARCHAR(100)
);

-- dim_appareil : dimension reconstituée à partir de combinaisons observées
-- (MySQL temps_connexion, Mongo events). Aucune source ne fournit de code
-- métier pour un appareil -> la clé unique est la combinaison des 4 attributs.
CREATE TABLE IF NOT EXISTS dim_appareil (
    appareil_key SERIAL PRIMARY KEY,
    type_appareil VARCHAR(50),
    navigateur VARCHAR(50),
    systeme_exploitation VARCHAR(50),
    version_application VARCHAR(30),
    UNIQUE (type_appareil, navigateur, systeme_exploitation, version_application)
);

-- ============================================================
-- FAITS
-- ============================================================

-- montant_inscription retiré : aucune source ne fournit de montant au
-- niveau de l'inscription (le montant réel n'existe que dans paiements,
-- via fact_paiements). Colonnes remplacées par ce que inscriptions.csv
-- fournit réellement.
CREATE TABLE IF NOT EXISTS fact_inscriptions (
    fact_id BIGSERIAL PRIMARY KEY,
    student_key INT REFERENCES dim_etudiant_academique(student_key),
    filiere_key INT REFERENCES dim_filiere(filiere_key),
    classe_key INT REFERENCES dim_classe(classe_key),
    time_key INT REFERENCES dim_temps(time_key),
    statut VARCHAR(30),
    type_inscription VARCHAR(30),
    bourse BOOLEAN,
    reduction NUMERIC(5,2)
);

CREATE TABLE IF NOT EXISTS fact_paiements (
    fact_id BIGSERIAL PRIMARY KEY,
    student_key INT REFERENCES dim_etudiant_academique(student_key),
    time_key INT REFERENCES dim_temps(time_key),
    montant NUMERIC(12,2),
    reduction NUMERIC(5,2)
);

CREATE TABLE IF NOT EXISTS fact_notes (
    fact_id BIGSERIAL PRIMARY KEY,
    student_lms_key INT REFERENCES dim_etudiant_lms(student_lms_key),
    quiz_key INT REFERENCES dim_quiz(quiz_key),
    time_key INT REFERENCES dim_temps(time_key),
    score NUMERIC(5,2),
    tentative INT,
    valide BOOLEAN
);

CREATE TABLE IF NOT EXISTS fact_progression (
    fact_id BIGSERIAL PRIMARY KEY,
    student_lms_key INT REFERENCES dim_etudiant_lms(student_lms_key),
    module_key INT REFERENCES dim_module(module_key),
    time_key INT REFERENCES dim_temps(time_key),
    pourcentage NUMERIC(5,2)
);

CREATE TABLE IF NOT EXISTS fact_connexions (
    fact_id BIGSERIAL PRIMARY KEY,
    student_lms_key INT REFERENCES dim_etudiant_lms(student_lms_key),
    appareil_key INT REFERENCES dim_appareil(appareil_key),
    time_key INT REFERENCES dim_temps(time_key),
    duree_minutes INT
);

-- module_code / course_code générés indépendamment par Faker côté Mongo
-- (random.randint sans lien avec MySQL) -> aucune correspondance réelle
-- avec dim_module / dim_cours. Conservés en dimensions dégénérées (texte
-- brut dans le fait) plutôt que rattachés à une dimension inexistante.
CREATE TABLE IF NOT EXISTS fact_events (
    fact_id BIGSERIAL PRIMARY KEY,
    student_lms_key INT REFERENCES dim_etudiant_lms(student_lms_key),
    module_code VARCHAR(20),
    course_code VARCHAR(20),
    appareil_key INT REFERENCES dim_appareil(appareil_key),
    time_key INT REFERENCES dim_temps(time_key),
    duree_secondes INT,
    succes BOOLEAN
);

-- nombre_jours -> duree_heures : absences.csv fournit une durée en heures,
-- pas un nombre de jours.
-- nombre_jours -> duree_heures : absences.csv fournit une durée en heures,
-- pas un nombre de jours. departement_key retiré : enseignants.csv ne
-- contient aucune référence à un département, ce lien n'existe dans
-- aucune source du projet (silo confirmé, pas un oubli de modélisation).
CREATE TABLE IF NOT EXISTS fact_absences (
    fact_id BIGSERIAL PRIMARY KEY,
    enseignant_key INT REFERENCES dim_enseignant(enseignant_key),
    time_key INT REFERENCES dim_temps(time_key),
    duree_heures INT
);

-- departement_key retiré : même constat que fact_absences, aucune source
-- ne relie un enseignant à un département.
CREATE TABLE IF NOT EXISTS fact_salaires (
    fact_id BIGSERIAL PRIMARY KEY,
    enseignant_key INT REFERENCES dim_enseignant(enseignant_key),
    time_key INT REFERENCES dim_temps(time_key),
    salaire_base NUMERIC(12,2),
    primes NUMERIC(12,2),
    retenues NUMERIC(12,2),
    salaire_net NUMERIC(12,2)
);

-- OPTIONNELLE — Redis étant un état temps réel (pas un historique), sa
-- valeur décisionnelle est limitée. Décommenter si un usage est identifié.
--
-- CREATE TABLE IF NOT EXISTS fact_sessions (
--     fact_id BIGSERIAL PRIMARY KEY,
--     student_lms_key INT REFERENCES dim_etudiant_lms(student_lms_key),
--     appareil_key INT REFERENCES dim_appareil(appareil_key),
--     time_key INT REFERENCES dim_temps(time_key),
--     statut VARCHAR(20)
-- );
"""


def create_schema():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(SCHEMA_SQL)
    conn.commit()
    cur.close()
    conn.close()
    print("Schéma edusmart_dw créé (dimensions + faits).")


if __name__ == "__main__":
    create_database_if_not_exists()
    create_schema()
    print("=" * 60)
    print("Data Warehouse edusmart_dw prêt.")
    print("=" * 60)