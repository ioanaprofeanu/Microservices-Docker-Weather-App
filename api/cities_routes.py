# Profeanu Ioana, 343C1 - routes for the cities table
from flask import Flask, request, jsonify
import psycopg2
from weather_forecast_schema import City
import json


def cities_routes(app, cursor, connection):
    """
    function for creating the routes for the cities table
    parameters: app - the Flask app;
                cursor - the cursor for the database connection;
                connection - the connection to the database
    """

    # get all cities
    @app.route('/api/cities', methods=['GET'])
    def get_cities():
        # fetch all rows from the table
        cursor.execute(
            "SELECT id, id_tara, nume_oras, latitudine::float, longitudine::float FROM Orase")
        rows = cursor.fetchall()

        # convert each row to a City object and store in an array
        cities_list = [City(id=row[0], idTara=row[1], nume=row[2],
                            lat=row[3], lon=row[4]) for row in rows]

        return jsonify(cities_list), 200

    # get all cities from a given country
    @app.route('/api/cities/country/<id_Tara>', methods=['GET'])
    def get_cities_by_country(id_Tara):
        # fetch all rows from the table where the country id is the given one
        cursor.execute(
            "SELECT id, id_tara, nume_oras, latitudine::float, longitudine::float FROM Orase WHERE id_tara = %s", (id_Tara,))
        rows = cursor.fetchall()

        # convert each row to a City object and store in an array
        cities_list = [City(id=row[0], idTara=row[1], nume=row[2],
                            lat=row[3], lon=row[4]) for row in rows]

        return jsonify(cities_list), 200

    # add a new city entry
    @app.route('/api/cities', methods=['POST'])
    def add_city():
        try:
            # verify if the request contains the required fields
            data = request.get_json()
            if 'idTara' not in data:
                return '', 400
            if 'nume' not in data:
                return '', 400
            if ('lat' not in data):
                return '', 400
            if ('lon' not in data):
                return '', 400

            # verify if the data format is correct
            if not str(data['idTara']).isdigit():
                return '', 400

            try:
                float_value = float(data['lat'])
            except ValueError:
                return '', 400

            try:
                float_value = float(data['lon'])
            except ValueError:
                return '', 400

            # check if the country entry with the given id exists
            # if it doesn't exist, return 404
            cursor.execute("SELECT id FROM Tari WHERE id = %s",
                           (data['idTara'],))
            row = cursor.fetchone()
            if row is None:
                return '', 404

            # insert the new entry into the database
            cursor.execute("INSERT INTO Orase (id_tara, nume_oras, latitudine, longitudine) VALUES (%s, %s, %s, %s) RETURNING id",
                           (data['idTara'], data['nume'], data['lat'], data['lon']))
            connection.commit()

            # return the id of the newly inserted entry
            inserted_id = cursor.fetchone()[0]
            return json.dumps({'id': inserted_id}), 201

        except psycopg2.Error as e:
            connection.rollback()
            # check if the error contains means that there is already a city name and country id pair in the database
            if 'duplicate key value violates unique constraint "orase_id_tara_nume_oras_key"' in str(e):
                return '', 409
            return '', 400

    # update a city entry
    @app.route("/api/cities/<id>", methods=["PUT"])
    def patch_city(id):
        try:
            # check if id is number and if the request contains the required fields
            # and if the data format is correct
            if not str(id).isdigit():
                return '', 400

            data = request.get_json()
            if 'id' not in data:
                return '', 400
            if not str(data['id']).isdigit():
                return '', 400

            # check if data['id'] is the same as id
            if int(data['id']) != int(id):
                return '', 400

            if 'idTara' not in data:
                return '', 400
            if not str(data['idTara']).isdigit():
                return '', 400

            if 'nume' not in data:
                return '', 400

            if ('lat' not in data):
                return '', 400
            try:
                float_value = float(data['lat'])
            except ValueError:
                return '', 400

            if ('lon' not in data):
                return '', 400
            try:
                float_value = float(data['lon'])
            except ValueError:
                return '', 400

            # check if the entry with the given id exists
            # if it doesn't exist, return 404
            cursor.execute("SELECT id FROM Orase WHERE id = %s", (id,))
            row = cursor.fetchone()
            if row is None:
                return '', 404

            # check if the country entry with the given id exists
            # if it doesn't exist, return 404
            cursor.execute("SELECT id FROM Tari WHERE id = %s",
                           (data['idTara'],))
            row = cursor.fetchone()
            if row is None:
                return '', 404

            # update the entry with the given id
            cursor.execute("UPDATE Orase SET id = %s, id_tara = %s, nume_oras = %s, latitudine = %s, longitudine = %s WHERE id = %s",
                           (data['id'], data['idTara'], data['nume'], data['lat'], data['lon'], id))
            connection.commit()
            return '', 200

        except psycopg2.Error as e:
            connection.rollback()
            # check if the error means that the new city name and country id pair is already in the database
            if 'duplicate key value violates unique constraint "orase_id_tara_nume_oras_key"' in str(e):
                return '', 409
            # check if the new id we try to assign already exists
            if 'duplicate key value violates unique constraint "orase_pkey"' in str(e):
                return '', 409
            return '', 400

    # delete a city entry
    @app.route("/api/cities/<id>", methods=['DELETE'])
    def delete_city(id):
        try:
            # check if id is number
            if not str(id).isdigit():
                return '', 400

            # check if the entry with the given id exists
            # if it doesn't exist, return 404
            cursor.execute("SELECT id FROM Orase WHERE id = %s", (id,))
            row = cursor.fetchone()
            if row is None:
                return '', 404

            # delete the entry with the given id
            cursor.execute("DELETE FROM Orase WHERE id = %s", (id,))
            connection.commit()
            return '', 200

        except psycopg2.Error as e:
            connection.rollback()
            return '', 400
