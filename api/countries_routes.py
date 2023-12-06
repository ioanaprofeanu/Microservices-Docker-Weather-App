from flask import Flask, request, jsonify
import psycopg2
from weather_forecast_schema import Country
import json

def countries_routes(app, cursor, connection):
	@app.route('/api/countries', methods=['GET'])
	def get_countries():
		cursor.execute("SELECT id, nume_tara, latitudine::float, longitudine::float FROM Tari")
		rows = cursor.fetchall()
		# Convert each row to a Tara object and store in an array
		countries_list = [Country(id=row[0], nume=row[1], lat=row[2], lon=row[3]) for row in rows]
        
		return jsonify(countries_list), 200
 
	@app.route('/api/countries', methods=['POST'])
	def add_country():
		try:
			data = request.get_json()
			if 'nume' not in data:
				return '', 400
			if ('lat' not in data):
				return '', 400
			if ('lon' not in data):
				return '', 400

			cursor.execute("INSERT INTO Tari (nume_tara, latitudine, longitudine) VALUES (%s, %s, %s) RETURNING id", (data['nume'], data['lat'], data['lon']))
			connection.commit()
   
			inserted_id = cursor.fetchone()[0]
			return json.dumps({'id' : inserted_id}), 201

		except psycopg2.Error as e:
			connection.rollback()
			# check if the error contains "duplicate key value violates unique constraint "tari_nume_tara_key"
			if 'duplicate key value violates unique constraint "tari_nume_tara_key"' in str(e):
				return '', 409
			return '', 400
		
	@app.route("/api/countries/<id>", methods=["PUT"])
	def patch_country(id):
		try:
			data = request.get_json()
			if 'nume' not in data:
				return '', 400
			if ('lat' not in data):
				return '', 400
			if ('lon' not in data):
				return '', 400

			if not str(id).isdigit():
				return '', 400

			# check if the entry with the given id exists
			cursor.execute("SELECT id FROM Tari WHERE id = %s", (id,))
			row = cursor.fetchone()
			if row is None:
				return '', 404

			cursor.execute("UPDATE Tari SET nume_tara = %s, latitudine = %s, longitudine = %s WHERE id = %s", (data['nume'], data['lat'], data['lon'], id))
			connection.commit()
			return '', 200

		except psycopg2.Error as e:
			connection.rollback()
			# check if the error contains "duplicate key value violates unique constraint "tari_nume_tara_key"
			if 'duplicate key value violates unique constraint "tari_nume_tara_key"' in str(e):
				return '', 409
			return '', 404

	@app.route("/api/countries/<id>", methods=['DELETE'])
	def delete_country(id):
		try:
			# check if id is number
			if not str(id).isdigit():
				return '', 400
   
			# check if the entry with the given id exists
			cursor.execute("SELECT id FROM Tari WHERE id = %s", (id,))
			row = cursor.fetchone()
			if row is None:
				return '', 404

			cursor.execute("DELETE FROM Tari WHERE id = %s", (id,))
			connection.commit()
			return '', 200

		except psycopg2.Error as e:
			connection.rollback()
			return '', 400