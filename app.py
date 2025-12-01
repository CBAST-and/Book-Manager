import os
from flask import Flask, render_template, send_from_directory, redirect, request, session, url_for
from books.books_controller import books_bp
from db_session import Base, engine
from models.book import Book

# -------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------

app = Flask(__name__)

# Clave secreta para manejar sesiones
app.secret_key = "clave_super_secreta"

# Carpeta donde se guardarán archivos subidos
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# -------------------------------
# USUARIO DE PRUEBA
# -------------------------------
USUARIO = "admin"
PASSWORD = "1234"

# -------------------------------
# RUTA PARA SERVIR ARCHIVOS
# -------------------------------
@app.route("/uploads/<path:filename>")
def uploaded_files(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# -------------------------------
# RUTA DE LOGIN
# -------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == USUARIO and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            error = "Usuario o contraseña incorrecta"
    return render_template("login.html", error=error)

# -------------------------------
# DASHBOARD / HOME PROTEGIDO
# -------------------------------
@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return redirect("/books")

@app.route("/")
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return redirect("/books")

# -------------------------------
# BLUEPRINTS
# -------------------------------
app.register_blueprint(books_bp)

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
