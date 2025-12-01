from flask import Blueprint, request, render_template, redirect
from db_session import SessionLocal
from models.book import Book
from sqlalchemy import or_
import os
from werkzeug.utils import secure_filename
from flask import current_app

books_bp = Blueprint("books", __name__)

# ---------------------------
# LISTAR + BUSCAR
# ---------------------------
@books_bp.route("/books", methods=["GET"])
def list_books():
    db = SessionLocal()
    search = request.args.get("search", "").strip()

    if search:
        books = db.query(Book).filter(
            or_(
                Book.Title.ilike(f"%{search}%"),
                Book.Author.ilike(f"%{search}%"),
                Book.Description.ilike(f"%{search}%")
            )
        ).order_by(Book.Id.desc()).all()
    else:
        books = db.query(Book).order_by(Book.Id.desc()).all()

    db.close()
    return render_template("index.html", books=books, search=search)

# ---------------------------
# AGREGAR
# ---------------------------
@books_bp.route("/books/add", methods=["GET"])
def add_book_form():
    return render_template("add_book.html")

@books_bp.route("/books/add", methods=["POST"])
def add_book():
    db = SessionLocal()

    file = request.files.get("pdf_file")
    pdf_url = request.form["pdf_url"]

    # Si el usuario subió un archivo
    if file and file.filename != "":
        filename = secure_filename(file.filename)
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)

        pdf_link = f"/uploads/{filename}"  # <-- URL pública
    else:
        pdf_link = pdf_url  # <-- URL del formulario

    new_book = Book(
        Title=request.form["title"],
        Author=request.form["author"],
        Description=request.form["description"],
        PdfUrl=pdf_link,
        CoverUrl=request.form["cover_url"]
    )

    db.add(new_book)
    db.commit()
    db.close()

    return redirect("/books")

# ---------------------------
# ELIMINAR
# ---------------------------
@books_bp.route("/books/delete/<int:id>", methods=["POST"])
def delete_book(id):
    db = SessionLocal()
    book = db.query(Book).filter(Book.Id == id).first()

    if book:
        db.delete(book)
        db.commit()

    db.close()
    return redirect("/books")

# ---------------------------
# EDITAR - FORM
# ---------------------------
@books_bp.route("/books/edit/<int:id>", methods=["GET"])
def edit_book_form(id):
    db = SessionLocal()
    book = db.query(Book).filter(Book.Id == id).first()
    db.close()

    if not book:
        return "Libro no encontrado", 404

    return render_template("edit_book.html", book=book)

# ---------------------------
# EDITAR - GUARDAR CAMBIOS
# ---------------------------
@books_bp.route("/books/edit/<int:id>", methods=["POST"])
def edit_book(id):
    db = SessionLocal()
    book = db.query(Book).filter(Book.Id == id).first()

    if not book:
        db.close()
        return "Libro no encontrado", 404

    book.Title = request.form["title"]
    book.Author = request.form["author"]
    book.Description = request.form["description"]
    book.PdfUrl = request.form["pdf_url"]
    book.CoverUrl = request.form["cover_url"]

    db.commit()
    db.close()

    return redirect("/books")
