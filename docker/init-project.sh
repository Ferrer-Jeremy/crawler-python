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

echoHeaderText 'Composer install'
docker-compose run --user="www-data" --rm application composer install --no-interaction

echoHeaderText 'Initializing  databases'
docker-compose run --user="www-data" --rm application chmod +x docker/database-init.sh
docker-compose run --user="www-data" --rm application ./docker/database-init.sh

echoHeaderText 'Docker containers'
docker-compose ps