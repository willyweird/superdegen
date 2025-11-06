from datetime import datetime

from core.extensions import db


class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    opponents = db.Column(db.String(160), nullable=False)
    league = db.Column(db.String(120), nullable=True)
    game = db.Column(db.String(80), nullable=True)
    stage = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(32), nullable=False, default="scheduled")
    result = db.Column(db.String(80), nullable=True)
    summary = db.Column(db.Text, nullable=True)
    scheduled_for = db.Column(db.DateTime, nullable=True)
    cover_image = db.Column(db.String(255), nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    created_by = db.relationship("User", backref="matches", foreign_keys=[created_by_id])

    def __repr__(self) -> str:
        return f"<Match id={self.id} title={self.title!r} status={self.status!r}>"


class Tournament(db.Model):
    __tablename__ = "tournaments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    organizer = db.Column(db.String(160), nullable=True)
    prize_pool = db.Column(db.String(120), nullable=True)
    game = db.Column(db.String(80), nullable=True)
    location = db.Column(db.String(120), nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.Text, nullable=True)
    banner_image = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Tournament id={self.id} name={self.name!r}>"


class League(db.Model):
    __tablename__ = "leagues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    region = db.Column(db.String(80), nullable=True)
    season = db.Column(db.String(80), nullable=True)
    game = db.Column(db.String(80), nullable=True)
    description = db.Column(db.Text, nullable=True)
    emblem_image = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    standings = db.relationship(
        "LeagueStanding",
        backref="league",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="LeagueStanding.position",
    )

    def __repr__(self) -> str:
        return f"<League id={self.id} name={self.name!r}>"


class LeagueStanding(db.Model):
    __tablename__ = "league_standings"

    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, db.ForeignKey("leagues.id"), nullable=False, index=True)
    position = db.Column(db.Integer, nullable=False, default=1)
    team_name = db.Column(db.String(160), nullable=False)
    wins = db.Column(db.Integer, nullable=False, default=0)
    losses = db.Column(db.Integer, nullable=False, default=0)
    draws = db.Column(db.Integer, nullable=False, default=0)
    points = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self) -> str:
        return (
            f"<LeagueStanding league_id={self.league_id} position={self.position} "
            f"team={self.team_name!r}>"
        )
