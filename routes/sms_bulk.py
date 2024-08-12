from flask import Blueprint, render_template, request, redirect
from routes.login import login_required
import telnyx
import csv
import os
import pandas as pd
import datetime
import shutil
import time
import sqlite3
import numlookupapi
from flask import jsonify

sms_bulk_blueprint = Blueprint('sms_bulk', __name__)

def validate_csv(csv_file_path):
    with open(csv_file_path, "r") as f:
        reader = csv.reader(f)
        encoding = f.encoding
        print(encoding)
        for row in reader:
            if len(row) != 1:
                return False
            try:
                if not row[0].startswith("+1"):
                    return False
            except ValueError:
                return False
    return True

@sms_bulk_blueprint.route("/bulk-sms-send", methods=["POST", "GET"])
@login_required
def sms_bulk():
    if request.method == "POST":
        # Upload the CSV file
        #csv_file = request.files.get("csv_file")  # Get the CSV file

        csv_file = request.files.get("csv_file")

        def get_temp_file_path(csv_file):
            os.makedirs("/tmp", exist_ok=True)
            temp_file_path = os.path.join("tmp/", "csv_file_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv")

            with open(temp_file_path, "wb") as temp_file:
                shutil.copyfileobj(csv_file, temp_file)

            return temp_file_path

        if csv_file:
            try:
                # Save the CSV file temporarily
                os.makedirs("/tmp", exist_ok=True)
                #temp_file_path = os.path.join("tmp/", os.path.normpath(csv_file.filename))
                
                #csv_file.save(os.path.join("tmp/", "csv_file_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"))
                temp_file_path = get_temp_file_path(csv_file)

                print(temp_file_path)

                if validate_csv(temp_file_path):
                    print("El archivo CSV es válido.")
                else:
                    print("El archivo CSV no es válido.")

                # Verify and process the CSV file
                #numbers = []

                data = []

                with open(temp_file_path, "r") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        data.append(row)

                #print(numbers)

                contact_fields = {
                    "PHONE-NUMBER": True,
                    "BUSINESS-NAME": True,
                    "CONTACT-NAME": True,
                    "ADDRESS":False,
                    "CITY":False,
                    "STATE":False,
                    "ZIP-CODE":False,
                    "COMMUNICATION-METHOD":False,
                    "BIRTHDAY":False,
                    "CUSTOM-#1":False,
                    "CUSTOM-#2":False,
                    "CUSTOM-#3":False
                }

                number_count = len(data)

                sent_count = 0

                client = numlookupapi.Client('num_live_WU95gjzcdLqNpiH1ql6LCArnA0EHK0CT86YxicSD')

                # Take dates from form sms_bulk.html
                telnyx.api_key = "KEY018ACDF31427E3EE307019E0E38C100C_eHOH9Dl9Y3rQMX1aW6dYbT"

                sms_content = request.form["sms_content"]
                your_telnyx_number = request.form["telnyx_number"]
                
                # Create report of campaign in sms_camaigns.db
                connection = sqlite3.connect("sms_campaigns.db")
                cursor = connection.cursor()
                cursor.execute("""
                        INSERT INTO campaigns (send_date, sender_number, number_count, finish_date_time)
                        VALUES (?, ?, ?, ?)
                    """, (datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p"), your_telnyx_number, sent_count, None))
                connection.commit()

                # Send SMS messages

                for contact in data:

                    # Build personalized message using tags
                    personalized_message = sms_content.format(
                        BUSINESS_NAME=contact.get("BUSINESS_NAME", ""),
                        CONTACT_NAME=contact.get("CONTACT_NAME", ""),
                        ADDRESS=contact.get("ADDRESS", ""),
                        CITY=contact.get("CITY", ""),
                        STATE=contact.get("STATE", ""),
                        ZIP_CODE=contact.get("ZIP_CODE", ""),
                        COMMUNICATION_METHOD=contact.get("COMMUNICATION_METHOD", ""),
                        BIRTHDAY=contact.get("BIRTHDAY", ""),
                        CUSTOM_1=contact.get("CUSTOM_1", ""),
                        CUSTOM_2=contact.get("CUSTOM_2", ""),
                        CUSTOM_3=contact.get("CUSTOM_3", ""),
                        PHONE_NUMBER=contact.get("PHONE_NUMBER", "")
                    )

                    phone_number = contact.get("PHONE_NUMBER")
                    result = client.validate(phone_number)
                    print(result['valid'] is True)

                    if result['valid'] is True:
                        try:
                            telnyx.Message.create(
                                from_=your_telnyx_number,
                                to=phone_number,
                                text=personalized_message,
                            )
                            sent_count += 1
                        except Exception as e:
                            # Handle sending error
                            return render_template("sms-bulk.html", data=f"Error sending SMS: {e}")

                cursor.execute("UPDATE campaigns SET finish_date_time = ? WHERE id = ?", (datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p"), cursor.lastrowid))
                cursor.execute("UPDATE campaigns SET number_count = ? WHERE id = ?", (sent_count, cursor.lastrowid))
                connection.commit()
                connection.close()

                # Successful processing
                return render_template("sms-bulk.html", data="SMS SENT =", number_count=number_count, sent_count=sent_count)

            except Exception as e:
                # General error handling
                return render_template("sms-bulk.html", data=f"Error processing CSV file: {e}")

    return render_template("sms-bulk.html")
