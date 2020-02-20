from flask import render_template, session, request, redirect, url_for, flash, abort
from root import administrace
from root.prispevky.models import Prispevky, Tagy
from root.uzivatele.models import Uzivatele
import root
from root.prispevky.pridat import PridatForm

@administrace.administrace_page.route("/prispevky/<int:id_c>", methods = ["GET", "POST"])
def admin_prispevky_uprava(id_c):
     #Pokud uživatel není přihlášen nebo není admin
    if "user" not in session or Uzivatele.query.filter_by(id = session["user"]["_id"]).first().is_admin != 1:
        flash("Chyba", "critical")
        return redirect(url_for("prispevky_page.uvod"))
    form = PridatForm()
    p = Prispevky.query.filter_by(id = id_c).first()
    if p is None:
        return abort(404)
    #Pokud byl formulář odeslán a je validní
    if form.validate_on_submit():
        p.text = form.text.data
        p.tagy = [ Tagy.query.filter_by(id = _id).first() for _id in form.tagy.data ]
        root.db.session.add(p)
        root.db.session.commit()
        return redirect(url_for("administrace_page.admin_prispevky"))
    form.text.data = p.text
    form.tagy.data = [str(i.id) for i in p.tagy]
    return render_template("pridat.html", form = form)

@administrace.administrace_page.route("/prispevky/", methods = ["GET", "POST"])
def admin_prispevky():
    #Pokud uživatel není přihlášen nebo není admin
    if "user" not in session or Uzivatele.query.filter_by(id = session["user"]["_id"]).first().is_admin != 1:
        flash("Chyba", "critical")
        return redirect(url_for("prispevky_page.uvod"))
    if request.method == "POST":
        #Pokud administrátor oděslal požadavek x udělej x
        if "upravit" in request.form:
            return redirect(url_for("administrace_page.admin_prispevky_uprava", id_c = request.form["upravit"]))
        elif "zablokovat" in request.form:
            #Zablokujeme příspěvek
            p = Prispevky.query.filter_by(id = request.form["zablokovat"]).first()
            p.zablokovano = 1
            root.db.session.add(p)
            root.db.session.commit()
        elif "smazat" in request.form:
            #Smažeme příspěvek
            p = Prispevky.query.filter_by(id = request.form["smazat"]).first()
            root.db.session.delete(p)
            root.db.session.commit()
    prispevky = Prispevky.query.all()
    return render_template("admin_prispevky.html", prispevky = prispevky)