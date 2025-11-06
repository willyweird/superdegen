from flask import Blueprint, render_template, g, request, jsonify, redirect, url_for
from core.security import login_required
from core.extensions import db
from modules.chat.models import ChatThread, ChatMessage
from modules.users.models import User
from sqlalchemy import or_

chat = Blueprint("chat", __name__, template_folder="templates/chat")


# LISTA DE CONVERSAS
@chat.get("/")
@login_required
def chat_list():
    threads = ChatThread.query.filter(
        or_(ChatThread.user1_id == g.user.id, ChatThread.user2_id == g.user.id)
    ).all()

    items = []
    for t in threads:
        other = t.other_user(g.user.id)
        last = ChatMessage.query.filter_by(thread_id=t.id).order_by(ChatMessage.id.desc()).first()

        items.append({
            "id": t.id,
            "username": other.username,
            "last": last.text if last else "Comece a conversa..."
        })

    return render_template("chat/chat_list.html", chats=items, page="chat")


# ABRIR OU CRIAR CHAT
@chat.get("/start/<int:user_id>")
@login_required
def start_chat(user_id):
    if user_id == g.user.id:
        return redirect(url_for("chat.chat_list"))

    thread = ChatThread.query.filter(
        or_(
            (ChatThread.user1_id == g.user.id) & (ChatThread.user2_id == user_id),
            (ChatThread.user2_id == g.user.id) & (ChatThread.user1_id == user_id)
        )
    ).first()

    if not thread:
        thread = ChatThread(user1_id=g.user.id, user2_id=user_id)
        db.session.add(thread)
        db.session.commit()

    return redirect(url_for("chat.chat_room", thread_id=thread.id))


# SALA DE CHAT
@chat.get("/room/<int:thread_id>")
@login_required
def chat_room(thread_id):
    thread = ChatThread.query.get_or_404(thread_id)
    messages = thread.messages

    # ✅ Marcar como visto
    changed = False
    for msg in messages:
        if msg.sender_id != g.user.id and not msg.seen:
            msg.seen = True
            changed = True

    if changed:
        db.session.commit()

    return render_template("chat/chat_room.html", thread=thread, messages=messages, page="chat")


# ENVIAR MENSAGEM
@chat.post("/send/<int:thread_id>")
@login_required
def send_message(thread_id):
    text = request.json.get("text", "").strip()
    if not text:
        return jsonify({"error": "empty"}), 400

    msg = ChatMessage(thread_id=thread_id, sender_id=g.user.id, text=text)
    db.session.add(msg)
    db.session.commit()

    return jsonify({"success": True})

@chat.get("/unread_count")
@login_required
def unread_count():
    count = ChatMessage.query.join(ChatThread).filter(
        ChatMessage.sender_id != g.user.id,
        ChatMessage.seen == False,
        (ChatThread.user1_id == g.user.id) | (ChatThread.user2_id == g.user.id)
    ).count()
    return jsonify(count)
