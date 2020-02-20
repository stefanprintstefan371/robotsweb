from .models import Prispevky
from flask import render_template, redirect, url_for, abort, session, flash
from root import prispevky
from flask_wtf import FlaskForm
from wtforms import SubmitField
import root

prispevky_page = prispevky.prispevky_page

class PrispevekForm(FlaskForm):
    delete = SubmitField("Smazat")

@prispevky_page.route("/detail/<int:id_c>", methods = ["GET", "POST"])
def detail(id_c):
    p = Prispevky.query.filter_by(id = id_c).first()
    if p is None:
        return abort(404)
    form = PrispevekForm()
    if form.is_submitted() and "user" in session:
        root.db.session.delete(p)
        root.db.session.commit()
        return redirect(url_for("prispevky_page.uvod"))
    elif "user" not in session and form.is_submitted():
        flash("Přihlaš se!", "critical")
        return redirect(url_for("uzivatele_page.login"))
    
    return render_template("detail.html", prispevek = p, form = form)
