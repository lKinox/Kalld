from flask import Blueprint, render_template, request, Response, flash, redirect, make_response, url_for, json, jsonify
from routes.login import login_required
from json import JSONDecodeError
from flask_socketio import SocketIO
import telnyx
import sqlite3

call_blueprint = Blueprint('call', __name__)

telnyx.api_key = "KEY018ACDF31427E3EE307019E0E38C100C_eHOH9Dl9Y3rQMX1aW6dYbT"

@call_blueprint.route("/call-webhook", methods=["POST"])
def call_webhook():
    if request.method == 'POST':
        try:
            data = request.get_json()
            event_type = data.get("data", {}).get("event_type")

            if event_type == "call.initiated":
                # Guarda todo el JSON
                connection = sqlite3.connect("webhooks-call.db")
                cursor = connection.cursor()
                cursor.execute("INSERT INTO webhooks (data) VALUES (?)", (json.dumps(data),))
                connection.commit()
                connection.close()
                print("base de datos call guardada")
            else:
                # No guarda nada si event_type no es "message.received"
                pass
        except JSONDecodeError:
            print("El JSON es inválido")
        return render_template('call.html'), 200
    else:
        return render_template('call.html')

#jcollins65537
#lbmUhlQS