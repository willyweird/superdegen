from flask import Blueprint, jsonify, g
from core.extensions import db
from core.security import login_required
from modules.social.models import Friendship
from modules.notifications.models import Notification
from sqlalchemy import and_, or_

social = Blueprint("social", __name__)


# ✅ STATUS (necessário pro botão no perfil e search)
@social.get("/friendship/status/<int:user_id>")
@login_required
def friendship_status(user_id):
    f = Friendship.query.filter(
        or_(
            and_(Friendship.requester_id == g.user.id, Friendship.receiver_id == user_id),
            and_(Friendship.requester_id == user_id, Friendship.receiver_id == g.user.id)
        )
    ).first()

    if not f:
        return jsonify({"status": "none"})

    return jsonify({
        "status": f.status,
        "requester": f.requester_id
    })


# ✅ ENVIAR SOLICITAÇÃO
@social.post("/friendship/send/<int:user_id>")
@login_required
def send_friend_request(user_id):
    if g.user.id == user_id:
        return jsonify({"error": "Você não pode adicionar você mesmo."}), 400

    existing = Friendship.query.filter(
        or_(
            and_(Friendship.requester_id == g.user.id, Friendship.receiver_id == user_id),
            and_(Friendship.requester_id == user_id, Friendship.receiver_id == g.user.id)
        )
    ).first()

    if existing:
        return jsonify({"error": "Pedido já existe ou já são amigos."}), 400

    friendship = Friendship(
        requester_id=g.user.id,
        receiver_id=user_id,
        status="pending"
    )
    db.session.add(friendship)

    # ✅ Cria notificação para o outro usuário
    notif = Notification(
        user_id=user_id,
        from_user_id=g.user.id,
        type="friend_request"
    )
    db.session.add(notif)

    db.session.commit()
    return jsonify({"success": True, "status": "pending"}), 200


# ✅ CANCELAR SOLICITAÇÃO
@social.post("/friendship/cancel/<int:user_id>")
@login_required
def cancel_friend_request(user_id):
    friendship = Friendship.query.filter_by(
        requester_id=g.user.id,
        receiver_id=user_id,
        status="pending"
    ).first()

    if not friendship:
        return jsonify({"error": "Nenhum pedido para cancelar."}), 400

    # Remove solicitação
    db.session.delete(friendship)

    # Remove notificação associada
    notif = Notification.query.filter_by(
        user_id=user_id,
        from_user_id=g.user.id,
        type="friend_request",
        seen=False
    ).first()
    if notif:
        db.session.delete(notif)

    db.session.commit()
    return jsonify({"success": True}), 200


# ✅ ACEITAR SOLICITAÇÃO
@social.post("/friendship/accept/<int:user_id>")
@login_required
def accept_friend_request(user_id):
    friendship = Friendship.query.filter_by(
        requester_id=user_id,
        receiver_id=g.user.id,
        status="pending"
    ).first()

    if not friendship:
        return jsonify({"error": "Nenhum pedido para aceitar."}), 400

    friendship.status = "accepted"

    # ✅ Remove notificação de pedido
    notif = Notification.query.filter_by(
        user_id=g.user.id,
        from_user_id=user_id,
        type="friend_request",
        seen=False
    ).first()
    if notif:
        db.session.delete(notif)

    db.session.commit()
    return jsonify({"success": True, "status": "accepted"}), 200


# ✅ RECUSAR SOLICITAÇÃO
@social.post("/friendship/decline/<int:user_id>")
@login_required
def decline_friend_request(user_id):
    friendship = Friendship.query.filter_by(
        requester_id=user_id,
        receiver_id=g.user.id,
        status="pending"
    ).first()

    if not friendship:
        return jsonify({"error": "Nenhum pedido para recusar."}), 400

    db.session.delete(friendship)

    # ✅ Remove notificação também
    notif = Notification.query.filter_by(
        user_id=g.user.id,
        from_user_id=user_id,
        type="friend_request",
        seen=False
    ).first()
    if notif:
        db.session.delete(notif)

    db.session.commit()
    return jsonify({"success": True}), 200


# ✅ REMOVER AMIGO
@social.post("/friendship/remove/<int:user_id>")
@login_required
def remove_friend(user_id):
    friendship = Friendship.query.filter(
        or_(
            and_(Friendship.requester_id == g.user.id, Friendship.receiver_id == user_id, Friendship.status == "accepted"),
            and_(Friendship.requester_id == user_id, Friendship.receiver_id == g.user.id, Friendship.status == "accepted")
        )
    ).first()

    if not friendship:
        return jsonify({"error": "Vocês não são amigos."}), 400

    db.session.delete(friendship)
    db.session.commit()
    return jsonify({"success": True}), 200
