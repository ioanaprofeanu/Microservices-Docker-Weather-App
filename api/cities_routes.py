from flask import Flask, request, jsonify
import psycopg2
from weather_forecast_schema import City
import json

def cities_routes(app, cursor, connection):
	@app.route('/api/cities', methods=['GET'])
	def get_cities():
		cursor.execute("SELECT id, id_tara, nume_oras, latitudine::float, longitudine::float FROM Orase")
		rows = cursor.fetchall()
		# Convert each row to a Tara object and store in an array
		cities_list = [City(id=row[0], idTara = row[1], nume=row[2], lat=row[3], lon=row[4]) for row in rows]
        
		return jsonify(cities_list), 200

	@app.route('/api/cities/country/<id_Tara>', methods=['GET'])
	def get_cities_by_country(id_Tara):
		cursor.execute("SELECT id, id_tara, nume_oras, latitudine::float, longitudine::float FROM Orase WHERE id_tara = %s", (id_Tara,))
		rows = cursor.fetchall()
		# Convert each row to a Tara object and store in an array
		cities_list = [City(id=row[0], idTara = row[1], nume=row[2], lat=row[3], lon=row[4]) for row in rows]
        
		return jsonify(cities_list), 200

	@app.route('/api/cities', methods=['POST'])
	def add_city():
		pass
		try:
			data = request.get_json()
			if 'idTara' not in data:
				return '', 400
			if 'nume' not in data:
				return '', 400
			if ('lat' not in data):
				return '', 400
			if ('lon' not in data):
				return '', 400

			# check if the country entry with the given id exists
			cursor.execute("SELECT id FROM Tari WHERE id = %s", (data['idTara'],))
			row = cursor.fetchone()
			if row is None:
				return '', 404

			cursor.execute("INSERT INTO Orase (id_tara, nume_oras, latitudine, longitudine) VALUES (%s, %s, %s, %s) RETURNING id", (data['idTara'], data['nume'], data['lat'], data['lon']))
			connection.commit()
   
			inserted_id = cursor.fetchone()[0]
			return json.dumps({'id' : inserted_id}), 201

		except psycopg2.Error as e:
			connection.rollback()
			# check if the error contains "duplicate key value violates unique constraint "tari_nume_tara_key"
			if 'duplicate key value violates unique constraint "orase_id_tara_nume_oras_key"' in str(e):
				return '', 409
			return '', 400
		
	@app.route("/api/cities/<id>", methods=["PUT"])
	def patch_city(id):
		pass
		# try:
		# 	data = request.get_json()
		# 	if 'nume' not in data:
		# 		return '', 400
		# 	if ('lat' not in data):
		# 		return '', 400
		# 	if ('lon' not in data):
		# 		return '', 400

		# 	if not str(id).isdigit():
		# 		return '', 400

		# 	# check if the entry with the given id exists
		# 	cursor.execute("SELECT id FROM Tari WHERE id = %s", (id,))
		# 	row = cursor.fetchone()
		# 	if row is None:
		# 		return '', 404

		# 	cursor.execute("UPDATE Tari SET nume_tara = %s, latitudine = %s, longitudine = %s WHERE id = %s", (data['nume'], data['lat'], data['lon'], id))
		# 	connection.commit()
		# 	return '', 200

		# except psycopg2.Error as e:
		# 	connection.rollback()
		# 	# check if the error contains "duplicate key value violates unique constraint "tari_nume_tara_key"
		# 	if 'duplicate key value violates unique constraint "tari_nume_tara_key"' in str(e):
		# 		return '', 409
		# 	return '', 404

	@app.route("/api/cities/<id>", methods=['DELETE'])
	def delete_city(id):
		# skip
		pass
		# try:
		# 	# check if id is number
		# 	if not str(id).isdigit():
		# 		return '', 400
   
		# 	# check if the entry with the given id exists
		# 	cursor.execute("SELECT id FROM Tari WHERE id = %s", (id,))
		# 	row = cursor.fetchone()
		# 	if row is None:
		# 		return '', 404

		# 	cursor.execute("DELETE FROM Tari WHERE id = %s", (id,))
		# 	connection.commit()
		# 	return '', 200

		# except psycopg2.Error as e:
		# 	connection.rollback()
		# 	return '', 400