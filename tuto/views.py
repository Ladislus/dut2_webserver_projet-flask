from .app import app, db
from flask import render_template, url_for, redirect, request
from flask_wtf import FlaskForm
from flask_login import login_user, current_user, login_required, logout_user
from wtforms import StringField, HiddenField, PasswordField
from wtforms.validators import DataRequired
from .models import Author, User, Cart, get_books, get_book, get_sample, get_authors, get_author, get_authorbooks, get_random_book, get_cart_books
from hashlib import sha256
from .commands import adddb

#LOGIN
class LoginForm(FlaskForm):
    username  = StringField('Username')
    password  = PasswordField('Password')
    next      = HiddenField()

    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None

@app.route("/login/", methods=("GET", "POST",))
def login():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect(next)
    return render_template(
        "login.html",
        form = f
    )

#LOGOUT
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

class AuthorForm(FlaskForm):
    id  = HiddenField('id')
    name= StringField('Nom', validators = [DataRequired()])

#CART
@app.route("/cart")
@login_required
def cart():
    books = get_cart_books(current_user.username)
    print(books)
    return render_template("cart.html",
                            books = books)

#EDIT AUTHOR
@app.route("/edit/author/<int:id>")
@login_required
def edit_author(id):
    a = get_author(id)
    f = AuthorForm(id=a.id, name=a.name)
    return render_template(
        "edit-author.html",
        title="Book shop",
        author=a, form=f
    )

#SAVE AUTHOR
@app.route("/save/author/", methods=('POST',))
def save_author():
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
        id = int(f.id.data)
        a = get_author(id)
        a.name = f.name.data
        db.session.commit()
        return redirect(url_for('home', id=a.id))
    a = get_author(int(f.id.data))
    return render_template(
        "edit-author.html",
        title = "Book shop",
        author = a, form = f)

#HOME
@app.route("/")
def home():
    return render_template(
            "home.html",
            title="Book shop",
            BOOKS=get_random_book(10))

#BOOKS
@app.route("/books/")
def books():
    return render_template(
            "books.html",
            title="Book shop",
            BOOKS=get_books())

#SPECIAL SEARCH BOOK
@app.route("/book/<int:index>")
def book(index):
    return render_template(
            "book.html",
            title="Book shop",
            BOOKS=get_book(index))

@app.route("/author/<int:index>")
def author(index):
    return render_template(
            "author.html",
            title="Book shop",
            author=get_author(index),
            books=get_authorbooks(index))

@app.route("/authors/")
def authors():
    return render_template(
            "authors.html",
            title="Book shop",
            AUTHORS=get_authors())

@app.route("/add/author/")
def add_author():
	f = AuthorForm(id=get_authors()[-1].id+1, name="")
	return render_template("add-author.html", form=f)

@app.route("/added/author", methods=("POST",))
def added_author():
	f = AuthorForm()
	if f.validate_on_submit():
		adddb(Author(name=f.name.data, id=f.id.data))
		db.session.commit()
		return redirect(url_for('author', index=f.id.data))
	a = get_author(int(f.id.data))

	return render_template("add-author.html", author=a, form=f)

@app.route("/added/cart", methods=("POST",))
def added_cart(id):
    adddb(Cart(username=current_user.username, id_book=id))
    db.session.commit()
    return redirect(url_for('cart'))

class BookForm(FlaskForm):
    id  = HiddenField('id')
    title= StringField('Title', validators = [DataRequired()])
    author= StringField('Author')
    price= StringField('Price')

#EDIT BOOK
@app.route("/edit/book/<int:id>")
@login_required
def edit_book(id):
    b = get_book(id)
    f = BookForm(id=b.id, title=b.title)
    return render_template(
        "edit-book.html",
        title="Book shop",
        book=b, form=f
    )

#SAVE BOOK
@app.route("/save/book/", methods=('POST',))
def save_book():
    b = None
    f = BookForm()
    if f.validate_on_submit():
        id = int(f.id.data)
        b = get_book(id)
        b.title = f.title.data
        b.price = f.price.data
        db.session.commit()
        return redirect(url_for('home', id=b.id))
    b = get_book(int(f.id.data))
    return render_template(
        "edit-book.html",
        title = "Book shop",
        book = b, form = f)


@app.route("/edit/")
def edit():
    return render_template(
    "edit.html",
    title = "Book shop"
    )
