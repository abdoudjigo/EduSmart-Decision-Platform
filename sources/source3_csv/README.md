# Source 3 — Ressources Humaines (CSV)

## Description

Cette source représente les données du service Ressources Humaines exportées sous forme de fichiers CSV.

Elle contient les informations concernant :

- les enseignants ;
- les départements ;
- les salaires ;
- les absences.

Les fichiers sont générés automatiquement avec Python et Faker afin de simuler une source réelle utilisée par un système décisionnel.

---

## Fichiers générés

Les fichiers CSV générés sont :

### enseignants.csv

Contient les informations générales des enseignants :

- identifiant RH ;
- nom et prénom ;
- spécialité ;
- grade ;
- statut ;
- date d'embauche.

### departements.csv

Contient les informations des départements :

- nom du département ;
- responsable ;
- budget annuel ;
- bâtiment.

### salaires.csv

Contient l'historique des paiements :

- salaire de base ;
- primes ;
- retenues ;
- salaire net ;
- mode de paiement.

### absences.csv

Contient l'historique des absences :

- enseignant concerné ;
- date d'absence ;
- motif ;
- durée ;
- justification.

---

## Génération des données

Les données sont générées avec :

```bash
scripts/generate_data.py
```

Les fichiers générés sont stockés dans :

```text
generated_csv/
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
- formats incorrects ;
- catégories non standardisées ;
- erreurs de saisie ;
- incohérences métier.

Les fichiers contenant les anomalies sont stockés dans :

```text
generated_csv_anomalies/
```

---

## Technologies utilisées

- Python
- Faker
- CSV