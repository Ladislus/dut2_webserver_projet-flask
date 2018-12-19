from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_bootstrap import Bootstrap

from flask_login import LoginManager

app = Flask(__name__)
Bootstrap(app)
app.debug = True
app.config['BOOTSTRAP_SERVE_LOCAL'] = True


import os.path
def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),p
        )
    )

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///'+mkpath('../tuto.db')
)

db = SQLAlchemy(app)

app.config["SECRET_KEY"] = "fec03c30-124c-43b2-85db-4dfb72c4b56e"

login_manager = LoginManager(app)
login_manager.login_view = "login"
