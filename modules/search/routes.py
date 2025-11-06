from flask import Blueprint, render_template, request, jsonify, g
from core.security import login_required
from modules.users.models import User

search = Blueprint("search", __name__, template_folder="templates")

@search.route("/")
@login_required
def search_home():
    return render_template("search.html", page="search")

@search.get("/users")
@login_required
def search_users():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])

    # Busca apenas por username (já que não temos campo name no User)
    users = User.query.filter(
        User.username.ilike(f"%{q}%")
    ).limit(12).all()

    return jsonify([
        {
            "id": u.id,
            "username": u.username,
        }
        for u in users
        if u.id != g.user.id   # não retorna o próprio usuário
    ])
