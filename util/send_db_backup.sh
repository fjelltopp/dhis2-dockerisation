#!/usr/bin/env bash -e
scp -i ${RSA_KEY_PATH} db_backup.sql ${DESTINATION_HOST}:db_backup.sql
rm db_backup.sql