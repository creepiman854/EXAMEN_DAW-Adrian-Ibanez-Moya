from flask import Flask, render_template
import mysql.connector
from dotenv import load_dotenv
from os import getenv

load_dotenv()

servidor = Flask(__name__)

def db_conn():
    conexion = mysql.connector.connect(
        host = getenv("SQL_HOST"),
        user = getenv("SQL_USER"),
        password = getenv("SQL_PASSWORD"),
        database = getenv("SQL_DB")
    )
    
    return conexion

@servidor.get("/")
def index():
    users = []
    error = None

    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, username, email, full_name FROM users ORDER BY id ASC;")
        users = cur.fetchall()  # [(id, username, email, full_name), ...]
        cur.close()
        conn.close()
    except Exception as e:
        error = str(e)

    return render_template("index.html", users=users, error=error)


@servidor.get("/about")
def about():
    return render_template("about.html")


@servidor.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


@servidor.get("/health")
def health():
    ok = False
    error = None

    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()
        ok = True
    except Exception as e:
        error = str(e)

    return render_template("health.html", ok=ok, error=error)


if __name__ == "__main__":
    servidor.run(host="0.0.0.0", debug=True)
