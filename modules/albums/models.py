from core.extensions import db
from datetime import datetime

# -----------------------------------
# ÁLBUM
# -----------------------------------
class Album(db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # Fotos do álbum
    photos = db.relationship(
    "Photo",
    backref="album",
    lazy=True,
    cascade="all, delete-orphan",
    foreign_keys="Photo.album_id"
)


    # Capa do álbum (opcional)
    cover_photo_id = db.Column(db.Integer, db.ForeignKey("photos.id"), nullable=True, index=True)
    cover_photo = db.relationship(
        "Photo",
        foreign_keys=[cover_photo_id],
        uselist=False,
        post_update=True,
    )

    # Membros e convites
    members = db.relationship("AlbumMember", backref="album", lazy=True, cascade="all, delete-orphan")
    invites = db.relationship("AlbumInvite", backref="album", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Album id={self.id} name={self.name!r}>"


# -----------------------------------
# FOTO
# -----------------------------------
class Photo(db.Model):
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)

    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"), nullable=False, index=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Legenda opcional
    caption = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Photo id={self.id} album_id={self.album_id}>"


# -----------------------------------
# MEMBROS DO ÁLBUM
# -----------------------------------
class AlbumMember(db.Model):
    __tablename__ = "album_members"

    id = db.Column(db.Integer, primary_key=True)

    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    # owner | editor | viewer
    role = db.Column(db.String(16), nullable=False, default="viewer")

    joined_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Evita repetição do mesmo usuário no mesmo álbum
    __table_args__ = (
        db.UniqueConstraint("album_id", "user_id", name="uq_album_member_album_user"),
    )

    def __repr__(self):
        return f"<AlbumMember album_id={self.album_id} user_id={self.user_id} role={self.role}>"


# -----------------------------------
# CONVITES PARA ÁLBUM
# -----------------------------------
class AlbumInvite(db.Model):
    __tablename__ = "album_invites"

    id = db.Column(db.Integer, primary_key=True)

    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"), nullable=False, index=True)

    # Quem convida e quem é convidado
    inviter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    invitee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    # pending | accepted | declined
    status = db.Column(db.String(16), nullable=False, default="pending", index=True)

    # Token único para aceitar/recusar (pode ser usado em link)
    token = db.Column(db.String(64), unique=True, nullable=False, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    responded_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<AlbumInvite album_id={self.album_id} invitee_id={self.invitee_id} status={self.status}>"
