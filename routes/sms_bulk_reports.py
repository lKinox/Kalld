from flask import Blueprint, render_template, redirect, session, json
from routes.login import login_required
import sqlite3

reports_blueprint = Blueprint('reports', __name__)

@reports_blueprint.route("/bulk-sms-reports", methods=["GET"])
@login_required
def reports():
    
    connection = sqlite3.connect("sms_campaigns.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM campaigns")  # Recupera todos los datos sin filtrar
    sms_data = cursor.fetchall()
    connection.close()

    return render_template('sms-bulk-reports.html', sms_data=sms_data)

