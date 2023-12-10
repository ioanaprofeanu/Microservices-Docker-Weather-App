# Profeanu Ioana, 343C1 - server app entry point
import psycopg2
from flask import Flask
from countries_routes import countries_routes
from cities_routes import cities_routes
from temperatures_routes import temperatures_routes


def database_connection():
    """
    function for connecting to the database
    """
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(
            host="weather_forecast_db",
            port="5432",
            database="weather_forecast_db",
            user="postgres",
            password="postgres")

        return connection

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None


def database_close_connection(connection):
    """
    function for closing the connection to the database
    parameters: connection - the connection to the database
    """
    if connection is not None:
        connection.close()
        print('Database connection closed.')


def app_create(cursor, connection):
    """
    function for creating the Flask app
    parameters: cursor - the cursor for the database connection;
                        connection - the connection to the database
    """
    app = Flask(__name__)
    print('Server started.')
    # add routes
    countries_routes(app, cursor, connection)
    cities_routes(app, cursor, connection)
    temperatures_routes(app, cursor, connection)

    return app


if __name__ == '__main__':
    # connect to the database
    connection = None
    # try to connect to the database until the connection is successful
    while connection is None:
        connection = database_connection()
    print('Connected to the database.')
    cursor = connection.cursor()

    # create the Flask app
    app = app_create(cursor, connection)
    app.run('0.0.0.0', debug=True, port=6000)

    # close the connection to the database
    cursor.close()
    database_close_connection(connection)
    print('Server stopped.')
