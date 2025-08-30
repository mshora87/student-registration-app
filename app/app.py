import os
import time
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret")

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "127.0.0.1"),
    "port": int(os.environ.get("DB_PORT", "3306")),
    "database": os.environ.get("DB_NAME", "training_center"),
    "user": os.environ.get("DB_USER", "appuser"),
    "password": os.environ.get("DB_PASSWORD", "apppass"),
}

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

for i in range(10):
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        break
    except Exception as e:
        print(f"Waiting for DB... ({i+1}/10) {e}")
        time.sleep(2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    course = request.form.get("course", "").strip()

    if not all([full_name, email, phone, course]):
        flash("All fields are required.", "error")
        return redirect(url_for("index"))

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO students (full_name, email, phone, course) VALUES (%s, %s, %s, %s)",
                    (full_name, email, phone, course)
                )
                conn.commit()
        flash("Registration saved successfully!", "success")
        return redirect(url_for("index"))
    except Error as e:
        flash(f"Database error: {e}", "error")
        return redirect(url_for("index"))


@app.route("/report")
def report():
    search = request.args.get("q", "").strip()
    rows = []
    try:
        with get_conn() as conn:
            with conn.cursor(dictionary=True) as cur:
                if search:
                    like = f"%{search}%"
                    cur.execute(
                        """
                        SELECT id, full_name, email, phone, course, registered_at
                        FROM students
                        WHERE full_name LIKE %s OR email LIKE %s OR phone LIKE %s OR course LIKE %s
                        ORDER BY registered_at DESC
                        """,
                        (like, like, like, like)
                    )
                else:
                    cur.execute(
                        "SELECT id, full_name, email, phone, course, registered_at FROM students ORDER BY registered_at DESC"
                    )
                rows = cur.fetchall()
    except Error as e:
        flash(f"Database error: {e}", "error")

    return render_template("report.html", rows=rows, search=search)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
