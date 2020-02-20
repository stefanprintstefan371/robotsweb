from flask import render_template, flash, session, redirect, url_for, request
from root.uzivatele.models import Uzivatele
from root import administrace
import root

@administrace.administrace_page.route("/uzivatele/", methods = ["GET", "POST"])
def admin_uzivatele():
    #Pokud uživatel není přihlášen nebo není admin
    if "user" not in session or Uzivatele.query.filter_by(id = session["user"]["_id"]).first().is_admin != 1:
        flash("Chyba", "critical")
        return redirect(url_for("prispevky_page.uvod"))
    #Pokud byl udeslán formulář
    if request.method == "POST":
        u = Uzivatele.query.filter_by(id = request.form["smazat"]).first()
        #Pokud se administrátor pokusí smazat administrátora
        if u.is_admin == 1:
            flash("Nemůžeš smazat administrátora", "critical")
        else:
            root.db.session.delete(u)
            root.db.session.commit()
    #Získáme všechny užovatele
    u = Uzivatele.query.all()
    return render_template("admin_uzivatele.html", users = u)