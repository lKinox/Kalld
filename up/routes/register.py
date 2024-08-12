from flask import Blueprint, render_template, redirect, request, session
from models import NewUser
from models import User

register_blueprint = Blueprint('register', __name__)

@register_blueprint.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Valida que el username y el email no estén vacíos
        if not username or not email:
            return render_template("register.html", error="The username or email cannot be empty")

        if NewUser.validate_username(username):
            return render_template("register.html", error="The username is already registered")

        # Valida que el email no esté ya registrado
        if NewUser.validate_email(email):
            return render_template("register.html", error="The email is already registered")

        # Si todo está bien, registra el usuario
        newuser = NewUser(username, email, password)
        newuser.register()

        # Inicia sesión al usuario
        session["logged_in"] = True

        return redirect("/")
    else:
        return render_template("register.html")