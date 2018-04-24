#!/usr/bin/env bash

psql -U postgres -c "CREATE USER ${DHIS2_PG_USER} WITH PASSWORD '${DHIS2_PG_PASSWORD}';"
psql -U postgres -c "ALTER USER ${DHIS2_PG_USER} CREATEDB;"
psql -U postgres -c "ALTER USER ${DHIS2_PG_USER} CREATEROLE;"
psql -U postgres -c "CREATE DATABASE ${DHIS2_PG_DB};"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ${DHIS2_PG_DB} TO ${DHIS2_PG_USER};"
psql -U ${DHIS2_PG_USER} ${DHIS2_PG_DB} < /tmp/dhis_init.sql



