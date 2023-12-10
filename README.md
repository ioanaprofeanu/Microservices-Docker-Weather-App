# Microservices-Docker-Weather-App
## Profeanu Ioana, 343C1 - Tema2 SPRC

### Project Structure:
.
├── api
│   ├── cities_routes.py
│   ├── countries_routes.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── server.py
│   ├── temperatures_routes.py
│   └── weather_forecast_schema.py
├── docker-compose.yml
├── init.sql
└── README.md

- The docker compose is run using the *docker-compose up -d* command in terminal.
- The docker-compose.yml file contains the following service definitions:
	- *weather_forecast_db*:
		- PostgreSQL database used to store the data; it uses a volume for data persistency and is
		inside two networks, weather_forecast_api_network and adminer_network.
	- *weather_forecast_api*:
		- the Python server api used to retrieve HTTP requests and connect to the database in order
		to parse data; the image is build from the Dockerfile found inside /api directory; the
		service is inside the weather_forecast_api_network, alongise the database
		- it is available at http://localhost:6000/
	- *weather_forecast_db_admin*:
		- a database manager for performing database operations. it is inside the adminer_network.
		it is available at http://localhost:8080/ and the connection to the database is made using
		the following credentials:
			- System: PostgreSQL
			- Server: weather_forecast_db
			- username: postgres
			- password: postgres
			- database: weather_forecast_db
- init.sql contains the PostgreSQL DDL queries for creating the database tables.
- The *api* directory contains:
	- the python implementation of the server api:
		- it uses *Flask* for http requests and route handling and *psycopg2* for database connection
		- *server.py* is the entrypoint of the api, and each route (for Countries, Cities, and
		Temperatures) is found in a separate file
	- *Dockerfile* used for building the api Docker image and the .dockerignore file.
	- The requirements.txt file, with the Python requirements used when building the api image.

## Useful commands:
- for running docker compose:
	docker-compose up -d
- for stopping docker compose:
	docker-compose down
- for deleting volume:
	docker volume rm *volume name*
- for deleting image:
	docker rmi *image name*

## Resources:
- SPRC Laboratory 3 & 4
- https://www.postgresqltutorial.com/postgresql-python/connect/
- https://youtu.be/3c-iBn73dDE?si=JpceswuyggguC5xK
- https://commandprompt.com/education/how-to-install-postgresql-using-docker-compose/
- https://www.freecodecamp.org/news/postgresql-in-python/
- https://www.postgresqltutorial.com/postgresql-python/ 
