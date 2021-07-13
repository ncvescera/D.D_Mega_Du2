from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)   # inizializzo l'app
db = SQLAlchemy(app)    # inizializzo il gestore del DB


if __name__ == "__main__":
    import config
    from api import *

    db.create_all()                      # crea tutte le tabelle

    app.run(host="0.0.0.0", port="4200") # avvia il server