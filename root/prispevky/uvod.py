from flask import render_template
from root import prispevky
from .models import Prispevky, Tagy


prispevky_page = prispevky.prispevky_page

@prispevky_page.route("/uvod/")
def uvod():
        return render_template("uvod.html")
    
    

@prispevky_page.route("/polozky/")
def polozky():
	return render_template("polozky.html")

@prispevky_page.route("/spravy/")
def spravy():
    #Získáme všechny příspěvky
    _prispevky = Prispevky.query.all()
    return render_template("spravy.html", prispevky = _prispevky)
