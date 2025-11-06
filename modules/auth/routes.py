from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from core.extensions import db
from modules.users.models import User

auth = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    template_folder="../../templates/auth"
)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash("Credenciais inválidas", "error")
            return redirect(url_for("auth.login"))

        session["user_id"] = user.id
        return redirect(url_for("home.home_page"))

    return render_template("auth/login.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if User.query.filter_by(username=username).first():
            flash("Este nome de usuário já existe.", "error")
            return redirect(url_for("auth.signup"))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        return redirect(url_for("home.home_page"))

    return render_template("auth/signup.html")


@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
