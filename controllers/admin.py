from services.db_service  import DatabaseService
from services.bot_service import BotService


class AdminController:
    def __init__(self, db: DatabaseService, bot: BotService):
        self.db  = db
        self.bot = bot

    # ── пользователи ─────────────────────────────────────────────────
    def list_users(self):
        return self.db.get_all_users()

    def create_user(self, username: str, password: str, role: str = "user"):
        import hashlib, uuid
        from models.user import User

        if self.db.find_by_username(username):
            return False, "Username already exists"

        pw_hash  = hashlib.sha256(password.encode()).hexdigest()
        new_user = User(str(uuid.uuid4()), username, pw_hash, role)
        self.db.add_user(new_user)
        self.bot.notify_admin_action("created_user", f"username={username} role={role}")
        return True, new_user

    def delete_user(self, user_id, current_admin_id) -> tuple[bool, str]:
        if str(user_id) == str(current_admin_id):
            return False, "You cannot delete yourself"

        user = self.db.find_by_id(user_id)
        if not user:
            return False, "User not found"

        self.db.delete_user_by_id(user_id)
        self.db.delete_records_by_user(user_id)   # удаляем и его записи
        self.bot.notify_admin_action("deleted_user", f"id={user_id} username={user.username}")
        return True, "Deleted"

    # ── записи ───────────────────────────────────────────────────────
    def list_all_records(self, page: int = 1, per_page: int = 10):
        all_records  = self.db.get_all_records()
        total        = len(all_records)
        total_pages  = max(1, (total + per_page - 1) // per_page)
        start        = (page - 1) * per_page
        page_records = all_records[start:start + per_page]
        return page_records, total, total_pages
