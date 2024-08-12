from flask import Blueprint, render_template, request
from routes.login import login_required
import telnyx

sms_blueprint = Blueprint('sms', __name__)

@sms_blueprint.route("/sms", methods=["POST", "GET"])
@login_required
def sms():
    if request.method == 'POST':
        telnyx.api_key = "KEY018ACDF31427E3EE307019E0E38C100C_eHOH9Dl9Y3rQMX1aW6dYbT"

        dest_number = request.form["dest_number"]
        sms_content = request.form["sms_content"]
        telnyx_number = request.form["telnyx_number"]

        your_telnyx_number = telnyx_number
        destination_number = dest_number

        telnyx.Message.create(
        from_=your_telnyx_number,
        to=destination_number,
        text=sms_content,
        )
        return render_template("sms.html", data="SMS SENDED")
    else:
        return render_template("sms.html")