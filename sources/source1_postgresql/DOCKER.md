# PostgreSQL — EduSmart Decision Platform

## Migration depuis le service natif

Base exportée depuis l'installation native puis restaurée dans le conteneur.

pg_dump -h localhost -p 5432 -U postgres -F c -f edusmart_academic.dump edusmart_academic

## Création du conteneur

Note : Postgres 18+ exige un montage sur /var/lib/postgresql (pas /var/lib/postgresql/data).

docker run -d --name edusmart-postgres -p 5432:5432 -e POSTGRES_PASSWORD=5853500 -v edusmart_postgres_data:/var/lib/postgresql postgres:latest

## Restauration (si volume neuf)

docker exec edusmart-postgres psql -U postgres -c "CREATE DATABASE edusmart_academic;"
docker exec -i edusmart-postgres pg_restore -U postgres -d edusmart_academic < edusmart_academic.dump

## Vérification

psql -h localhost -p 5432 -U postgres -d edusmart_academic -c "SELECT count(*) FROM etudiants;"
