from flask import Flask, render_template, request, redirect, send_file, flash
import psycopg2
import csv
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"


conn = psycopg2.connect(
    dbname=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT")
)
cur = conn.cursor()

@app.route("/", methods=["GET", "POST"])
def index():
    lang = request.args.get("lang", "en")
    action = request.args.get("action", "")
    results = []

    if request.method == "POST":
        query = request.form.get("query", "")
        cur.execute("""
            SELECT * FROM clients 
            WHERE name ILIKE %s OR email ILIKE %s OR phone ILIKE %s
        """, (f"%{query}%", f"%{query}%", f"%{query}%"))
        results = cur.fetchall()
    elif action == "all":
        cur.execute("SELECT * FROM clients")
        results = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM clients")
    total_clients = cur.fetchone()[0]

    return render_template("index.html", results=results, lang=lang, total_clients=total_clients, action=action)

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

@app.route("/stats")
def stats():
    cur.execute("SELECT COUNT(*) FROM clients")
    total = cur.fetchone()[0]
    return render_template("stats.html", total=total)

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
    
if __name__ == "__main__":
    app.run(debug=True)