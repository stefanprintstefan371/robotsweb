import os

from flask_sqlalchemy import SQLAlchemy
from flask import (Flask, flash, Markup, redirect, render_template, request,
                   Response, session, url_for)
#KONFIGURACE
app = Flask(__name__)
app.config["SECRET_KEY"] = "super tajny klic"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../databaze.sqlite3"
UPLOAD_FOLDER = app.static_folder + "/uploads/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
#DATABAZE
db = SQLAlchemy(app)

from . import models
#REGISTRACE BLUEPRINTU
from root.galerie.galerie import galerie_page
from root.error_handlers import error_404
from root import uzivatele
from root import prispevky
from root import administrace
app.register_blueprint(galerie_page)
app.register_error_handler(404, error_404)
app.register_blueprint(uzivatele.uzivatele_page)
app.register_blueprint(prispevky.prispevky_page)
app.register_blueprint(administrace.administrace_page, url_prefix = "/admin")


#HOMEPAGE
@app.route("/")
def homepage():
    return redirect(url_for("prispevky_page.uvod"))
