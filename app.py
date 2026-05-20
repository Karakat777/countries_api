from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

from config import Config
from services.db_service import DatabaseService
from services.bot_service import BotService
from controllers.auth import AuthController, login_required
from controllers.admin import AdminController
from controllers.user import UserController

# ── инициализация ────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

db = DatabaseService()
bot = BotService()

auth_ctrl = AuthController(db, bot)
admin_ctrl = AdminController(db, bot)
user_ctrl = UserController(db)


# ════════════════════════════════════════════════════════════════════
#  ГЛАВНАЯ
# ════════════════════════════════════════════════════════════════════
@app.route("/")
def index():
    if "user_id" in session:
        if session.get("role") == "admin":
            return redirect(url_for("admin_dashboard"))
        return redirect(url_for("user_dashboard"))
    return redirect(url_for("login_page"))


# ════════════════════════════════════════════════════════════════════
#  AUTH
# ════════════════════════════════════════════════════════════════════
@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if auth_ctrl.login(username, password):
            return redirect(url_for("index"))
        flash("Invalid username or password", "error")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        telegram_id = request.form.get("telegram_id", "").strip()  # Получаем Telegram ID из формы

        # Передаем telegram_id в контроллер регистрации
        ok, msg = auth_ctrl.register(username, password, telegram_id)
        if ok:
            flash("Account created! Please log in.", "success")
            return redirect(url_for("login_page"))
        flash(msg, "error")
    return render_template("register.html")


@app.route("/logout")
def logout():
    auth_ctrl.logout()
    return redirect(url_for("login_page"))


# ════════════════════════════════════════════════════════════════════
#  ADMIN ROUTES
# ════════════════════════════════════════════════════════════════════
@app.route("/admin/dashboard")
@login_required(role="admin")
def admin_dashboard():
    users = admin_ctrl.list_users()
    recs, total, _ = admin_ctrl.list_all_records(per_page=9999)
    recent = sorted(users, key=lambda u: u.created_at, reverse=True)[:5]
    return render_template("admin/dashboard.html",
                           total_users=len(users),
                           total_records=total,
                           recent=recent)


@app.route("/admin/users")
@login_required(role="admin")
def admin_users():
    users = admin_ctrl.list_users()
    return render_template("admin/users.html", users=users)


@app.route("/admin/users/create", methods=["POST"])
@login_required(role="admin")
def admin_create_user():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    role = request.form.get("role", "user")
    ok, result = admin_ctrl.create_user(username, password, role)
    flash(f"User '{username}' created." if ok else result,
          "success" if ok else "error")
    return redirect(url_for("admin_users"))


@app.route("/admin/users/delete/<user_id>", methods=["POST"])
@login_required(role="admin")
def admin_delete_user(user_id):
    ok, msg = admin_ctrl.delete_user(user_id, session["user_id"])
    flash(msg if not ok else f"User deleted.", "error" if not ok else "success")
    return redirect(url_for("admin_users"))


@app.route("/admin/data")
@login_required(role="admin")
def admin_data():
    page = int(request.args.get("page", 1))
    records, total, total_pages = admin_ctrl.list_all_records(page=page)
    return render_template("admin/data.html",
                           records=records,
                           page=page,
                           total_pages=total_pages)


# ── API для live-search (main.js fetch) ──────────────────────────────
@app.route("/api/users/search")
@login_required(role="admin")
def api_search_users():
    q = request.args.get("q", "").lower()
    users = admin_ctrl.list_users()
    if q:
        users = [u for u in users if q in u.username.lower()]
    return jsonify([u.to_dict() for u in users])


# ════════════════════════════════════════════════════════════════════
#  USER ROUTES
# ════════════════════════════════════════════════════════════════════
@app.route("/user/dashboard")
@login_required()
def user_dashboard():
    records = user_ctrl.get_my_records(session["user_id"])
    return render_template("user/dashboard.html", records=records)


@app.route("/user/profile", methods=["GET", "POST"])
@login_required()
def user_profile():
    if request.method == "POST":
        new_pw = request.form.get("password", "")
        ok, msg = user_ctrl.update_profile(session["user_id"], new_pw)
        flash(msg, "success" if ok else "error")
        return redirect(url_for("user_profile"))

    user, record_count = user_ctrl.get_profile(session["user_id"])
    return render_template("user/profile.html",
                           user=user, record_count=record_count)


@app.route("/user/records/add", methods=["POST"])
@login_required()
def user_add_record():
    data = {
        "name": request.form.get("name", "").strip(),
        "capital": request.form.get("capital", "").strip(),
        "population": request.form.get("population", 0),
        "year": request.form.get("year", 0),
    }
    try:
        data["population"] = int(data["population"])
        data["year"] = int(data["year"])
    except ValueError:
        flash("Population and Year must be numbers.", "error")
        return redirect(url_for("user_dashboard"))

    ok, result = user_ctrl.add_record(session["user_id"], data)
    flash(f"Country '{data['name']}' added!" if ok else result,
          "success" if ok else "error")
    return redirect(url_for("user_dashboard"))


# ════════════════════════════════════════════════════════════════════
#  НОВОЕ: BOT REST API ENDPOINTS (Связующее звено Бот ↔ Сайт)
# ════════════════════════════════════════════════════════════════════
@app.route("/api/bot/countries", methods=["GET", "POST"])
def bot_countries():
    tg_id = request.headers.get("X-Telegram-ID")
    if not tg_id:
        return jsonify({"error": "Missing X-Telegram-ID header"}), 400

    # Ищем пользователя по его Telegram ID
    users = db.get_all_users()
    user = next((u for u in users if u.telegram_id and str(u.telegram_id) == str(tg_id)), None)

    if not user:
        return jsonify({"error": "Telegram ID not linked to any web account."}), 403

    # POST: Бот сохраняет страну через пошаговый диалог
    if request.method == "POST":
        data = request.json
        ok, result = user_ctrl.add_record(user.id, data)
        if ok:
            # Отправляем уведомление админу через BotService (Требование Task 6)
            bot.notify_admin_action("Bot Entry Added",
                                    f"User @{user.username} saved country via bot: {data.get('name')}")
            return jsonify({"status": "success", "record": result.to_dict()}), 201
        return jsonify({"error": result}), 400

    # GET: Бот запрашивает список сохраненных стран (или ищет по столице)
    elif request.method == "GET":
        capital_query = request.args.get("capital")
        records = user_ctrl.get_my_records(user.id)

        # Если это бонусный поиск /search <capital> в боте
        if capital_query:
            records = [r for r in records if r.capital.lower() == capital_query.lower()]

        return jsonify({"countries": [r.to_dict() for r in records]}), 200


@app.route("/api/bot/countries/<int:record_id>", methods=["DELETE"])
def bot_delete_country(record_id):
    tg_id = request.headers.get("X-Telegram-ID")
    if not tg_id:
        return jsonify({"error": "Missing ID"}), 400

    users = db.get_all_users()
    user = next((u for u in users if u.telegram_id and str(u.telegram_id) == str(tg_id)), None)
    if not user:
        return jsonify({"error": "Unauthorized"}), 403

    records = db.get_all_records()
    new_records = []
    deleted = False

    for r in records:
        if r.id == record_id and str(r.user_id) == str(user.id):
            deleted = True
        else:
            new_records.append(r)

    if deleted:
        db.save_all_records(new_records)
        bot.notify_admin_action("Bot Entry Deleted", f"User @{user.username} deleted a record via bot.")
        return jsonify({"message": "Deleted successfully"}), 200

    return jsonify({"error": "Record not found or access denied"}), 404


# ════════════════════════════════════════════════════════════════════
#  ERROR PAGES
# ════════════════════════════════════════════════════════════════════
@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


# ════════════════════════════════════════════════════════════════════
#  ЗАПУСК
# ════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Порт 5001 сохранен из вашей конфигурации
    app.run(debug=Config.DEBUG, host="0.0.0.0", port=5001)