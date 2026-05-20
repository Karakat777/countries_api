import hashlib

from models.record       import Record
from services.db_service import DatabaseService
from validation          import validate_country   # реиспользуем из Assignment 3


class UserController:
    def __init__(self, db: DatabaseService):
        self.db = db

    # ── профиль ──────────────────────────────────────────────────────
    def get_profile(self, user_id):
        user    = self.db.find_by_id(user_id)
        records = self.db.get_records_by_user(user_id)
        return user, len(records)

    def update_profile(self, user_id, new_password: str) -> tuple[bool, str]:
        if len(new_password) < 6:
            return False, "Password must be at least 6 characters"

        users = self.db.get_all_users()
        for user in users:
            if str(user.id) == str(user_id):
                user.password_hash = hashlib.sha256(new_password.encode()).hexdigest()
                self.db.save_all_users(users)
                return True, "Password updated"

        return False, "User not found"

    # ── записи ───────────────────────────────────────────────────────
    def get_my_records(self, user_id):
        return self.db.get_records_by_user(user_id)

    def add_record(self, user_id, data: dict) -> tuple[bool, any]:
        # валидация — тот же validate_country из Assignment 3
        error = validate_country(data, partial=False)
        if error:
            return False, error

        records = self.db.get_all_records()
        new_id  = max((r.id for r in records), default=0) + 1

        record = Record(
            id         = new_id,
            name       = data["name"].strip(),
            population = data["population"],
            capital    = data["capital"].strip(),
            year       = data["year"],
            user_id    = user_id,
        )
        self.db.add_record(record)
        return True, record
