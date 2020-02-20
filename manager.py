#Importujeme
import root
from root import models
from flask_migrate import Migrate, Manager, MigrateCommand
app = root.app
#Nastavíme novou relativní cestu k databázi, jelikož script nespouštíme ze složky root
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///databaze.sqlite3"
#Provedeme inicializaci
migrate = Migrate(app, root.db)
manager = Manager(app)
#Přidáme přikaz pro manager
manager.add_command("db", MigrateCommand)
#Přikaz spustíme, pokud byl script spuštěn
if __name__ == "__main__":
    manager.run()