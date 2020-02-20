from flask import render_template, url_for, session, redirect, Blueprint, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired

from .models import Uzivatele
from flask_bcrypt import check_password_hash
from root import uzivatele

login_page = uzivatele.uzivatele_page

class LoginForm(FlaskForm):
    user = StringField("Uživatel", validators = [InputRequired()], render_kw = dict(class_ = "form-control")) #Přihlašovací jméno
    password = PasswordField("Heslo", validators = [InputRequired()], render_kw = dict(class_ = "form-control")) #Heslo
    submit = SubmitField("Odeslat", render_kw = dict(class_ = "btn btn-outline-primary btn-block"))

@login_page.route("/login/", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.user.data
        password = form.password.data
        u = Uzivatele.query.filter_by(username = user).first()
        #Pokud uživatel neexistuje
        if u is None:
            flash("Chyba", "critical")
            return render_template("login.html", form = form)
        #Pokud jsou hesla stejná
        if check_password_hash(u.password, password):
            session["user"] = dict(username = u.username, _id = u.id)
            flash("Byl jsi přihlášen jako {username}".format(username = user), "info")
    return render_template("login.html", form = form)

@login_page.route("/logout/")
def odhlasit():
    if "user" in session:
        flash("Uživatel {username} byl odhlášen".format(username = session["user"]["username"]), "critical")
    session.pop("user", None)
    return redirect(url_for("uzivatele_page.login"))