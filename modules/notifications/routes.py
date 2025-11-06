from flask import Blueprint, render_template, g, jsonify
from core.security import login_required
from core.extensions import db
from modules.notifications.models import Notification
from modules.users.models import User
from modules.social.models import Friendship

notifications = Blueprint(
    "notifications",
    __name__,
    template_folder="templates/notifications"
)

@notifications.route("/")
@login_required
def notifications_home():

    # ✅ Buscar pedidos de amizade pendentes (origem: tabela friendships)
    pending = Friendship.query.filter_by(
        receiver_id=g.user.id,
        status="pending"
    ).order_by(Friendship.created_at.desc()).all()

    data = []
    for f in pending:
        from_user = User.query.get(f.requester_id)
        data.append({
            "user_id": f.requester_id,
            "username": from_user.username if from_user else "Alguém"
        })

    # ✅ Marcar notificações como vistas sem remover da lista
    Notification.query.filter_by(
        user_id=g.user.id,
        type="friend_request",
        seen=False
    ).update({ "seen": True })
    db.session.commit()

    return render_template(
        "notifications/notifications.html",
        notifications=data,
        page="notifications"
    )


@notifications.get("/count")
@login_required
def notifications_count():
    count = Notification.query.filter_by(
        user_id=g.user.id,
        seen=False,
        type="friend_request"
    ).count()
    return jsonify(count)
