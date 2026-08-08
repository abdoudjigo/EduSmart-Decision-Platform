"""
config.py — Connexion centralisée au Data Warehouse edusmart_dw.

Logique Docker (identique à tout le reste du projet) :
- En local : POSTGRES_HOST retombe sur "localhost"
- Dans le conteneur etl (docker-compose) : POSTGRES_HOST = "postgres"
Aucune autre modification nécessaire entre les deux contextes.
"""

import os
import psycopg2

HOST = os.getenv("POSTGRES_HOST", "localhost")
PORT = int(os.getenv("POSTGRES_PORT", "5432"))
USER = os.getenv("POSTGRES_USER", "postgres")
PASSWORD = os.getenv("POSTGRES_PASSWORD", "5853500")
DW_DATABASE = os.getenv("POSTGRES_DW_DATABASE", "edusmart_dw")


def get_connection(dbname=None):
    """
    Ouvre une connexion à PostgreSQL.
    dbname=None -> se connecte à edusmart_dw (usage normal).
    dbname="postgres" -> se connecte à la base système (nécessaire uniquement
    pour CREATE DATABASE, qui ne peut pas s'exécuter depuis la base cible elle-même).
    """
    return psycopg2.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        dbname=dbname or DW_DATABASE,
    )