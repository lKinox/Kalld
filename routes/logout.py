from flask import Blueprint, render_template, redirect, session
from routes.login import login_required

logout_blueprint = Blueprint('logout', __name__)

@logout_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    # Elimina la sesión del usuario
    session.pop("logged_in", None)

    # Redirige al inicio
    return redirect("/login")
