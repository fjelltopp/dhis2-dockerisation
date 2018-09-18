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

## Utility scripts

### Removing organisation unit from a DHIS2 instance

Instructions to remove an organisation unit from a DHIS2 instance

#### Removing leaf organisation units

Repeat the following steps for all leaf organisation units
1. In the DHIS2 UI in Organisation Units, remove all data sets from the organisation unit
2. Configure and run script `util/delete_organisational_unit.py` to soft delete all data values from the unit
3. `util/delete_organisational_unit.py` print the `uid` of the organisational unit. You can also get this from the web API
4. Use the DHIS2 UI in Data Administration -> Maintenance to permanently delete soft deleted data values
5. Configure the SQL delete statement "delete all data value audits for organisation id" in `util/database_utils.sql` to use the
`uid` of the organisation unit. Run the data value audit deletion statement in the backend database.
6. Using the DHIS2 UI in Organisation Units, delete the organisation unit

####  Removing non-leaf organisation units

1. Remove all organisation units further down in the organisation hierarchy using the instructions above
2. Use the Web API `<dhis_api_url>/organisationUnits/<uid>` to get the full object description of the organisation unit to be removed
3. Edit the JSON object destription to replace the following array values with empty values: `organisationUnits` and `dataViewOrganisationUnits`
4. Use the same Web API `<dhis_api_url>/organisationUnits/<uid>` to `PUT` the edited JSON payload to update the user
5. Use the DHIS2 UI in Organisation Units to remove the organisation unit now that all references have been removed
