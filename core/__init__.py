from flask import Flask, request, redirect, url_for, g
from flask_babel import Babel
import os

from core.config import Config, DB_PATH
from core.extensions import db
from core.security import get_current_user

# Importar Blueprints
from modules.home.routes import home
from modules.matches.routes import matches
from modules.search.routes import search
from modules.profile.routes import profile
from modules.notifications.routes import notifications
from modules.chat.routes import chat
from modules.auth.routes import auth
from modules.users.routes import users
from modules.social.routes import social

# Importar Models (ANTES do create_all)
from modules.users.models import User
from modules.matches.models import League, LeagueStanding, Match, Tournament

babel = Babel()

PUBLIC_ENDPOINTS = {
    "auth.login",
    "auth.signup",
    "auth.logout"
}

def get_locale():
    return "pt"  # mais tarde: preferências do usuário


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    app.config.from_object(Config)
    db.init_app(app)

    babel.init_app(app, locale_selector=get_locale)

    # Registrar Blueprints
    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(matches, url_prefix="/matches")
    app.register_blueprint(search, url_prefix="/search")
    app.register_blueprint(profile, url_prefix="/profile")
    app.register_blueprint(notifications, url_prefix="/notifications")
    app.register_blueprint(chat, url_prefix="/chat")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(users, url_prefix="/users")
    app.register_blueprint(social, url_prefix="/social")


    # ✅ VERIFICA LOGIN AUTOMATICAMENTE
    @app.before_request
    def global_auth_check():
        g.user = get_current_user()

        # Se endpoint não existe → não bloquear
        if not request.endpoint:
            return

        # Se rota é pública → permitir
        if request.endpoint in PUBLIC_ENDPOINTS:
            return

        # Se é arquivo estático → permitir
        if request.endpoint.startswith("static"):
            return

        # Se usuário não está logado → redirecionar
        if g.user is None:
            return redirect(url_for("auth.login"))


    # ✅ Criar tabelas somente se o banco **ainda não existir**
    with app.app_context():
        if not os.path.exists(DB_PATH):
            db.create_all()


    return app
