from flask import Flask, render_template, request, redirect, send_file
from flask import jsonify
import psycopg2
import csv

app = Flask(__name__)

conn = psycopg2.connect(
    dbname="clients",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

@app.route("/", methods=["GET", "POST"])
def index():
    lang = request.args.get("lang", "en")
    action = request.args.get("action", "")
    query = request.form.get("query", "")
    results = []

    if request.method == "POST" and query:
        cur.execute("SELECT * FROM clients WHERE name ILIKE %s OR email ILIKE %s OR phone ILIKE %s",
                    (f"%{query}%", f"%{query}%", f"%{query}%"))
        results = cur.fetchall()
    elif action == "all":
        cur.execute("SELECT * FROM clients")
        results = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM clients")
    total_clients = cur.fetchone()[0]

    return render_template("index.html", results=results, lang=lang, total_clients=total_clients, query=query)

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


@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query", "")
    cur.execute("SELECT * FROM clients WHERE name ILIKE %s OR email ILIKE %s OR phone ILIKE %s",
                (f"%{query}%", f"%{query}%", f"%{query}%"))
    results = cur.fetchall()
    return render_template("results.html", results=results)

@app.route("/stats")
def stats():
    cur.execute("SELECT COUNT(*) FROM clients")
    total = cur.fetchone()[0]
    return render_template("stats.html", total=total)

if __name__ == "__main__":
    app.run(debug=True)