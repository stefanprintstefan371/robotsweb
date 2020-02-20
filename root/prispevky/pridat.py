from flask import render_template, session, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import InputRequired
from wtforms.widgets import TextArea
from root import prispevky
import root
from .models import Prispevky, Tagy

prispevky_page = prispevky.prispevky_page

class PridatForm(FlaskForm):
    text = StringField("Text příspěvku", validators = [InputRequired()], render_kw = dict(class_ = "form-control"), widget = TextArea())
    tagy = SelectMultipleField("Tagy", choices = [ (str(tag.id), tag.nazev) for tag in Tagy.query.all() ], render_kw = dict(class_ = "form-control"))
    submit = SubmitField("Odeslat", render_kw = dict(class_ = "btn btn-outline-primary btn-block"))
    def __init__(self):
        super(PridatForm, self).__init__()
        self.tagy.choices = [ (str(tag.id), tag.nazev) for tag in Tagy.query.all() ]
        

@prispevky_page.route("/pridat/", methods = ["GET", "POST"])
def pridat():
    form = PridatForm()
    if form.is_submitted():
        if "user" not in session:
            flash("Přihlaš se!", "critical")
            return redirect(url_for("uzivatele_page.login"))
        if form.validate():
            p = Prispevky(text = form.text.data, autor_id = session["user"]["_id"], tagy = [ Tagy.query.filter_by(id = _id).first() for _id in form.tagy.data ])
            root.db.session.add(p)
            root.db.session.commit()
            return redirect(url_for("prispevky_page.uvod"))
    return render_template("pridat.html", form = form)
           

 
