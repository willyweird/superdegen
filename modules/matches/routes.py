from datetime import datetime

from flask import Blueprint, jsonify, render_template, request, g

from core.extensions import db
from core.security import login_required
from modules.users.models import User

from .models import League, LeagueStanding, Match, Tournament


matches = Blueprint("matches", __name__, template_folder="templates")


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None

    for fmt in ("%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


@matches.get("/")
@login_required
def matches_home():
    match_list = sorted(
        Match.query.all(),
        key=lambda match: (
            match.scheduled_for is None,
            match.scheduled_for or datetime.max,
        ),
    )

    tournament_list = sorted(
        Tournament.query.all(),
        key=lambda tournament: (
            tournament.start_date is None,
            tournament.start_date or datetime.max,
        ),
    )

    league_list = sorted(
        League.query.all(),
        key=lambda league: league.created_at or datetime.min,
        reverse=True,
    )

    return render_template(
        "matches/matches.html",
        page="matches",
        matches=match_list,
        tournaments=tournament_list,
        leagues=league_list,
    )


@matches.post("/create")
@login_required
def create_match():
    title = request.form.get("title", "").strip()
    opponents = request.form.get("opponents", "").strip()
    league = request.form.get("league", "").strip() or None
    game = request.form.get("game", "").strip() or None
    stage = request.form.get("stage", "").strip() or None
    status = request.form.get("status", "").strip() or "scheduled"
    if status not in {"scheduled", "live", "finished"}:
        status = "scheduled"
    scheduled_for = _parse_datetime(request.form.get("scheduled_for"))

    if not title or not opponents:
        return jsonify({"error": "Informe título e adversários"}), 400

    match = Match(
        title=title,
        opponents=opponents,
        league=league,
        game=game,
        stage=stage,
        status=status,
        scheduled_for=scheduled_for,
        created_by_id=g.user.id if isinstance(g.user, User) else None,
    )

    db.session.add(match)
    db.session.commit()

    return jsonify({"success": True, "match_id": match.id})


@matches.post("/<int:match_id>/result")
@login_required
def update_match_result(match_id: int):
    match = Match.query.get_or_404(match_id)

    if match.created_by_id and g.user.id != match.created_by_id:
        return jsonify({"error": "Sem permissão"}), 403

    status = request.form.get("status", "").strip() or match.status
    if status not in {"scheduled", "live", "finished"}:
        status = match.status
    result = request.form.get("result", "").strip() or None
    summary = request.form.get("summary", "").strip() or None

    match.status = status
    match.result = result
    match.summary = summary

    db.session.commit()

    return jsonify({"success": True})


@matches.get("/<int:match_id>")
@login_required
def match_view(match_id: int):
    match = Match.query.get_or_404(match_id)
    return render_template("matches/match_view.html", page="match-view", match=match)


@matches.get("/tournaments/<int:tournament_id>")
@login_required
def tournament_view(tournament_id: int):
    tournament = Tournament.query.get_or_404(tournament_id)
    related_matches = (
        Match.query.filter(Match.league == tournament.name)
        .order_by(Match.scheduled_for.asc())
        .all()
    )
    return render_template(
        "matches/tournament_view.html",
        page="tournament-view",
        tournament=tournament,
        matches=related_matches,
    )


@matches.get("/leagues/<int:league_id>")
@login_required
def league_view(league_id: int):
    league = League.query.get_or_404(league_id)
    standings = league.standings
    recent_matches = (
        Match.query.filter(Match.league == league.name)
        .order_by(Match.scheduled_for.desc())
        .limit(6)
        .all()
    )
    return render_template(
        "matches/league_view.html",
        page="league-view",
        league=league,
        standings=standings,
        matches=recent_matches,
    )


@matches.get("/leagues/<int:league_id>/standings")
@login_required
def league_standings_api(league_id: int):
    league = League.query.get_or_404(league_id)
    payload = [
        {
            "position": standing.position,
            "team": standing.team_name,
            "wins": standing.wins,
            "losses": standing.losses,
            "draws": standing.draws,
            "points": standing.points,
        }
        for standing in league.standings
    ]
    return jsonify({"league": league.name, "standings": payload})
