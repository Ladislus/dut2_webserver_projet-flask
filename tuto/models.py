import os.path
import random
from .app import db
from flask_sqlalchemy import SQLAlchemy

class Author(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    name        = db.Column(db.String(100))

    def __repr__(self):
        return "<Author (%d) %s>" % (self.id, self.name)

class Book(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    img         = db.Column(db.String(100))
    price       = db.Column(db.Float)
    title       = db.Column(db.String(100))
    url         = db.Column(db.String(200))
    author_id   = db.Column(db.Integer, db.ForeignKey("author.id"))
    author      = db.relationship("Author", backref = db.backref("books", lazy = "dynamic"))

    def __repr__(self):
        return "<Book (%d) %s>" % (self.id, self.title)



def get_sample(n = 10):
    return Book.query.limit(n).all()

def get_books(n = None):
    return Book.query.all()

def get_book(id):
    return Book.query.get(id)

def get_authors(n = None):
    return Author.query.all()

def get_author(id):
    return Author.query.get(id)

def get_authorbooks(id):
    return Book.query.filter(Book.author == get_author(id)).all()
