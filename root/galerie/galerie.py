from flask import render_template, Blueprint
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_wtf.file import FileRequired
from werkzeug.utils import secure_filename
import os

import root

galerie_page = Blueprint("galerie_page", __name__, template_folder = "templates")
galeria_page = Blueprint("galeria_page", __name__, template_folder = "templates")

class FileFormular(FlaskForm):
    soubor = FileField("Vlož obrázek", validators = [FileRequired()])
    submit = SubmitField("Odeslat", render_kw = dict(class_ = "btn btn-outline-primary btn-block"))

@galerie_page.route("/galerie/", methods = ["GET", "POST"])
def galerie():
    form = FileFormular()
    if form.validate_on_submit():
        soubor = form.soubor.data
        nazev = secure_filename(soubor.filename)
        soubor.save(os.path.join(root.app.config['UPLOAD_FOLDER'], nazev))
        
    obrazky = os.listdir(root.app.static_folder + "/uploads")
    
    return render_template("galerie.html", form = form, obrazky = obrazky)

@galeria_page.route("/galeria/", methods = ["GET"])
def galeria():
	
    return render_template("galeria.html")
