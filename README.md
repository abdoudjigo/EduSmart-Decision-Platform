# EduSmart Decision Platform

## 📌 Présentation du projet

EduSmart Decision Platform est une plateforme décisionnelle complète permettant de centraliser, nettoyer et analyser les données provenant de plusieurs systèmes hétérogènes d'une plateforme d'apprentissage numérique.

Le projet simule un environnement réel d'entreprise où les données proviennent de plusieurs sources :

- Bases relationnelles PostgreSQL et MySQL ;
- Fichiers CSV provenant des ressources humaines ;
- Documents JSON MongoDB issus d'une application mobile ;
- Données temps réel stockées dans Redis.

L'objectif est de construire une architecture Data capable de :

- collecter les données depuis différentes sources ;
- détecter et gérer les anomalies ;
- préparer les données pour un processus ETL ;
- alimenter un Data Warehouse décisionnel ;
- produire des analyses et dashboards avec Power BI.


---

# 🏗️ Architecture générale du projet

```
EduSmart_Decision_Platform

│
├── sources
│   │
│   ├── source1_postgresql
│   │
│   ├── source2_mysql
│   │
│   ├── source3_csv
│   │
│   ├── source4_mongodb
│   │
│   └── source5_redis
│
├── etl
│
├── datawarehouse
│
├── powerbi
│
└── docs
```

Chaque source représente un système opérationnel différent.


---

# 📂 Structure globale

```
sources/

├── source1_postgresql
│   ├── data
│   ├── data_anomalies
│   ├── scripts
│   └── sql
│
├── source2_mysql
│   ├── data
│   ├── data_anomalies
│   ├── scripts
│   └── sql
│
├── source3_csv
│   ├── generated_csv
│   ├── generated_csv_anomalies
│   └── scripts
│
├── source4_mongodb
│   ├── json
│   ├── json_anomalies
│   └── scripts
│
└── source5_redis
    ├── data
    ├── data_anomalies
    └── scripts
```


---

# 🟦 Source 1 — PostgreSQL
## Gestion académique

## Description

Cette source représente le système académique principal de l'école.

Elle contient :

- les étudiants ;
- les filières ;
- les classes ;
- les inscriptions ;
- les paiements.


## Technologie

- PostgreSQL
- Python
- Faker


## Données générées

| Table | Nombre de lignes |
|-|-:|
| étudiants | 120 000 |
| filières | 20 |
| classes | 100 |
| inscriptions | 15 000 |
| paiements | 25 000 |


## Fichiers générés

```
source1_postgresql/

data/

├── etudiants.csv
├── filieres.csv
├── classes.csv
├── inscriptions.csv
└── paiements.csv
```


## Scripts

```
scripts/

├── generate_data.py
├── introduce_anomalies.py
└── insert_data.py
```


## Anomalies introduites

Le script `introduce_anomalies.py` simule des problèmes réels :

- valeurs manquantes ;
- doublons ;
- erreurs de saisie ;
- formats incohérents ;
- identifiants incompatibles ;
- données métier incorrectes.


---

# 🟩 Source 2 — MySQL
## Plateforme Learning Management System (LMS)


## Description

Cette source représente la plateforme pédagogique en ligne.

Elle contient :

- modules ;
- cours ;
- quiz ;
- résultats des étudiants ;
- progression ;
- temps de connexion.


## Technologie

- MySQL
- Python
- Faker


## Données générées


| Table | Nombre de lignes |
|-|-:|
| modules | 15 |
| cours | 300 |
| quiz | 900 |
| notes | 150 000 |
| progression | 120 000 |
| temps_connexion | 300 000 |


## Fichiers générés

```
source2_mysql/data/

├── modules.csv
├── cours.csv
├── quiz.csv
├── notes.csv
├── progression.csv
└── temps_connexion.csv
```


## Scripts

```
scripts/

├── generate_data.py
├── introduce_anomalies.py
└── insert_data.py
```


## Anomalies introduites

Exemples :

- catégories différentes :
  - Data
  - DATA
  - Data Science

- progressions :
  - supérieures à 100%
  - valeurs négatives

- connexions :
  - durée négative
  - IP invalides
  - appareils mal standardisés

- doublons de cours.


---

# 🟨 Source 3 — CSV
## Ressources Humaines


## Description

Le service RH exporte chaque mois des fichiers CSV.

Ces données concernent :

- enseignants ;
- départements ;
- salaires ;
- absences.


## Technologie

- CSV
- Python
- Faker


## Données générées


| Fichier | Nombre de lignes |
|-|-:|
| enseignants.csv | 5 000 |
| departements.csv | 30 |
| salaires.csv | 60 000 |
| absences.csv | 30 000 |


## Structure


```
source3_csv/

generated_csv/

├── enseignants.csv
├── departements.csv
├── salaires.csv
└── absences.csv
```


## Scripts

```
scripts/

├── generate_data.py
└── introduce_anomalies.py
```


## Anomalies introduites


- emails manquants ;
- téléphones incorrects ;
- spécialités différentes :
  - IA
  - Intelligence Artificielle
  - Data Science

- grades incohérents ;
- budgets absents ;
- dates avec plusieurs formats ;
- doublons.


---

# 🟥 Source 4 — MongoDB
## Journaux application mobile


## Description

Cette source représente les événements utilisateurs provenant de l'application mobile EduSmart.

Chaque document JSON représente une action utilisateur.


## Technologie

- MongoDB
- Docker
- Python
- Faker


## Collection

```
events
```


## Données générées


| Collection | Nombre |
|-|-:|
| events | 200 000 documents |
| events anomalies | 200 500 documents |


## Types d'événements


- LOGIN
- LOGOUT
- COURSE_OPENED
- VIDEO_STARTED
- VIDEO_FINISHED
- QUIZ_STARTED
- QUIZ_SUBMITTED
- RESOURCE_DOWNLOADED
- SEARCH
- PAYMENT_SUCCESS


## Particularité MongoDB

Les documents possèdent une structure flexible.

Certains événements contiennent :

```
quiz_code
score
attempt
```

D'autres contiennent :

```
video_quality
buffer_time
```


## Anomalies introduites


- documents incomplets ;
- champs absents ;
- valeurs nulles ;
- villes mal écrites :

```
Dakar
DAKAR
dakar
dakarr
```

- versions incohérentes :

```
2.4
2.4.0
v2.4
```

- IP invalides ;
- durées négatives ;
- doublons.


---

# 🟪 Source 5 — Redis
## Données temps réel


## Description

Cette source représente les données rapides utilisées par l'application :

- sessions utilisateurs ;
- statut connexion ;
- dernières activités.


## Technologie

- Redis
- Docker
- Python


## Données générées


| Élément | Nombre |
|-|-:|
| Clés Redis | 55 152 |


## Exemple de clé


```
session:LMS-006496
```


Valeur :

```json
{
"status":"online",
"last_activity":"2026-07-19 06:19",
"device":"Mobile"
}
```


## Scripts


```
scripts/

├── create_source.py
├── generate_data.py
├── introduce_anomalies.py
└── insert_data.py
```


## Anomalies introduites


- statuts incohérents ;
- appareils mal écrits ;
- sessions incomplètes ;
- valeurs manquantes ;
- formats différents.


---

# 🧪 Gestion des anomalies


Chaque source possède deux versions :

## Données propres

```
data/
generated_csv/
json/
```


## Données avec anomalies

```
data_anomalies/
generated_csv_anomalies/
json_anomalies/
```


Les anomalies permettent de reproduire un environnement Data réel avant nettoyage ETL.


---

# ⚙️ Technologies utilisées


| Domaine | Technologie |
|-|-|
| Langage | Python |
| Génération données | Faker |
| Base relationnelle | PostgreSQL |
| Base relationnelle | MySQL |
| Base documentaire | MongoDB |
| Cache temps réel | Redis |
| Conteneurisation | Docker |
| Visualisation | Power BI |
| ETL | Python / Data Pipeline |


---

# 🚀 Objectif final


Construire une plateforme décisionnelle capable de :

1. Extraire les données des différentes sources.

2. Nettoyer les anomalies.

3. Transformer les données.

4. Charger les données dans un Data Warehouse.

5. Produire des indicateurs décisionnels.


Exemples d'analyses :

- évolution des inscriptions ;
- performance académique ;
- activité des étudiants ;
- efficacité des enseignants ;
- utilisation de la plateforme ;
- statistiques RH.


---

# 👨‍💻 Auteur

Projet réalisé dans le cadre de la formation Data Engineering.

**EduSmart Decision Platform**
