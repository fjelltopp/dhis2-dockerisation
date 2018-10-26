#!/usr/bin/env bash
docker exec -it dhis2-database bash -c 'pg_dump --username=$POSTGRES_USER --dbname=$POSTGRES_DB > db-backup.sql'
docker cp dhis2-database:/db-backup.sql .
docker exec -it dhis2-database bash -c 'rm -f db-backup.sql'