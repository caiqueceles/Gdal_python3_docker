#!/usr/bin/env bash
docker exec -it pythoncaique pip3 install "$@"
docker exec -it pythoncaique pip3 freeze > requirements.txt
# docker-compose build &>/dev/null &