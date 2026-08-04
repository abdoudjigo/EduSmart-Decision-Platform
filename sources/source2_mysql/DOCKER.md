# MySQL — EduSmart Decision Platform

## Migration depuis le service natif

mysqldump -h localhost -P 3306 -u root -p5853500 edusmart_learning > edusmart_learning.sql

## Création du conteneur

docker run -d --name edusmart-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=5853500 -v edusmart_mysql_data:/var/lib/mysql mysql:latest

## Restauration (si volume neuf)

docker exec edusmart-mysql mysql -u root -p5853500 -e "CREATE DATABASE edusmart_learning;"
docker exec -i edusmart-mysql mysql -u root -p5853500 edusmart_learning < edusmart_learning.sql

## Vérification

mysql -h localhost -P 3306 -u root -p5853500 edusmart_learning -e "SELECT count(*) FROM notes;"
