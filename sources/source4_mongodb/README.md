# Source 4 — MongoDB (Documents JSON)

## Description

Cette source représente les journaux d'activité de l'application mobile EduSmart.

Contrairement aux bases relationnelles, les données sont stockées sous forme de documents JSON dans MongoDB.

Chaque document représente un événement réalisé par un utilisateur :
- connexion ;
- consultation de cours ;
- passage de quiz ;
- téléchargement de ressources ;
- actions sur l'application.

Ces données permettent d'analyser :
- le comportement des étudiants ;
- l'utilisation de la plateforme ;
- les habitudes d'apprentissage ;
- les performances des formations.

---

## Structure

La collection principale utilisée est :

### events

Elle contient les événements utilisateurs avec :

- identifiant événement ;
- étudiant concerné ;
- date et heure ;
- type d'événement ;
- module et cours associés ;
- appareil utilisé ;
- système d'exploitation ;
- informations réseau ;
- durée ;
- statut de réussite ;
- métadonnées complémentaires.

MongoDB permet une structure flexible : tous les documents ne possèdent pas obligatoirement les mêmes champs.

Exemple :
- un événement `LOGIN` ne contient pas forcément de quiz ;
- un événement `QUIZ_SUBMITTED` peut contenir un score et une tentative ;
- un événement `VIDEO_STARTED` peut contenir des informations sur la qualité vidéo.

---

## Génération des données

Les données sont générées automatiquement avec Python et Faker.

Script utilisé :

```bash
scripts/generate_data.py
```

Le volume généré est d'environ :

- 200 000 événements utilisateurs.

Les fichiers JSON sont stockés dans :

```
json/
```

---

## Insertion MongoDB

Les documents JSON générés sont insérés dans une base MongoDB.

Script utilisé :

```bash
scripts/insert_data.py
```

La collection utilisée est :

```
events
```

---

## Introduction des anomalies

Un second script permet de simuler des problèmes réels de qualité des données :

```bash
scripts/introduce_anomalies.py
```

Les anomalies introduites comprennent :

- documents incomplets ;
- champs manquants ;
- valeurs nulles ;
- villes non standardisées ;
- versions d'application incohérentes ;
- systèmes d'exploitation mal formatés ;
- dates et formats différents ;
- événements dupliqués ;
- adresses IP invalides ;
- durées négatives ;
- événements sans identifiant étudiant.

Les fichiers contenant les anomalies sont stockés dans :

```
json_anomalies/
```

---

## Technologies utilisées

- Python
- Faker
- MongoDB
- Documents JSON