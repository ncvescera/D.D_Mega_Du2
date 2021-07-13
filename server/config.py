from app import app

# configurazioni per il database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'segreto'
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = '/home/candy/Videos'
app.config['CORS_HEADERS'] = 'Content-Type'
