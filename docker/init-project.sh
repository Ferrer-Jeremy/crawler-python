#!/bin/bash

TC_RESET=$'\x1B[0m'
TC_SKY=$'\x1B[0;37;44m'
CLREOL=$'\x1B[K'
echoHeaderText () {
    echo -n "${TC_SKY}${CLREOL}"
    echo -e "\n           $1${CLREOL}"
    echo -n "${TC_SKY}${CLREOL}"
    echo ${TC_RESET}
}


echoHeaderText '(Re)creating Docker containers'
docker-compose up -d --force-recreate

docker-compose run --user="www-data" --rm application chmod +x docker/application/geckodriver
#docker-compose run --user="www-data" --rm application xvfb-run &&
#docker-compose run --user="www-data" --rm application bash export DISPLAY=:99


echoHeaderText 'Initializing  databases'
#docker-compose run --user="www-data" --rm application python3 docker/database-init.py

echoHeaderText 'Docker containers'
docker-compose ps