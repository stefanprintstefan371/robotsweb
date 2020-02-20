from flask import Blueprint
prispevky_page = Blueprint("prispevky_page", __name__, template_folder = "templates")

import root.prispevky.uvod
import root.prispevky.pridat
import root.prispevky.detail

