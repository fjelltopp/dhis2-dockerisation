#!/usr/bin/env bash
set -e
mv ~/db-backup.sql ~/dhis2-dockerisation/${COUNTRY}/
cd ~/dhis2-dockerisation
set +e
set +x
docker-compose -f docker-compose-${COUNTRY}.yml -f docker-compose-ssl.yml down
docker volume ls -qf dangling=true | xargs -r docker volume rm
docker-compose -f docker-compose-${COUNTRY}.yml -f docker-compose-ssl.yml up -d
