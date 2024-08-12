import os
from flask import Flask, Blueprint, request, render_template, json, redirect, flash
from json import JSONDecodeError
from routes.login import login_required
from datetime import datetime
import sqlite3
import telnyx

webhooks_blueprint = Blueprint('webhooks', __name__)

@webhooks_blueprint.route('/sms-inbound', methods=['POST', 'GET'])

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
        return render_template('sms-inbound.html'), 200
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
                our_phone_number = data.get("data", {}).get("payload", {}).get("to", {})[0].get("phone_number")
                occurred_at = data.get("data", {}).get("occurred_at")
                date_time_str, timezone = occurred_at.split(".")

                # Elimina la zona horaria
                date_time_str = date_time_str[:-1]

                # Convierte la fecha y hora a un objeto datetime
                datetime_object = datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S")
                if text and phone_number:  # Verifica que ambos campos existan
                    filtered_data.append([row[0], text, phone_number, our_phone_number, datetime_object])

            return render_template('sms-inbound.html', webhooks_data=filtered_data)
        except sqlite3.Error as e:
            print("Error al acceder a la base de datos:", e)
            return render_template('sms-inbound.html'), 500
        
@webhooks_blueprint.route('/answer-sms', methods=['POST'])
def sms_response():
    if request.method == 'POST':
        telnyx.api_key = "KEY018ACDF31427E3EE307019E0E38C100C_eHOH9Dl9Y3rQMX1aW6dYbT"

        dest_number = request.form["dest_number"]
        sms_content = request.form["sms_content"]
        telnyx_number = request.form["telnyx_number"]

        print(dest_number)
        print(telnyx_number)
        print(sms_content)

        your_telnyx_number = telnyx_number
        destination_number = dest_number

        telnyx.Message.create(
        from_=your_telnyx_number,
        to=destination_number,
        text=sms_content,
        )

        flash("SMS SENDED From: {} to: {}".format(your_telnyx_number, destination_number))
        return redirect("/sms-inbound")
    else:
        return render_template("sms-inbound.html")