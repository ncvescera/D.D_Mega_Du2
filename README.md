# D.D_Mega_Du2
Distributed Database Mega Digital Universe

D.D_Mega_Du2 è un Database Distribuito per raccogliere, collezionare e catalogare Serie Tv e Sketch Comici.

## Installazione

E' conveniente utilizzare un ambiente virtuale (come venv) per eseguire questo progetto.

Avviare l'ambiente virtuale ed installare i requisiti:

```bash
source ./venv/bin/activate       # se si utilizza venv
pip install -r requirements.txt
```

## Esecuzione

Prima di avviare client e server ricorda che possono stare su macchine diverse 🚀😲!! Che tu decida di metterli sulla stessa macchina o no, controlla sempre il file di configurazione di ciascuno, nello specifico controlla `client/config.py` e assicurati di ver settato il valore `app.config['SERVER_IP]` con il corretto IP della macchina dove è in esecuzione il server (devi specificare anche la porta).

Un esempio:

```python
# client/config.py

...

app.config['SERVER_IP'] = 'http://mydeedeemegadoodoo.it:4200'

...
```

Rircorda che il server è sempre in esecuzione sulla porta `4200` di default.<br>
Ricorda che il client è sempre in esecuzione suppa porta `8080` di default.

### Client

Per avviare il cliente esegui questi comandi

```bash
source ./venv/bin/activate # attiva sempre l'ambiente virtuale !!
cd client
python app.py
```

### Server

Per avviare il server esegui questi comandi

```bash
source ./venv/bin/activate # attiva sempre l'ambiente virtuale !!
cd server
python app.py
```

## Utilizzo

Una volta avviati client e server, apri il browser e, nella barra degli url, inserisci l'IP del Client con il numero di porta.

Un esempio:

```bash
firefox http://myclienteaddress:8080
```
