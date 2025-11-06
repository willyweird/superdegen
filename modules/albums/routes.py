from flask import Blueprint, render_template, request, jsonify, current_app, g
from core.extensions import db
from core.security import login_required
from .models import Album, Photo
import os, uuid
from .models import Album, Photo, AlbumMember, AlbumInvite
from modules.users.models import User
import secrets
from datetime import datetime


albums = Blueprint(
    "albums",
    __name__,
    template_folder="templates"
)

# LISTA DE ÁLBUNS (Mostrar apenas os do usuário logado)
@albums.get("/")
@login_required
def albums_home():
    # Álbuns onde o usuário é dono
    owned = Album.query.filter_by(owner_id=g.user.id)

    # Álbuns onde o usuário é membro
    member = Album.query.join(AlbumMember).filter(AlbumMember.user_id == g.user.id)

    # Junta tudo
    albums_list = owned.union(member).all()

    return render_template("albums/albums.html", albums=albums_list, page="albums")


# ✅ API: Criar Álbum (Salvar dono)
@albums.post("/create")
@login_required
def create_album():
    name = request.form.get("name", "").strip()
    if not name:
        return jsonify({"error": "Nome inválido"}), 400

    album = Album(name=name, owner_id=g.user.id)   # <-- AQUI
    db.session.add(album)
    db.session.commit()

    return jsonify({"success": True, "album_id": album.id})


# ✅ API: Upload de imagem (Somente no álbum do usuário)
@albums.post("/upload/<int:album_id>")
@login_required
def upload_photo(album_id):
    role = user_role(album_id)
    if role is None:
        return jsonify({"error": "Sem acesso"}), 403

    album = Album.query.get_or_404(album_id)

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    upload_dir = os.path.join(current_app.static_folder, "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    ext = file.filename.rsplit(".", 1)[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)

    url = f"/static/uploads/{filename}"
    photo = Photo(url=url, album_id=album.id)
    db.session.add(photo)
    db.session.commit()

    return jsonify({"success": True, "url": url})

# VIEW DE UMA FOTO (Apenas se for do usuário)
@albums.get("/photo/<int:photo_id>")
@login_required
def photo_view(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    role = user_role(photo.album_id)

    if role is None:
        return "Você não tem acesso a esta foto.", 403

    return render_template("albums/photo_view.html", photo=photo, role=role)

def user_role(album_id):
    """Retorna o papel do usuário no álbum: owner, editor, viewer ou None."""
    member = AlbumMember.query.filter_by(album_id=album_id, user_id=g.user.id).first()
    album = Album.query.get(album_id)

    if album.owner_id == g.user.id:
        return "owner"

    if member:
        return member.role

    return None

@albums.get("/<int:album_id>")
@login_required
def album_view(album_id):
    role = user_role(album_id)
    if role is None:
        return "Você não tem acesso a este álbum.", 403

    album = Album.query.get_or_404(album_id)
    return render_template("albums/album_view.html", album=album, page="album-view", role=role)

@albums.post("/photo/<int:photo_id>/caption")
@login_required
def edit_caption(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    role = user_role(photo.album_id)

    if role is None:
        return jsonify({"error": "Sem acesso"}), 403

    caption = request.form.get("caption", "").strip()
    photo.caption = caption
    db.session.commit()

    return jsonify({"success": True})

@albums.post("/<int:album_id>/cover")
@login_required
def set_cover(album_id):
    album = Album.query.get_or_404(album_id)
    role = user_role(album_id)

    if role not in ("owner", "editor"):
        return jsonify({"error": "Sem permissão"}), 403

    photo_id = request.form.get("photo_id")
    album.cover_photo_id = photo_id
    db.session.commit()

    return jsonify({"success": True})

@albums.post("/<int:album_id>/rename")
@login_required
def rename_album(album_id):
    role = user_role(album_id)
    if role not in ("owner", "editor"):
        return jsonify({"error": "Sem permissão"}), 403

    name = request.form.get("name", "").strip()
    if not name:
        return jsonify({"error": "Nome inválido"}), 400

    album = Album.query.get_or_404(album_id)
    album.name = name
    db.session.commit()

    return jsonify({"success": True})


@albums.get("/<int:album_id>/members")
@login_required
def list_members(album_id):
    role = user_role(album_id)
    if role is None:
        return jsonify({"error": "Sem acesso"}), 403

    album = Album.query.get_or_404(album_id)

    members = []
    for m in album.members:
        user = User.query.get(m.user_id)
        members.append({
            "id": m.user_id,
            "username": user.username,
            "role": m.role
        })

    # inclui o dono
    owner = User.query.get(album.owner_id)
    members.append({
        "id": album.owner_id,
        "username": owner.username,
        "role": "owner"
    })

    return jsonify({"members": members})

@albums.get("/<int:album_id>/friends")
@login_required
def album_friends(album_id):
    from modules.users.models import User
    album = Album.query.get_or_404(album_id)

    # amigos do usuário
    friends = g.user.friends()

    # membros já no álbum
    member_ids = {m.user_id for m in album.members}
    member_ids.add(album.owner_id)

    available = [
        {"id": f.id, "username": f.username}
        for f in friends if f.id not in member_ids
    ]

    return jsonify({"friends": available})

@albums.post("/<int:album_id>/invite")
@login_required
def invite_member(album_id):
    role = user_role(album_id)
    if role not in ("owner", "editor"):
        return jsonify({"error": "Sem permissão"}), 403

    invitee_id = request.form.get("user_id")
    token = secrets.token_hex(16)

    invite = AlbumInvite(
        album_id=album_id,
        inviter_id=g.user.id,
        invitee_id=invitee_id,
        token=token
    )
    db.session.add(invite)
    db.session.commit()

    return jsonify({"success": True, "token": token})

@albums.post("/invites/<token>/respond")
@login_required
def respond_invite(token):
    invite = AlbumInvite.query.filter_by(token=token, status="pending").first_or_404()

    if invite.invitee_id != g.user.id:
        return jsonify({"error": "Não é seu convite"}), 403

    decision = request.form.get("decision")  # 'accept' ou 'decline'
    if decision == "accept":
        member = AlbumMember(album_id=invite.album_id, user_id=g.user.id, role="viewer")
        db.session.add(member)
        invite.status = "accepted"
    else:
        invite.status = "declined"

    invite.responded_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"success": True})
