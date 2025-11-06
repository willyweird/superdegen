from flask import Blueprint, render_template
from core.security import login_required  # <-- adiciona isso
from modules.users.models import User
from flask import g


profile = Blueprint(
    "profile",
    __name__,
    template_folder="templates"
)

@profile.route("/")
@login_required
def profile_home():
    user = {"name": "Usuário", "username": "@user"}  # depois vamos ligar ao banco
    return render_template("profile/profile.html", user=user)

@profile.route("/<int:user_id>")
@login_required
def view_profile(user_id):
    # Se o usuário abrir o próprio /profile/<id>, redireciona para /profile
    if g.user.id == user_id:
        return render_template("profile/profile.html", user=g.user)

    user = User.query.get_or_404(user_id)
    return render_template("users/profile.html", user=user)
