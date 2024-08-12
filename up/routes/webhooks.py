import os
from flask import Flask, Blueprint, request, render_template, json
from json import JSONDecodeError
from routes.login import login_required
import sqlite3

webhooks_blueprint = Blueprint('webhooks', __name__)

@webhooks_blueprint.route('/webhooks', methods=['POST', 'GET'])

def webhooks():
    if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
        try:
            data = request.get_json()
            event_type = data.get("data", {}).get("event_type")

            if event_type == "message.received":
                # Guarda todo el JSON
                connection = sqlite3.connect("webhooks.db")
                cursor = connection.cursor()
                cursor.execute("INSERT INTO webhooks (data) VALUES (?)", (json.dumps(data),))
                connection.commit()
                connection.close()
                print("Datos del webhook guardados en la base de datos")
            else:
                # No guarda nada si event_type no es "message.received"
                pass
        except JSONDecodeError:
            print("El JSON es inválido")
        return render_template('webhooks.html'), 200
    else:  # Si es una solicitud GET, recuperar los datos de la base de datos y filtrarlos
        try:
            connection = sqlite3.connect("webhooks.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM webhooks")  # Recupera todos los datos sin filtrar
            webhooks_data = cursor.fetchall()
            filtered_data = []
            for row in webhooks_data:
                data = json.loads(row[1])  # Convierte la cadena JSON en un diccionario
                text = data.get("data", {}).get("payload", {}).get("text")
                phone_number = data.get("data", {}).get("payload", {}).get("from", {}).get("phone_number")
                if text and phone_number:  # Verifica que ambos campos existan
                    filtered_data.append([row[0], text, phone_number])

            return render_template('webhooks.html', webhooks_data=filtered_data)
        except sqlite3.Error as e:
            print("Error al acceder a la base de datos:", e)
            return render_template('webhooks.html'), 500