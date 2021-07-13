from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)   # inizializzo l'app
db = SQLAlchemy(app)    # inizializzo il gestore del DB
cors = CORS(app)

if __name__ == "__main__":
    import config
    from api import *

    db.create_all()                      # crea tutte le tabelle

    app.run(host="0.0.0.0", port="4200") # avvia il server