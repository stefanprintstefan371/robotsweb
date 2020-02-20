from flask import render_template, redirect, url_for, session, flash, request, abort
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from root import administrace
from root.prispevky.models import Tagy, Prispevky
from root.uzivatele.models import Uzivatele
import root

class TagyForm(FlaskForm):
    nazev = StringField("Název tagu", validators = [InputRequired()], render_kw = dict(class_ = "form-control"))
    submit = SubmitField("Odeslat")

@administrace.administrace_page.route("/tagy/", methods = ["GET", "POST"])
def admin_tagy():
    #Pokud uživatel není přihlášen nebo není admin
    if "user" not in session or Uzivatele.query.filter_by(id = session["user"]["_id"]).first().is_admin != 1:
        flash("Chyba", "critical")
        return redirect(url_for("prispevky_page.uvod"))
    if request.method == "POST":
        if "upravit" in request.form:
            return redirect(url_for("administrace_page.admin_tagy_zobrazit", id_t = request.form["upravit"]))
        elif "smazat" in request.form:
            t = Tagy.query.filter_by(id = request.form["smazat"]).first()
            root.db.session.delete(t)
            root.db.session.commit()
        elif "zobrazit" in request.form:
            t = Tagy.query.filter_by(id = request.form["zobrazit"]).first()
            p = Prispevky.query.filter(Prispevky.tagy.contains(t)).all()
            return "<br>".join(["{} {}".format(i.id, i.text) for i in p])
    tagy = Tagy.query.all()
    return render_template("admin_tagy.html", tagy = tagy)

@administrace.administrace_page.route("/tagy/<int:id_t>/", methods = ["GET", "POST"])
def admin_tagy_uprava(id_t):
    #Pokud uživatel není přihlášen nebo není admin
    if "user" not in session or Uzivatele.query.filter_by(id = session["user"]["_id"]).first().is_admin != 1:
        flash("Chyba", "critical")
        return redirect(url_for("prispevky_page.uvod"))
    form = TagyForm()
    t = Tagy.query.filter_by(id = id_t).first()
    if t is None:
        return abort(404)
    #Pokud byl formulář odeslán a je validní
    if form.validate_on_submit():
        t.nazev = form.nazev.data
        root.db.session.add(t)
        root.db.session.commit()
        return redirect(url_for("administrace_page.admin_tagy"))
    form.nazev.data = t.nazev
    return render_template("admin_tagy_uprava.html", form = form)