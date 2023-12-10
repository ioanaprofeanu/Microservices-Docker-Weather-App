# Profeanu Ioana, 343C1 - routes for the temperatures table
from flask import Flask, request, jsonify
import psycopg2
from weather_forecast_schema import Temperature, TemperatureFilters
import json
from datetime import datetime


def is_valid_float(value_str):
    '''
    function for checking if a string is a valid float
    '''
    try:
        float(value_str)
        return True
    except ValueError:
        return False


def is_valid_date(date_str):
    '''
    function for checking if a string is a valid date with the format YYYY-MM-DD
    '''
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def get_filters_and_parameters(get_all, from_date_str=None, until_date_str=None, lat_str=None, lon_str=None):
    '''
    function for creating the query filters and parameters tuple
    '''
    # create a new empty TemperatureFilters object
    new_temperature_filters = TemperatureFilters()

    # check if the query parameters are valid and
    # set the corresponding fields in the TemperatureFilters object
    if (get_all == True):
        if lat_str is not None and is_valid_float(lat_str):
            new_temperature_filters.lat = float(lat_str)
        if lon_str is not None and is_valid_float(lon_str):
            new_temperature_filters.lon = float(lon_str)

    if from_date_str is not None and is_valid_date(from_date_str):
        new_temperature_filters.from_date = datetime.strptime(
            from_date_str, '%Y-%m-%d')
    if until_date_str is not None and is_valid_date(until_date_str):
        new_temperature_filters.until_date = datetime.strptime(
            until_date_str, '%Y-%m-%d')

    # create an array of query filters and a tuple of parameters
    # used for the query and for each valid field in the TemperatureFilters object,
    # add a filter and a parameter to the corresponding arrays
    filters = []
    parameters_tuple = ()

    if (get_all == True):
        if new_temperature_filters.lat is not None:
            filters.append("o.latitudine = %s")
            parameters_tuple = parameters_tuple + \
                (new_temperature_filters.lat,)
        if new_temperature_filters.lon is not None:
            filters.append("o.longitudine = %s")
            parameters_tuple = parameters_tuple + \
                (new_temperature_filters.lon,)

    if new_temperature_filters.from_date is not None:
        filters.append("t.timestamp >= %s")
        parameters_tuple = parameters_tuple + \
            (new_temperature_filters.from_date,)
    if new_temperature_filters.until_date is not None:
        filters.append("t.timestamp <= %s")
        parameters_tuple = parameters_tuple + \
            (new_temperature_filters.until_date,)

    return filters, parameters_tuple


def temperatures_routes(app, cursor, connection):
    """
    function for creating the routes for the temperatures table
    parameters: app - the Flask app;
                cursor - the cursor for the database connection;
                connection - the connection to the database
    """

    # get all temperatures that match the given filters
    @app.route('/api/temperatures', methods=['GET'])
    def get_temperatures():
        # extract query parameters
        lat_str = request.args.get('lat')
        lon_str = request.args.get('lon')
        from_date_str = request.args.get('from')
        until_date_str = request.args.get('until')

        # get the filters and parameters tuple
        filters, parameters_tuple = get_filters_and_parameters(
            True, from_date_str, until_date_str, lat_str, lon_str)

        # if there are no filters, extract all rows from the table
        if len(filters) == 0:
            cursor.execute(
                "SELECT t.id, t.valoare::float, t.timestamp FROM Temperaturi t INNER JOIN Orase o ON o.id = t.id_oras")
        else:
            # otherwise, execute the query by adding the filters to the WHERE clause
            query = "SELECT t.id, t.valoare::float, t.timestamp FROM Temperaturi t INNER JOIN Orase o ON o.id = t.id_oras WHERE " + \
                " AND ".join(filters)
            cursor.execute(query, parameters_tuple)

        rows = cursor.fetchall()
        # convert each row to a temperature object and store in an array
        temperatures_list = [Temperature(
            id=row[0], valoare=row[1], timestamp=row[2]) for row in rows]
        for temperature in temperatures_list:
            temperature.timestamp = temperature.timestamp.strftime(
                '%Y-%m-%d')

        return jsonify(temperatures_list), 200

    # get all temperatures for a given city
    @app.route('/api/temperatures/cities/<id_oras>', methods=['GET'])
    def get_temperatures_by_city(id_oras):
        # extract query parameters
        from_date_str = request.args.get('from')
        until_date_str = request.args.get('until')

        # get the filters and parameters tuple
        filters, parameters_tuple = get_filters_and_parameters(
            False, from_date_str, until_date_str)
        parameters_tuple = (id_oras,) + parameters_tuple

        # if there are no filters, extract all rows from the table from the given city id
        if len(filters) == 0:
            cursor.execute(
                "SELECT t.id, t.valoare::float, t.timestamp FROM Temperaturi t INNER JOIN Orase o ON o.id = t.id_oras WHERE o.id = %s", (id_oras,))
        else:
            # otherwise, execute the query by adding the filters to the WHERE clause
            query = "SELECT t.id, t.valoare::float, t.timestamp FROM Temperaturi t INNER JOIN Orase o ON o.id = t.id_oras WHERE o.id = %s " + \
                " AND ".join(filters)
            cursor.execute(query, parameters_tuple)

        rows = cursor.fetchall()
        # convert each row to a Temperature object and store in an array
        temperatures_list = [Temperature(
            id=row[0], valoare=row[1], timestamp=row[2]) for row in rows]
        for temperature in temperatures_list:
            temperature.timestamp = temperature.timestamp.strftime(
                '%Y-%m-%d')

        return jsonify(temperatures_list), 200

    # get all temperatures for a given country
    @app.route('/api/temperatures/countries/<id_tara>', methods=['GET'])
    def get_temperatures_by_country(id_tara):
        # extract query parameters
        from_date_str = request.args.get('from')
        until_date_str = request.args.get('until')

        # get the filters and parameters tuple
        filters, parameters_tuple = get_filters_and_parameters(
            False, from_date_str, until_date_str)
        parameters_tuple = (id_tara,) + parameters_tuple

        # if there are no filters, extract all rows from the table from the given country id
        if len(filters) == 0:
            cursor.execute(
                "SELECT t.id, t.valoare::float, t.timestamp FROM Temperaturi t INNER JOIN Orase o ON o.id = t.id_oras INNER JOIN Tari c on c.id = o.id_tara WHERE c.id = %s", (id_tara,))
        else:
            # otherwise, execute the query by adding the filters to the WHERE clause
            query = "SELECT t.id, t.valoare::float, t.timestamp FROM Temperaturi t INNER JOIN Orase o ON o.id = t.id_oras INNER JOIN Tari c on c.id = o.id_tara WHERE c.id = %s " + \
                " AND ".join(filters)
            cursor.execute(query, parameters_tuple)

        rows = cursor.fetchall()
        # convert each row to a Temperature object and store in an array
        temperatures_list = [Temperature(
            id=row[0], valoare=row[1], timestamp=row[2]) for row in rows]
        for temperature in temperatures_list:
            temperature.timestamp = temperature.timestamp.strftime(
                '%Y-%m-%d')

        return jsonify(temperatures_list), 200

    # add a new temperature entry
    @app.route('/api/temperatures', methods=['POST'])
    def add_temperature():
        try:
            # verify if the request contains the required fields
            data = request.get_json()
            if 'idOras' not in data:
                return '', 400
            if 'valoare' not in data:
                return '', 400

            # verify if the data format is correct
            if not str(data['idOras']).isdigit():
                return '', 400

            try:
                float_value = float(data['valoare'])
            except ValueError:
                return '', 400

            # check if the city entry with the given id exists
            # if not, return 404
            cursor.execute("SELECT id FROM Orase WHERE id = %s",
                           (data['idOras'],))
            row = cursor.fetchone()
            if row is None:
                return '', 404

            # insert the new entry into the database
            cursor.execute("INSERT INTO Temperaturi (id_oras, valoare) VALUES (%s, %s) RETURNING id",
                           (data['idOras'], data['valoare']))
            connection.commit()

            # return the id of the newly inserted entry
            inserted_id = cursor.fetchone()[0]
            return json.dumps({'id': inserted_id}), 201

        except psycopg2.Error as e:
            connection.rollback()
            # check if the error means that the idOras and timestamp pair is already in the database
            if 'duplicate key value violates unique constraint "temperaturi_id_oras_timestamp_key"' in str(e):
                return '', 409
            return '', 400

    # update a temperature entry
    @app.route("/api/temperatures/<id>", methods=["PUT"])
    def patch_temperature(id):
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

            if 'idOras' not in data:
                return '', 400
            if not str(data['idOras']).isdigit():
                return '', 400

            if 'valoare' not in data:
                return '', 400
            try:
                float_value = float(data['valoare'])
            except ValueError:
                return '', 400

            # check if the entry with the given id exists
            # if it doesn't exist, return 404
            cursor.execute("SELECT id FROM Temperaturi WHERE id = %s", (id,))
            row = cursor.fetchone()
            if row is None:
                return '', 404

            # check if the city entry with the given id exists
            # if not, return 404
            cursor.execute("SELECT id FROM Orase WHERE id = %s",
                           (data['idOras'],))
            row = cursor.fetchone()
            if row is None:
                return '', 404

            # update the entry in the database
            cursor.execute("UPDATE Temperaturi SET id = %s, id_oras = %s, valoare = %s WHERE id = %s",
                           (data['id'], data['idOras'], data['valoare'], id))
            connection.commit()
            return '', 200

        except psycopg2.Error as e:
            connection.rollback()
            # check if the error means that the idOras and timestamp pair is already in the database
            if 'duplicate key value violates unique constraint "temperaturi_id_oras_timestamp_key"' in str(e):
                return '', 409
            # check if the new id we try to assign already exists
            if 'duplicate key value violates unique constraint "temperaturi_pkey"' in str(e):
                return '', 409
            return '', 400

    # delete a temperature entry
    @app.route("/api/temperatures/<id>", methods=['DELETE'])
    def delete_temperature(id):
        try:
            # check if id is number
            if not str(id).isdigit():
                return '', 400

            # check if the entry with the given id exists
            # if it doesn't exist, return 404
            cursor.execute("SELECT id FROM Temperaturi WHERE id = %s", (id,))
            row = cursor.fetchone()
            if row is None:
                return '', 404

            # delete the entry from the database
            cursor.execute("DELETE FROM Temperaturi WHERE id = %s", (id,))
            connection.commit()
            return '', 200

        except psycopg2.Error as e:
            connection.rollback()
            return '', 400
