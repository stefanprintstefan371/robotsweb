from flask import render_template, redirect, url_for, Blueprint, session, flash
import root
from .models import Uzivatele
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired

from root import uzivatele

registrace_page = uzivatele.uzivatele_page

class RegistraceForm(FlaskForm):
    username = StringField("Uživatelské jméno", validators = [InputRequired()])
    password = PasswordField("Heslo", validators = [InputRequired()])
    submit = SubmitField("Odeslat")

@registrace_page.route("/registrace/", methods = ["GET", "POST"])
def registrace():
    form = RegistraceForm()
    if form.validate_on_submit() and "user" not in session:
        #Vytvoříme uživatele
        u = Uzivatele.create_uzivatel(username = form.username.data, password = form.password.data)
        #Přidáme do session databáze
        root.db.session.add(u)
        #Provedeme změny
        try:
            root.db.session.commit()
        except:
            flash("Chyba", "critical")
            return render_template("registrace.html", form = form)
        #Do session přidáme slovník
        session["user"] = dict(username = u.username, _id = u.id)
        flash("Uživatel {username} byl registrován".format(username = u.username))
        return redirect(url_for("galerie_page.galerie"))
    return render_template("registrace.html", form = form)