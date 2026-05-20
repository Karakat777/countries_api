import logging
import telebot
from config import Config


class BotService:
    def __init__(self):
        self.token   = Config.BOT_TOKEN
        self.chat_id = Config.CHAT_ID

    def notify_new_user(self, username: str):
        """Вызывается когда новый пользователь регистрируется."""
        self._send(f"🌍 New user registered: *{username}*")

    def notify_admin_action(self, action: str, detail: str):
        """Вызывается когда admin делает важное действие."""
        self._send(f"⚡ Admin action: *{action}*\n└ {detail}")

    # ── внутренний метод отправки ─────────────────────────────────────
    def _send(self, text: str):
        try:
            bot = telebot.TeleBot(self.token)
            bot.send_message(self.chat_id, text, parse_mode="Markdown")
        except Exception as e:
            # НЕ крашим приложение — только логируем
            logging.error(f"[BotService] Failed to send message: {e}")
