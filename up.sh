#!/usr/bin/env bash
docker-compose down
docker-compose up -d

while sleep 3; do
    docker ps | grep pythonjupyter;
    if [ $? -eq 0 ]; then
        docker exec -it pythonjupyter bash ;
        break;
    fi
done