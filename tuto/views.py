from .app import app
from flask import render_template
from .models import get_books, get_book, get_sample

@app.route("/")
def home():
    return render_template(
            "home.html",
            title="Book shop",
            BOOKS=getBooks(10))

@app.route("/books/")
def books():
    return render_template(
            "books.html",
            title="Book shop",
            BOOKS=getBooks())

@app.route("/book/<int:index>")
def book(index):
    return getBook(index)["title"]
