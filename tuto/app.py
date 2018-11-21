from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_bootstrap import Bootstrap

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
    'sqlite:///'+mkpath('../myapp.db')
)

db = SQLAlchemy(app)
