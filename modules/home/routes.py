from flask import Blueprint, render_template
from core.security import login_required   # <-- ADICIONA ESTA LINHA

home = Blueprint("home", __name__, template_folder="templates")

@home.route("/")
@login_required  # <-- PROTEGE A ROTA
def home_page():
    return render_template("home.html")  # ou "home/home.html", dependendo de como está seu template
