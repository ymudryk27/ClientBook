from flask import Flask, render_template, request, redirect, send_file, flash
from dotenv import load_dotenv
import os
import psycopg2
import csv
from urllib.parse import urlparse

app = Flask(__name__)  # ← ОЦЕ ДОДАЙ
app.secret_key = "secret-key"

load_dotenv()



DATABASE_URL = os.environ.get("DATABASE_URL")
result = urlparse(DATABASE_URL)

conn = psycopg2.connect(
    dbname=result.path[1:],
    user=result.username,
    password=result.password,
    host=result.hostname,
    port=result.port
)

cur = conn.cursor()

@app.route("/stats")
def stats():
    cur.execute("SELECT COUNT(*) FROM clients")
    total = cur.fetchone()[0]
    return render_template("stats.html", total=total)

@app.route("/export")
def export_csv():
    cur.execute("SELECT name, email, phone FROM clients")
    rows = cur.fetchall()
    filepath = "clients_export.csv"
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Email", "Phone"])
        writer.writerows(rows)
    return send_file(filepath, as_attachment=True)

@app.route("/add", methods=["POST"])
def add_client():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    try:
        cur.execute("INSERT INTO clients (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        conn.commit()
        flash("Client added successfully!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
    return redirect("/")

@app.route("/", methods=["GET", "POST"])
def index():
    lang = request.args.get("lang", "en")
    action = request.args.get("action", "")
    results = []

    if request.method == "POST":
        query = request.form.get("query", "")
        cur.execute("SELECT * FROM clients WHERE name ILIKE %s OR email ILIKE %s OR phone ILIKE %s",
                    (f"%{query}%", f"%{query}%", f"%{query}%"))
        results = cur.fetchall()
    elif action == "all":
        cur.execute("SELECT * FROM clients")
        results = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM clients")
    total_clients = cur.fetchone()[0]

    return render_template("index.html", results=results, lang=lang, total_clients=total_clients)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)