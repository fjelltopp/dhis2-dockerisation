# dhis2-dockerisation
Docker setup for starting DHIS2 based on a PostgreSQL SQL dump. Example configurations are presented in docker-compose files. Note that no SQL dumps are provided in the current version of the setup and must be provided from elsewhere.

## Requirements
This Docker setup requires the installation of following requirements:
 - Docker CE/EE: https://docs.docker.com/install/
 - Docker Compose version 1.12.0 or newer: https://docs.docker.com/compose/install/


## Setup

### Generating PostgreSQL database dumps

Instructions to generate SQL dumps from PostgreSQL 9.5 can be found here: https://www.postgresql.org/docs/9.5/static/backup-dump.html

### Configuring database container
 In the `docker-compose-<deployment>.yml` file, the database configuration must be set to match the configurations in the database used to generate the SQL dump. Also the SQL dump needs to be mounted as a volume.
1. Set the service image to match the correct PostgreSQL version. Note that the image is for PostgreSQL with PostGIS extension already installed:
`image: mdillon/postgis:9.5`
2. Set the environmental variables to correct database name and default user as in the SQL dump. Password is generated here and needs only to match the webapp constainer configurations:
	```
	POSTGRES_USER: <user>
	POSTGRES_DB: <database>
	POSTGRES_PASSWORD: <password>
	POSTGRES_DB_TARGET: dhis-target
	```
3. Set the container healthcheck to point into the correct database:
`test: ["CMD-SHELL", "pg_isready -h database -p 5432 -d <database>"]`
4. Mount the creation scripts for all non-default database users as a volume to `/docker-entrypoint-initdb.d/1-db-init.sql`
5. Mount the SQL dump as a volume to `/docker-entrypoint-initdb.d/2-backup.sql`

### Configuring webapp container
1. Set the service image to match the same DHIS2 version as was used in the source system of the SQL dump:
`dhis2/dhis2-web:2.27-tomcat7-jre8-latest`
2. Set the environmental variable to correct database name:
`POSTGRES_DB: <database>`
4. Edit the DHIS2 configuration file to have the correct DB configurations as in the SQL dump and mount it as a volume to `/opt/dhis2/config/dhis.conf`


## Launching services
Launch the services by calling docker-compose:
`docker-compose -f docker-compose-<deployment>.yml up -d`
The DHIS2 service is accessible in `localhost:8085` unless another port was mapped in the Docker Compose file.
