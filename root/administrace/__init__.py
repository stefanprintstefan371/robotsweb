from flask import Blueprint

administrace_page = Blueprint("administrace_page", __name__, template_folder = "templates")

import root.administrace.admin_uzivatele
import root.administrace.admin_prispevky
import root.administrace.admin_tagy