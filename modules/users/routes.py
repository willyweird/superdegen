from flask import Blueprint, render_template, g, abort
from core.security import login_required
from modules.users.models import User

users = Blueprint(
    "users",
    __name__,
    template_folder="templates/users"
)

@users.get("/<int:user_id>")
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)

    return render_template(
        "users/profile.html",
        user=user,
        profile_user_id=user.id,  # necessário para o JS montar o botão de amizade
        page="profile"
    )
