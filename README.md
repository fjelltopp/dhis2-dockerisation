# dhis2-dockerisation
Docker setup for starting DHIS2 based on a PostgreSQL SQL dump. An example configuration is presented in `docker-compose-example.yml` file.

## Requirements
This Docker setup requires the installation of following requirements:
 - Docker CE/EE: https://docs.docker.com/install/
 - Docker Compose version 1.12.0 or newer: https://docs.docker.com/compose/install/


## Setup

### Generating PostgreSQL database dumps

### Configuring database container
 In the `docker-compose.yml` file, the database configuration must be set to match the configurations in the database used to generate the SQL dump. Also the SQL dump needs to be mounted as a volume.
1. Set the service image to match the correct PostgreSQL version. Note that the image is for PostgreSQL with PostGIS extension already installed:
`image: mdillon/postgis:9.5`
2. Set the environmental variables to correct database name, default user and password as in the SQL dump:
	```
	POSTGRES_USER: dhis2
	POSTGRES_DB: dhis2
	POSTGRES_PASSWORD: dhis2
	POSTGRES_DB_TARGET: dhis-target
	```
3. Set the container healthcheck to point into the correct database:
`test: ["CMD-SHELL", "pg_isready -h database -p 5432 -d dhis2"]`
4. Mount the creation scripts for all non-default database users as a volume to `/docker-entrypoint-initdb.d/1-db-init.sql`
5. Mount the SQL dump as a volume to `/docker-entrypoint-initdb.d/2-backup.sql`

### Configuring webapp container
1. Set the service image to match the correct DHIS2 version:
`dhis2/dhis2-web:2.27-tomcat7-jre8-latest`
2. Set the environmental variable to correct database name:
`POSTGRES_DB: dhis2`
4. Edit the DHIS2 configuration file to have the correct DB configurations as in the SQL dump and mount it as a volume to `/opt/dhis2/config/dhis.conf`


## Launching services
Launch the services by calling docker-compose:
`docker-compose -f docker-compose-example.yml up -d`
The DHIS2 service is accessible in `localhost:8085` unless another port was mapped in the Docker Compose file.
