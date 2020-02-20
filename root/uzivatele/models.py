import root
import datetime
from flask_bcrypt import generate_password_hash

db = root.db


class Uzivatele(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable = False)
    datum_registrace = db.Column(db.Text, nullable = False, default = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    datum_prihlaseni = db.Column(db.Text, nullable = False, default = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    prispevky = db.relationship("Prispevky", backref = "autor", lazy = True)
    is_admin = db.Column(db.Integer, server_default = "0")
    def __repr__(self):
        return "<Uzivatele {username} {id}>".format(username = self.username, id = self.id)
    def __str__(self):
        return "{id} - {username} - {password} - {datum_registrace}".format(id = self.id,
         username = self.username, password = self.password, datum_registrace = self.datum_registrace)
    @staticmethod
    def create_uzivatel(username, password):
        u = Uzivatele(username = username, password = generate_password_hash(password))
        return u


