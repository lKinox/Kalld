from flask import Blueprint, render_template, redirect, session, json
from routes.login import login_required
from json import JSONDecodeError
from datetime import datetime
import sqlite3

call_history_blueprint = Blueprint('call-history', __name__)

@call_history_blueprint.route("/call-history", methods=["GET"])
@login_required
def call_history():

    connection = sqlite3.connect("webhooks-call.db")
    cursor = connection.cursor()

    # Ejecuta la consulta para obtener los datos
    cursor.execute("SELECT * FROM webhooks")

    # Recupera los datos
    call_data = cursor.fetchall()

    # Cierra la conexión a la base de datos
    connection.close()

    # Prepara un diccionario vacío para almacenar los datos formateados
    formatted_data = []

    # Recorre cada registro en call_data
    for data in call_data:

        # Accede al contenido del webhook (asumiendo que está en el segundo elemento)
        webhook_content = data[1]

        # Extrae la información deseada del contenido del webhook:
        try:
            json_data = json.loads(webhook_content)

            # Accede a las secciones que necesitas del JSON
            
            occurred_at = json_data['data']['occurred_at']

            # Convierte la fecha y hora a un objeto datetime
            # Divide la cadena en dos partes
            date_time_str, timezone = occurred_at.split(".")

            # Elimina la zona horaria
            date_time_str = date_time_str[:-1]

            # Convierte la fecha y hora a un objeto datetime
            datetime_object = datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S")

            payload = json_data['data']['payload']

            # Extrae valores específicos del payload
            direction = payload['direction']
            from_number = payload['from']
            to_number = payload['to']

        except JSONDecodeError:
            # Maneja el error si el contenido no es un JSON válido
            continue

        # ... (resto del código para formatear fecha y hora, etc.)

        # Crea un diccionario con los valores formateados
        formatted_data.append({
            'occurred_at': datetime_object,
            'direction': direction,
            'from_number': from_number,
            'to_number': to_number
        })

    # Pasa el diccionario con los datos formateados a la plantilla
    return render_template('call-history.html', call_data=formatted_data)
