import json
import os
from models.user   import User
from models.record import Record


class DatabaseService:
    def __init__(self):
        base = os.path.dirname(os.path.abspath(__file__))
        self._users_path   = os.path.join(base, "../data/users.json")
        self._records_path = os.path.join(base, "../data/records.json")

    # ════════════════════════════════════════════════════════
    #  USERS
    # ════════════════════════════════════════════════════════
    def get_all_users(self) -> list[User]:
        return [User.from_dict(d) for d in self._read(self._users_path)]

    def save_all_users(self, users: list[User]):
        self._write(self._users_path, [u.to_dict() for u in users])

    def find_by_username(self, username: str) -> User | None:
        return next(
            (u for u in self.get_all_users() if u.username == username),
            None
        )

    def find_by_id(self, user_id) -> User | None:
        return next(
            (u for u in self.get_all_users() if str(u.id) == str(user_id)),
            None
        )

    def add_user(self, user: User):
        users = self.get_all_users()
        users.append(user)
        self.save_all_users(users)

    def delete_user_by_id(self, user_id):
        users = [u for u in self.get_all_users() if str(u.id) != str(user_id)]
        self.save_all_users(users)

    # ════════════════════════════════════════════════════════
    #  RECORDS
    # ════════════════════════════════════════════════════════
    def get_all_records(self) -> list[Record]:
        return [Record.from_dict(d) for d in self._read(self._records_path)]

    def save_all_records(self, records: list[Record]):
        self._write(self._records_path, [r.to_dict() for r in records])

    def get_records_by_user(self, user_id) -> list[Record]:
        return [r for r in self.get_all_records() if str(r.user_id) == str(user_id)]

    def add_record(self, record: Record):
        records = self.get_all_records()
        records.append(record)
        self.save_all_records(records)

    def delete_records_by_user(self, user_id):
        records = [r for r in self.get_all_records() if str(r.user_id) != str(user_id)]
        self.save_all_records(records)

    # ════════════════════════════════════════════════════════
    #  HELPERS (бывший storage.py)
    # ════════════════════════════════════════════════════════
    def _read(self, path: str) -> list:
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def _write(self, path: str, data: list):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
