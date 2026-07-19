# Source 2 — MySQL (Plateforme d'apprentissage)

## Description

Cette source représente la base de données de la plateforme d'apprentissage en ligne EduSmart.

Elle enregistre les informations liées :

- aux modules ;
- aux cours ;
- aux quiz ;
- aux résultats des étudiants ;
- à la progression des apprenants ;
- aux temps de connexion.

La base est générée automatiquement avec Python et stockée dans MySQL afin de simuler une source réelle utilisée par un système décisionnel.

---

## Structure de la base

La base utilisée est :

```text
edusmart_learning
```

Les principales tables sont :

### modules

Contient les informations des modules de formation :

- code du module ;
- nom ;
- catégorie ;
- niveau ;
- durée ;
- état actif.

### cours

Contient les cours associés aux modules :

- titre ;
- ordre ;
- durée ;
- type de cours ;
- statut.

### quiz

Contient les évaluations associées aux cours :

- nombre de questions ;
- score maximal ;
- durée.

### notes

Contient les résultats des étudiants :

- quiz effectué ;
- étudiant concerné ;
- score ;
- tentative ;
- validation.

### progression

Contient le suivi de l'avancement des étudiants :

- module suivi ;
- pourcentage de progression ;
- dernier cours consulté ;
- date de mise à jour.

### temps_connexion

Contient l'historique d'activité :

- connexion ;
- déconnexion ;
- durée ;
- appareil ;
- navigateur ;
- adresse IP.

---

## Génération des données

Les données sont générées avec :

```bash
scripts/generate_data.py
```

Les fichiers CSV générés sont stockés dans :

```text
data/
```

Ils sont ensuite utilisés pour alimenter la base MySQL.

---

## Insertion dans MySQL

L'insertion des données est réalisée avec :

```bash
scripts/insert_data.py
```

La connexion utilise MySQL afin de charger les fichiers CSV dans les différentes tables de la base :

```text
edusmart_learning
```

---

## Introduction des anomalies

Un second script permet de simuler des problèmes réels de qualité des données :

```bash
scripts/introduce_anomalies.py
```

Les anomalies introduites comprennent :

- valeurs manquantes ;
- doublons ;
- catégories non standardisées ;
- erreurs de saisie ;
- progressions supérieures à 100 % ;
- valeurs négatives ;
- connexions incomplètes ;
- incohérences métier.

Les fichiers contenant les anomalies sont stockés dans :

```text
data_anomalies/
```

---

## Technologies utilisées

- Python
- Faker
- MySQL
- CSV