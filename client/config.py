from app import app

# configurazioni per il database
app.config['SECRET_KEY'] = 'segreto'
app.config['DEBUG'] = True
app.config['SERVER_IP'] = 'http://localhost:4200'