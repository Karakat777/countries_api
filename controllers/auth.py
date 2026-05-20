import hashlib
import uuid
from functools import wraps

from flask import session, redirect, url_for, abort

from models.user import User
from services.db_service  import DatabaseService
from services.bot_service import BotService


# ════════════════════════════════════════════════════════════════
#  DECORATOR
# ════════════════════════════════════════════════════════════════
def login_required(role=None):
    """
    Использование:
        @login_required()              — любой залогиненный
        @login_required(role='admin')  — только admin
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login_page"))
            if role == "admin" and session.get("role") != "admin":
                abort(403)
            return f(*args, **kwargs)
        return decorated
    return decorator


# ════════════════════════════════════════════════════════════════
#  AUTH CONTROLLER
# ════════════════════════════════════════════════════════════════
class AuthController:
    def __init__(self, db: DatabaseService, bot: BotService):
        self.db  = db
        self.bot = bot

    # ── login ────────────────────────────────────────────────────────
    def login(self, username: str, password: str) -> bool:
        user = self.db.find_by_username(username)
        if user and user.check_password(password):
            session["user_id"]  = user.id
            session["role"]     = user.role
            session["username"] = user.username
            return True
        return False

    # ── logout ───────────────────────────────────────────────────────
    def logout(self):
        session.clear()

    # ── register ─────────────────────────────────────────────────────
    def register(self, username: str, password: str, telegram_id: str = None) -> tuple[bool, str]:
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters"
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters"
        if self.db.find_by_username(username):
            return False, "Username already exists"

        pw_hash  = hashlib.sha256(password.encode()).hexdigest()
        new_user = User(
            id            = str(uuid.uuid4()),
            username      = username,
            password_hash = pw_hash,
            role          = "user",
            telegram_id   = telegram_id if telegram_id else None # Сохраняем Telegram ID
        )
        self.db.add_user(new_user)
        self.bot.notify_new_user(username)   # Уведомление админа в Telegram
        return True, "OK"