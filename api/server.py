#!/usr/bin/python
import psycopg2
from flask import Flask
from countries_routes import countries_routes
from cities_routes import cities_routes
from temperatures_routes import temperatures_routes

def database_connection():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(
			host="localhost",
			database="weather_forecast_db",
			user="postgres",
			password="postgres")
        
        return connection

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

def database_close_connection(connection):
     if connection is not None:
        connection.close()
        print('Database connection closed.')

def app_create(cursor, connection):
	app = Flask(__name__)
	countries_routes(app, cursor, connection)
	cities_routes(app, cursor, connection)
	temperatures_routes(app, cursor, connection)
	# de adaugat si alte rute
	return app
 
if __name__ == '__main__':
    connection = database_connection()
    cursor = connection.cursor()
    # cursor.execute('SET search_path TO weather_forecast_schema')
    
    app = app_create(cursor, connection)
    app.run(debug=True, port=6000)
    
    cursor.close()
    database_close_connection(connection)
    print('Server stopped.')