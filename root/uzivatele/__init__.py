from flask import Blueprint
uzivatele_page = Blueprint("uzivatele_page", __name__, template_folder = "templates")

import root.uzivatele.login
import root.uzivatele.registrace