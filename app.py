import os
import sqlite3
from functools import wraps

from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash, g)
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

app = Flask(__name__)
app.secret_key = "өөрийн-нууц-түлхүүрээ-энд-солино-уу"


# ---------- Мэдээллийн сан (SQLite) ----------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            aimag TEXT,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
    )
    db.commit()
    db.close()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Эхлээд нэвтэрнэ үү.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


# ---------- Жишээ өгөгдөл ----------
PRODUCTS = [
    {"name": "Үхрийн мах", "cat": "Мал аж ахуй", "price": "18,000₮ / кг", "icon": "🥩"},
    {"name": "Хонины мах", "cat": "Мал аж ахуй", "price": "14,000₮ / кг", "icon": "🐑"},
    {"name": "Айраг", "cat": "Сүү, цагаан идээ", "price": "6,000₮ / л", "icon": "🥛"},
    {"name": "Ааруул", "cat": "Сүү, цагаан идээ", "price": "12,000₮ / кг", "icon": "🧀"},
    {"name": "Төмс", "cat": "Газар тариалан", "price": "2,500₮ / кг", "icon": "🥔"},
    {"name": "Лууван", "cat": "Газар тариалан", "price": "2,800₮ / кг", "icon": "🥕"},
    {"name": "Улаан лооль", "cat": "Хүлэмжийн ногоо", "price": "7,000₮ / кг", "icon": "🍅"},
    {"name": "Гурил", "cat": "Үр тариа", "price": "3,200₮ / кг", "icon": "🌾"},
]

NEWS = [
    {"title": "Хаврын тариалалтад бэлдэх 5 зөвлөгөө",
     "date": "2026.03.10",
     "text": "Хөрсөө шинжлүүлж, үрээ сорьж, тоног төхөөрөмжөө урьдчилан засварлаж бэлдээрэй."},
    {"title": "Малын өвөл, хаврын хяналт",
     "date": "2026.02.22",
     "text": "Өвөлжилтийн үед хүйтнээс хамгаалж, өвс тэжээлийн нөөцөө тооцож байх нь чухал."},
    {"title": "Хүлэмжийн ногооны арчилгаа",
     "date": "2026.01.15",
     "text": "Температур, чийгшлийг тогтмол хэмжиж, усалгааг тунг баримтлан хийнэ."},
]

AIMAGS = ["Улаанбаатар", "Архангай", "Баян-Өлгий", "Баянхонгор", "Булган",
          "Говь-Алтай", "Говьсүмбэр", "Дархан-Уул", "Дорноговь", "Дорнод",
          "Дундговь", "Завхан", "Орхон", "Өвөрхангай", "Өмнөговь", "Сүхбаатар",
          "Сэлэнгэ", "Төв", "Увс", "Ховд", "Хөвсгөл", "Хэнтий"]

CALENDAR = [
    ("Хавар", "Тариалалт, мал төллөлт, хөрс боловсруулалт"),
    ("Зун", "Услалт, хогийн ургамал устгах, өвс бэлтгэл"),
    ("Намар", "Ургац хураалт, мал таргалуулалт, ногоо хадгалалт"),
    ("Өвөл", "Өвөлжилт, малын тэжээл, тоног төхөөрөмжийн засвар"),
]


# ---------- Хуудсууд ----------
@app.route("/")
def home():
    return render_template("index.html", news=NEWS, products=PRODUCTS[:4])


@app.route("/products")
def products():
    cats = sorted({p["cat"] for p in PRODUCTS})
    selected = request.args.get("cat")
    items = [p for p in PRODUCTS if not selected or p["cat"] == selected]
    return render_template("products.html", items=items, cats=cats, selected=selected)


@app.route("/news")
def news():
    return render_template("news.html", news=NEWS)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Таны мессежийг хүлээн авлаа. Баярлалаа!", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")


# ---------- Нэвтрэх / Бүртгүүлэх ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        aimag = request.form.get("aimag", "")

        if not fullname or not username or not password:
            flash("Бүх талбарыг бөглөнө үү.", "error")
        elif len(password) < 6:
            flash("Нууц үг дор хаяж 6 тэмдэгттэй байх ёстой.", "error")
        elif password != confirm:
            flash("Нууц үг хоёр талбарт таарахгүй байна.", "error")
        else:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO users (fullname, username, password, aimag) VALUES (?,?,?,?)",
                    (fullname, username, generate_password_hash(password), aimag),
                )
                db.commit()
                flash("Амжилттай бүртгэгдлээ. Одоо нэвтэрнэ үү.", "success")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("Энэ нэвтрэх нэр аль хэдийн бүртгэгдсэн байна.", "error")
    return render_template("register.html", aimags=AIMAGS)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_db().execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        if user and check_password_hash(user["password"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["fullname"] = user["fullname"]
            flash(f"Тавтай морил, {user['fullname']}!", "success")
            return redirect(url_for("dashboard"))
        flash("Нэвтрэх нэр эсвэл нууц үг буруу байна.", "error")
    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    user = get_db().execute(
        "SELECT * FROM users WHERE id = ?", (session["user_id"],)
    ).fetchone()
    return render_template("dashboard.html", user=user, calendar=CALENDAR)


@app.route("/logout")
def logout():
    session.clear()
    flash("Системээс гарлаа.", "success")
    return redirect(url_for("home"))


init_db()

if __name__ == "__main__":
    app.run(debug=True)
