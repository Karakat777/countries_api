import hashlib
from datetime import datetime


class User:
    def __init__(self, id, username, password_hash, role, telegram_id=None, created_at=None):
        self.id            = id
        self.username      = username
        self.password_hash = password_hash
        self.role          = role          # 'admin' | 'user'
        self.telegram_id   = telegram_id   # Новое поле для интеграции с ботом
        self.created_at    = created_at or datetime.now().isoformat()

    # ── проверка пароля ──────────────────────────────────────────────
    def check_password(self, password: str) -> bool:
        hashed = hashlib.sha256(password.encode()).hexdigest()
        return hashed == self.password_hash

    # ── сериализация ─────────────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "id":            self.id,
            "username":      self.username,
            "password_hash": self.password_hash,
            "role":          self.role,
            "telegram_id":   self.telegram_id, # Сериализация нового поля
            "created_at":    self.created_at,
        }

    # ── десериализация ───────────────────────────────────────────────
    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            id            = data["id"],
            username      = data["username"],
            password_hash = data["password_hash"],
            role          = data["role"],
            telegram_id   = data.get("telegram_id"), # Десериализация нового поля
            created_at    = data.get("created_at"),
        )

    def __repr__(self):
        return f"<User id={self.id} username={self.username} role={self.role} tg={self.telegram_id}>"