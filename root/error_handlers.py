from flask import render_template

def error_404(error):
    return render_template("404.html"), 404