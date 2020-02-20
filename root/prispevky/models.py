import root

db = root.db

pri_tag = db.Table("pri_tag",
    db.Column("prispevek", db.Integer, db.ForeignKey("prispevky.id"), nullable = False),
    db.Column("tag", db.Integer, db.ForeignKey("tagy.id"), nullable = False)
)

class Tagy(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nazev = db.Column(db.Text, unique = True)

class Prispevky(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, nullable = False)
    autor_id = db.Column(db.Integer, db.ForeignKey("uzivatele.id"), nullable = False)
    tagy = db.relationship("Tagy", secondary = pri_tag, backref = "prispevky")
    zablokovano = db.Column(db.Integer, server_default = "0")
