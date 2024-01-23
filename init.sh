#!/bin/bash
# Levantar los servicios con Docker Compose
docker-compose up -d

echo "Ejecutando init_db.py en contenedor INIT-DB..."
docker-compose exec -t INIT-DB python init_db.py
