import os
from flask import Flask, render_template, send_from_directory, redirect
from books.books_controller import books_bp
from db_session import Base, engine
from models.book import Book

# -------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------

app = Flask(__name__)

# Carpeta donde se guardarán archivos subidos
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# -------------------------------
# RUTA PARA SERVIR ARCHIVOS
# -------------------------------
@app.route("/uploads/<path:filename>")
def uploaded_files(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# -------------------------------
# RUTA PRINCIPAL
# -------------------------------
@app.route("/")
def home():
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
