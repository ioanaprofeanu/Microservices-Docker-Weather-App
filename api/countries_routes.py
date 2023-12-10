# Profeanu Ioana, 343C1 - routes for the countries table
from flask import Flask, request, jsonify
import psycopg2
from weather_forecast_schema import Country
import json


def countries_routes(app, cursor, connection):
    """
    function for creating the routes for the countries table
    parameters: app - the Flask app;
                cursor - the cursor for the database connection;
                connection - the connection to the database
    """

    # get all countries
    @app.route('/api/countries', methods=['GET'])
    def get_countries():
        # fetch all rows from the table
        cursor.execute(
            "SELECT id, nume_tara, latitudine::float, longitudine::float FROM Tari")
        rows = cursor.fetchall()

        # convert each row to a Country object and store in an array
        countries_list = [
            Country(id=row[0], nume=row[1], lat=row[2], lon=row[3]) for row in rows]

        return jsonify(countries_list), 200

    # add new country entry
    @app.route('/api/countries', methods=['POST'])
    def add_country():
        try:
            # verify if the request contains the required fields
            data = request.get_json()
            if 'nume' not in data:
                return '', 400
            if ('lat' not in data):
                return '', 400
            if ('lon' not in data):
                return '', 400

            # verify if the lat and lon values are float numbers
            try:
                float_value = float(data['lat'])
            except ValueError:
                return '', 400

            try:
                float_value = float(data['lon'])
            except ValueError:
                return '', 400

            # insert the new entry into the database
            cursor.execute("INSERT INTO Tari (nume_tara, latitudine, longitudine) VALUES (%s, %s, %s) RETURNING id",
                           (data['nume'], data['lat'], data['lon']))
            connection.commit()

            # return the id of the newly inserted entry
            inserted_id = cursor.fetchone()[0]
            return json.dumps({'id': inserted_id}), 201

        except psycopg2.Error as e:
            connection.rollback()
            # check if the error means that the new country name is already in the database
            if 'duplicate key value violates unique constraint "tari_nume_tara_key"' in str(e):
                return '', 409
            return '', 400

    # update a country entry
    @app.route("/api/countries/<id>", methods=["PUT"])
    def patch_country(id):
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

            # check if the entry with the given id exists;
            # if it doesn't exist, return 404
            cursor.execute("SELECT id FROM Tari WHERE id = %s", (id,))
            row = cursor.fetchone()
            if row is None:
                return '', 404

            # update the entry with the given id
            cursor.execute("UPDATE Tari SET nume_tara = %s, latitudine = %s, longitudine = %s WHERE id = %s",
                           (data['nume'], data['lat'], data['lon'], id))
            connection.commit()

            return '', 200

        except psycopg2.Error as e:
            connection.rollback()
            # check if the error means that the new country name is already in the database
            if 'duplicate key value violates unique constraint "tari_nume_tara_key"' in str(e):
                return '', 409
            # check if the new id we try to assign already exists
            if 'duplicate key value violates unique constraint "tari_pkey"' in str(e):
                return '', 409
            return '', 400

    # delete a country entry
    @app.route("/api/countries/<id>", methods=['DELETE'])
    def delete_country(id):
        try:
            # check if id is number
            if not str(id).isdigit():
                return '', 400

            # check if the entry with the given id exists
            # if it doesn't exist, return 404
            cursor.execute("SELECT id FROM Tari WHERE id = %s", (id,))
            row = cursor.fetchone()
            if row is None:
                return '', 404

            # delete the entry with the given id
            cursor.execute("DELETE FROM Tari WHERE id = %s", (id,))
            connection.commit()
            return '', 200

        except psycopg2.Error as e:
            connection.rollback()
            return '', 400
