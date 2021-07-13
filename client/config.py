from app import app

# configurazioni per il database
app.config['SECRET_KEY'] = 'segreto'
app.config['DEBUG'] = True
app.config['SERVER_IP'] = 'http://thecandy:4200'

# scrive l'ip del server in un file js
with open('./static/js/server.js', 'w') as f:
    f.write(f'var server_ip = \'{app.config["SERVER_IP"]}\';\n')