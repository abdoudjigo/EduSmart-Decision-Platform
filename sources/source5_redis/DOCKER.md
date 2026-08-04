# Redis — EduSmart Decision Platform

## Création du conteneur

Aucune personnalisation de l'image officielle n'est nécessaire.

```bash
docker run -d \
  --name edusmart-redis \
  -p 6379:6379 \
  -v edusmart_redis_data:/data \
  redis:latest
```

## Réinjection des données (si le volume est neuf)

```bash
source venv/bin/activate
python sources/source5_redis/scripts/insert_data.py
```

## Vérification

```bash
docker exec edusmart-redis redis-cli DBSIZE
```
