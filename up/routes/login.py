from flask import Blueprint, render_template, redirect, request, session
from functools import wraps
from models import User

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        user = User(username, password)
        if user.authenticate(username, password):
            session["logged_in"] = True
            return redirect("/")
        else:
            return render_template("login.html", error="Username or password incorrect")
    else:
        return render_template("login.html")
    
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect("/login")  # Redirige al login si no está logueado
        return f(*args, **kwargs)
    return decorated_function