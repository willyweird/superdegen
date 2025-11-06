from core.extensions import db
from datetime import datetime


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    # Usuário que RECEBE a notificação
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # Usuário que GEROU a notificação (ex.: quem enviou pedido)
    from_user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    # Tipo da notificação: ex: "friend_request", "like", "comment", etc.
    type = db.Column(db.String(50), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ Se já foi visualizada
    seen = db.Column(db.Boolean, default=False)

    # ✅ Facilita acessar via notificação.user e notificação.from_user
    user = db.relationship("User", foreign_keys=[user_id], backref="notifications_received")
    from_user = db.relationship("User", foreign_keys=[from_user_id], backref="notifications_sent")

    def __repr__(self):
        return f"<Notification id={self.id} type={self.type} to={self.user_id} from={self.from_user_id}>"
