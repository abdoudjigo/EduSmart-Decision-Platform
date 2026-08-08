"""
utils.py — Fonctions communes à load_dimensions.py et load_facts.py.
"""

import pandas as pd
import numpy as np


def read_clean_csv(source, table):
    """
    Lit un fichier propre depuis etl/staging/clean/{source}/{table}.csv
    Retourne un DataFrame pandas.
    """
    path = f"etl/staging/clean/{source}/{table}.csv"
    return pd.read_csv(path)


def to_pg_value(value):
    """
    Convertit une valeur pandas/numpy (NaN, np.int64, np.bool_...) en une
    valeur que psycopg2 sait insérer telle quelle. Sans ça, un NaN pandas
    provoque une erreur d'insertion silencieusement incorrecte (il doit
    devenir un vrai None Python -> NULL en SQL).
    """
    if pd.isna(value):
        return None
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    return value


def get_or_create_key(cur, table, key_column, natural_key_columns, values, cache):
    """
    Retourne la clé de substitution (surrogate key) correspondant à une
    combinaison de valeurs de clé métier (natural key), en la créant si
    elle n'existe pas encore.

    - table : nom de la table dimension (ex: "dim_appareil")
    - key_column : nom de la colonne clé de substitution (ex: "appareil_key")
    - natural_key_columns : liste des colonnes formant la clé métier
      (ex: ["type_appareil", "navigateur", "systeme_exploitation", "version_application"])
    - values : dict complet des colonnes à insérer si la ligne n'existe pas
    - cache : dict Python passé par l'appelant, pour éviter une requête SQL
      à chaque ligne (les mêmes combinaisons reviennent des milliers de fois
      dans fact_connexions/fact_events)

    Pourquoi ce mécanisme : une table de faits ne référence jamais les
    valeurs métier directement (ex: "Chrome", "Android") — elle référence
    la clé de substitution générée par la dimension. Ce helper fait le
    lien "valeur métier -> clé de substitution" une seule fois par
    combinaison unique, grâce au cache.
    """
    natural_key = tuple(to_pg_value(values[col]) for col in natural_key_columns)

    if natural_key in cache:
        return cache[natural_key]

    where_clause = " AND ".join(
        f"{col} IS NOT DISTINCT FROM %s" for col in natural_key_columns
    )
    cur.execute(
        f"SELECT {key_column} FROM {table} WHERE {where_clause}",
        natural_key,
    )
    row = cur.fetchone()

    if row:
        key = row[0]
    else:
        columns = list(values.keys())
        placeholders = ", ".join(["%s"] * len(columns))
        col_names = ", ".join(columns)
        insert_values = tuple(to_pg_value(values[col]) for col in columns)

        cur.execute(
            f"INSERT INTO {table} ({col_names}) VALUES ({placeholders}) "
            f"ON CONFLICT DO NOTHING RETURNING {key_column}",
            insert_values,
        )
        row = cur.fetchone()

        if row:
            key = row[0]
        else:
            # Cas rare : conflit géré par ON CONFLICT DO NOTHING mais la ligne
            # a été insérée entre-temps (peu probable ici, pipeline séquentiel,
            # mais on sécurise plutôt qu'on suppose).
            cur.execute(
                f"SELECT {key_column} FROM {table} WHERE {where_clause}",
                natural_key,
            )
            key = cur.fetchone()[0]

    cache[natural_key] = key
    return key