# MongoDB — EduSmart Decision Platform

## Création du conteneur

Aucune personnalisation de l'image officielle n'est nécessaire.

docker run -d --name edusmart-mongo -p 27017:27017 -v edusmart_mongo_data:/data/db -v edusmart_mongo_config:/data/configdb mongo:latest

## Réinjection des données (si le volume est neuf)

source venv/bin/activate
python sources/source4_mongodb/scripts/insert_data.py

## Vérification

docker exec edusmart-mongo mongosh edusmart_mobile --quiet --eval "db.events.countDocuments()"
