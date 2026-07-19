# Source 5 — Redis (Clé-Valeur)

## Description

Cette source représente les données temps réel utilisées par la plateforme EduSmart.

Contrairement aux bases relationnelles et documentaires, Redis stocke les informations sous forme de paires **clé-valeur**.

Cette source permet de simuler :
- les sessions utilisateurs ;
- les états de connexion ;
- les informations temporaires utilisées par l'application.

Les données sont générées automatiquement avec Python.

---

## Structure des données

Les informations sont stockées sous forme de clés Redis.

Exemple :

```text
session:LMS-006496
```

Valeur associée :

```json
{
    "status": "online",
    "last_activity": "2026-07-19 06:19:37",
    "device": "Mobile"
}
```

---

## Génération des données

Les données sont générées avec :

```bash
scripts/generate_data.py
```

Le fichier généré est :

```text
data/redis_data.json
```

Il contient les informations simulant les sessions des étudiants.

---

## Insertion dans Redis

Redis est exécuté avec Docker.

L'insertion des données est réalisée avec :

```bash
scripts/insert_data.py
```

Les données sont chargées dans Redis sous forme de clés :

```text
session:LMS-xxxx
```

---

## Introduction des anomalies

Un second script permet de simuler des problèmes réels de qualité des données :

```bash
scripts/introduce_anomalies.py
```

Les anomalies introduites comprennent :

- valeurs manquantes ;
- valeurs nulles ;
- statuts incohérents ;
- appareils mal standardisés ;
- formats différents.

Les fichiers contenant les anomalies sont stockés dans :

```text
data_anomalies/
```

---

## Technologies utilisées

- Python
- Faker
- Redis
- Docker