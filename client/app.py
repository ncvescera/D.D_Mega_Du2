from flask import Flask


app = Flask(__name__)   # inizializzo l'app


if __name__ == "__main__":
    import config
    from routes import *

    app.run(host="0.0.0.0", port="8080") # avvia il server