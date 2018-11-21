import os.path
import random
from .app import db

class Author(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    name        = db.Column(db.String(100))

class Book(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    img         = db.Column(db.String(100))
    price       = db.Column(db.Float)
    title       = db.Column(db.String(100))
    url         = db.Column(db.String(200))
    author_id   = db.Column(db.Integer, db.ForeignKey("author.id"))
    author      = db.relationship("Author", backref = db.backref("books", lazy = "dynamic"))

def get_sample(n = 10):
    return Book.query.limit(n).all()

def get_books(n = None):
    return get_sample(n) if n else BOOKS

def get_book(id):
    return Book.get(id)
