from flask import Flask, render_template, request, json,  make_response, flash, redirect, jsonify
from json import JSONDecodeError
from flask_socketio import SocketIO
import sqlite3
from flask_apscheduler import APScheduler
import threading
from routes.login import login_blueprint
from routes.register import register_blueprint
from routes.sms_send import sms_blueprint
from routes.sms_inbound import webhooks_blueprint
from routes.logout import logout_blueprint
from routes.sms_bulk import sms_bulk_blueprint
from routes.sms_bulk_reports import reports_blueprint
from routes.calls import call_blueprint
from routes.call_history import call_history_blueprint
from routes.login import login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin1234'
app.config['JSON_AS_ASCII'] = False
socketio = SocketIO(app)




app.register_blueprint(register_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(sms_blueprint)
app.register_blueprint(webhooks_blueprint)
app.register_blueprint(logout_blueprint)
app.register_blueprint(sms_bulk_blueprint)
app.register_blueprint(reports_blueprint)
app.register_blueprint(call_blueprint)
app.register_blueprint(call_history_blueprint)



@app.route("/call", methods=["GET", "POST"])
def call():
    if request.method == 'POST':
        json_data = request.get_json()
        call_type = json_data.get("data", {}).get("payload", {}).get("direction")
        event_type = json_data.get("data", {}).get("event_type")

        if event_type == "call.initiated":
            # Guarda todo el JSON
            connection = sqlite3.connect("webhooks-call.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO webhooks (data) VALUES (?)", (json.dumps(json_data),))
            connection.commit()
            connection.close()
            print("base de datos call guardada")
        if call_type == "incoming":
            from_call = json_data['data']['payload']['from']
            to_call = json_data['data']['payload']['to']

            socketio.emit('data_updated', {
                'from_call': from_call,
                'to_call': to_call
            })
            return jsonify({'status': 'success'})
        else:
            return render_template('call.html') 
    
    return render_template('call.html')   
    
@app.route("/", methods=["GET"])
@login_required
def index():
  return render_template("index.html")


if __name__ == "__main__":
    app.run(port=5000, debug=True)