Voici une version complète, propre et professionnelle de ton `README.md` pour **source1_postgresql** :

````md
# Source 1 - PostgreSQL : Gestion Académique

## Présentation

Cette source représente le système opérationnel de gestion académique de la plateforme **EduSmart**.

Elle simule une base de données PostgreSQL nommée :

```text
edusmart_academic
```

Cette base contient les informations liées au parcours académique des étudiants :

- étudiants ;
- filières ;
- classes ;
- inscriptions ;
- paiements.

L'objectif est de reproduire un environnement proche d'un système d'information réel afin de servir de source pour une future plateforme décisionnelle.

Les données ont été générées automatiquement avec **Python et Faker**.

Deux versions des données sont disponibles :

- une version propre respectant les contraintes métier ;
- une version contenant volontairement des anomalies afin de tester les étapes de nettoyage, transformation et intégration des données.


---

# Structure du projet

```text
source1_postgresql/
│
├── data/
│   ├── etudiants.csv
│   ├── filieres.csv
│   ├── classes.csv
│   ├── inscriptions.csv
│   └── paiements.csv
│
├── data_anomalies/
│   ├── etudiants_anomalies.csv
│   ├── filieres_anomalies.csv
│   ├── classes_anomalies.csv
│   ├── inscriptions_anomalies.csv
│   └── paiements_anomalies.csv
│
├── scripts/
│   ├── generate_data.py
│   ├── introduce_anomalies.py
│   └── insert_data.py
│
├── sql/
│   └── create_database.sql
│
└── README.md
```


---

# Description des dossiers et fichiers

## data/

Ce dossier contient les données générées initialement sans anomalies.

Chaque fichier correspond à une table PostgreSQL :

| Fichier | Description |
|---|---|
| etudiants.csv | Informations personnelles des étudiants |
| filieres.csv | Formations proposées par l'établissement |
| classes.csv | Classes rattachées aux filières |
| inscriptions.csv | Associations entre étudiants et classes |
| paiements.csv | Historique des paiements étudiants |


---

## data_anomalies/

Ce dossier contient une copie des données avec des anomalies volontairement introduites.

Ces données simulent les problèmes que l'on retrouve dans les systèmes d'information réels avant un processus ETL.

Exemples :

- valeurs manquantes ;
- doublons ;
- erreurs de saisie ;
- catégories non standardisées ;
- incohérences métier ;
- références inexistantes.


---

## scripts/

### generate_data.py

Script Python permettant de générer automatiquement les données de la source PostgreSQL.

Il utilise :

- Faker pour générer des données réalistes ;
- UUID pour les identifiants techniques ;
- random pour certaines valeurs aléatoires.


### introduce_anomalies.py

Script permettant d'ajouter volontairement des anomalies dans les données générées.

Son objectif est de reproduire des problèmes réels rencontrés lors des projets Data Engineering.


### insert_data.py

Script Python utilisant `psycopg` afin d'insérer les fichiers CSV générés dans la base PostgreSQL.

Processus :

```text
CSV
 |
 |
 v
Lecture Python
 |
 |
 v
INSERT PostgreSQL
 |
 |
 v
Base edusmart_academic
```


---

# Modèle relationnel

La base repose sur cinq tables principales :

```text
                 FILIERES
                    |
                    |
                    | 1,N
                    |
                 CLASSES
                    |
                    |
                    | 1,N
                    |
              INSCRIPTIONS
              /          \
             /            \
            /              \
           N                N
     ETUDIANTS          PAIEMENTS
```


---

# Relations entre les tables

## Filières → Classes

Une filière peut contenir plusieurs classes.

Relation :

```text
Une filière possède plusieurs classes
```

Clé étrangère :

```sql
classes.id_filiere
        |
        v
filieres.id_filiere
```


---

## Étudiants → Inscriptions

Un étudiant peut avoir plusieurs inscriptions au cours de son parcours.

Relation :

```text
Un étudiant possède plusieurs inscriptions
```

Clé étrangère :

```sql
inscriptions.id_etudiant
        |
        v
etudiants.id_etudiant
```


---

## Classes → Inscriptions

Une classe peut contenir plusieurs inscriptions.

Relation :

```text
Une classe possède plusieurs étudiants inscrits
```

Clé étrangère :

```sql
inscriptions.id_classe
        |
        v
classes.id_classe
```


---

## Inscriptions → Paiements

Un paiement est obligatoirement lié à une inscription.

Relation :

```text
Une inscription peut avoir plusieurs paiements
```

Clé étrangère :

```sql
paiements.id_inscription
        |
        v
inscriptions.id_inscription
```


---

# Contraintes mises en place

## Clés primaires

Chaque table possède un identifiant unique :

- id_etudiant ;
- id_filiere ;
- id_classe ;
- id_inscription ;
- id_paiement.


---

## Clés étrangères

Les relations sont assurées par :

- classes → filieres ;
- inscriptions → etudiants ;
- inscriptions → classes ;
- paiements → inscriptions.


---

## Contraintes métier

Plusieurs règles garantissent la cohérence des données :

- matricule étudiant unique ;
- email étudiant unique ;
- sexe limité aux valeurs M et F ;
- date de naissance antérieure à la date actuelle ;
- durée des formations supérieure à zéro ;
- montant des paiements positif ;
- réduction comprise entre 0 et 100 % ;
- références de paiement uniques.


---

# Anomalies introduites volontairement

Afin de simuler un environnement réel, plusieurs problèmes ont été ajoutés.


## Valeurs manquantes

Exemples :

- téléphone absent ;
- adresse inexistante ;
- informations non renseignées.


---

## Doublons

Ajout d'enregistrements identiques ou similaires.

Exemples :

- étudiants dupliqués ;
- inscriptions répétées ;
- références de paiement identiques.


---

## Formats différents

Exemples :

Sexe :

```text
M
F
Homme
Femme
1
0
```

Salle :

```text
A101
Salle A101
A-101
```

Mode paiement :

```text
OM
Orange Money
orange money
```


---

## Valeurs incohérentes

Exemples :

- réduction supérieure à 100 % ;
- montants négatifs ;
- dates d'inscription dans le futur ;
- catégories mal écrites.


---

## Enregistrements orphelins

Certaines données possèdent des références inexistantes.

Exemple :

```text
paiement
    |
    id_inscription
    |
    X inscription inexistante
```

Ces anomalies permettront de tester les contrôles d'intégrité pendant le processus ETL.


---

# Volume des données générées

| Table | Nombre de lignes |
|---|---:|
| étudiants | 120 000 |
| filières | 20 |
| classes | 100 |
| inscriptions | 15 000 |
| paiements | 25 000 |


Ces volumes permettent de tester :

- les performances SQL ;
- les opérations de nettoyage ;
- les traitements ETL ;
- la préparation des données décisionnelles.


---

# Technologies utilisées

| Technologie | Utilisation |
|---|---|
| PostgreSQL | Base de données source |
| Python | Génération et insertion des données |
| Faker | Création de données réalistes |
| Pandas | Manipulation et création des anomalies |
| Psycopg | Connexion Python/PostgreSQL |


---

# Conclusion

La source PostgreSQL `edusmart_academic` représente le système académique opérationnel d'EduSmart.

Elle contient des données structurées, des relations métier et des contraintes permettant de reproduire un environnement réel.

Les données générées serviront comme source d'entrée pour les prochaines étapes du projet :

```text
Extraction
    |
    v
Nettoyage et transformation
    |
    v
Contrôle qualité des données
    |
    v
Intégration dans une base décisionnelle
    |
    v
Analyse et tableaux de bord Power BI
```

Cette source constitue donc la première étape de construction de la plateforme décisionnelle EduSmart.
````
