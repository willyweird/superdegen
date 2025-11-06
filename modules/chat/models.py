from core.extensions import db
from datetime import datetime

class ChatThread(db.Model):
    __tablename__ = "chat_threads"

    id = db.Column(db.Integer, primary_key=True)

    user1_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Ordena mensagens automaticamente por ID
    messages = db.relationship(
        "ChatMessage",
        backref="thread",
        cascade="all, delete-orphan",
        order_by="ChatMessage.id"
    )

    user1 = db.relationship("User", foreign_keys=[user1_id], backref="chats_as_u1")
    user2 = db.relationship("User", foreign_keys=[user2_id], backref="chats_as_u2")

    __table_args__ = (
        db.UniqueConstraint("user1_id", "user2_id", name="unique_chat_thread"),
    )

    def other_user(self, user_id):
        """Retorna o outro participante da conversa."""
        return self.user2 if self.user1_id == user_id else self.user1


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey("chat_threads.id", ondelete="CASCADE"))
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    sender = db.relationship("User", foreign_keys=[sender_id])

    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    seen = db.Column(db.Boolean, default=False)
