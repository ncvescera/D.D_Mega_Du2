from flask import request, send_from_directory, jsonify
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
from natsort import natsorted, ns
from app import *
from models import *
from utils import *
import os

## ----------------------- PLAY EPISODIO ----------------------- ##
@app.route('/play/<int:id>')
def play_episodio(id):
    episodio = Episodio.query.filter_by(id=id).first()

    return send_from_directory(app.config['UPLOAD_FOLDER'], episodio.path)


## ----------------------- SERIE ----------------------- ##
@app.route('/serie', methods=['GET'])
@cross_origin()
def all_serie():
    """
    Ritorna i dati di tutte le serie nel DB
    """

    series = Serie.query.all()

    series_json = [x.as_dict() for x in series]     # trasforma ogni serie in dizionario per essere convertito in json

    return jsonify({"response": series_json}), 200


@app.route('/serie/<int:id>', methods=['GET'])
@cross_origin()
def get_serie(id):
    """
    Ritorna i dati di una specifica serie 
    (identificatata univocamente dal campo ID)
    """

    serie = Serie.query.filter_by(id=id).first()

    serie_json = serie.as_dict()

    return jsonify({'response': serie_json}), 200


@app.route('/serie', methods=['POST'])
@cross_origin()
def add_serie():
    """
    Aggiunge una nuova serie con i dati passati
    """

    # prende i dati del form  
    nome            = request.form['nome']
    descrizione     = request.form['descrizione']
    tag             = request.form['tag']
    
    # controlla che i dati necessari siano inseriti
    if not check_required_data((nome,)):
        return jsonify({"error": "Inserisci tutti i dati necessari !"}), 400

    # controlla se esiste gia' una serie con gli stessi dati
    existing_serie = Serie.query.filter_by(nome=nome).first()
    if existing_serie:
        return jsonify({"error": "La serie esiste già !"}), 400

    else:
        # aggiunge la nuova serie
        new_serie = Serie(nome=nome, descrizione=descrizione, tag=tag)

        try:
            db.session.add(new_serie)
            db.session.commit()

            return jsonify({"message": f"Serie {nome} aggiunta con successo !"}), 200

        except:
            return jsonify({"error": "Impossibile aggiungere la serie :/"}), 401


@app.route('/serie', methods=['PUT'])
@cross_origin()
def aggiorna_serie():
    """
    Aggiorna i dati di una serie esistente
    (identificata univocamente dal campo ID)
    """

    nome = request.form['nome']
    descrizione = request.form['descrizione']
    tag = request.form['tag']
    id = request.form['id']

    # controlla che i dati necessari siano inseriti
    if not check_required_data((nome, id,)):
        return jsonify({"error": "Inserisci tutti i dati necessari !"}), 400

    # controlla se la serie esiste
    to_update = Serie.query.filter_by(id=id).first()
    if to_update:
        to_update.nome = nome
        to_update.descrizione = descrizione
        to_update.tag = tag

        try:
            db.session.commit()

            return jsonify({'message': 'Serie aggiornata con successo !'}), 200

        except:
            return jsonify({'error': 'Impossibile aggiornare i dati !'}), 400
        
    return jsonify({'error': 'Serie inesistente !'}),400


@app.route('/serie/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_serie(id):
    """
    Elimina una serie
    (identificata univocamente dal campo ID)
    """

    # controlla se la serie esiste nel database
    to_remove = Serie.query.filter_by(id=id).first()
    if to_remove:
        try:
            db.session.delete(to_remove)
            db.session.commit()

            # elimina tutte le stagioni appartenenti alla serie
            stagioni_to_remove = Stagione.query.filter_by(serie_id=id).all()
            for stagione in stagioni_to_remove:
                delete_stagione(stagione.id)

            return jsonify({'message': 'Serie eliminata !'}), 200
        except:
            return jsonify({'error': 'Impossibile eliminare la serie !'}), 400

    return jsonify({'error': 'La serie non esiste !'}), 400


## ----------------------- STAGIONI ----------------------- ##
@app.route('/stagione/<int:id>', methods=['GET'])
@cross_origin()
def get_stagione(id):
    """
    Ritorna i dati di una singola stagione
    """

    stagione = Stagione.query.filter_by(id=id).first()

    stagione_json = stagione.as_dict()

    return jsonify({'response': stagione_json}), 200


@app.route('/stagioni_of/<int:serie_id>', methods=['GET'])
@cross_origin()
def stagioni_by_serie(serie_id):
    """
    Ritorna tutte le stagioni di una data serie
    """

    stagioni = Stagione.query.filter_by(serie_id=serie_id)

    stagioni = natsorted(stagioni, key=lambda x: x.nome)  # ordina le stagioni in base al nome
    
    stagioni_json = [x.as_dict() for x in stagioni]

    return jsonify({"response": stagioni_json}), 200


@app.route('/stagione', methods=['POST'])
@cross_origin()
def add_stagione():
    """
    Aggiunge una Stagione ad una serie
    """

    # prende i dati del form  
    nome            = request.form['nome']
    descrizione     = request.form['descrizione']
    tag             = request.form['tag']
    serie_id        = request.form['serie_id']

    # controlla che i dati necessari siano inseriti
    if not check_required_data((nome, serie_id,)):
        return jsonify({"error": "Inserisci tutti i dati necessari !"}), 400

    # controlla se esiste una stagione con gli stessi dati
    existing_stagione = Stagione.query.filter_by(nome=nome, serie_id=serie_id).first()
    if existing_stagione:
        return jsonify({"error": "La stagione esiste già !"}), 400

    else:
        # aggiunge la nuova stagione al DB
        new_stagione = Stagione(nome=nome, descrizione=descrizione, tag=tag, serie_id=serie_id)

        try:
            db.session.add(new_stagione)
            db.session.commit()

            return jsonify({"message": f"Stagione {nome} aggiunta con successo !"}), 200

        except:
            return jsonify({"error": "Impossibile aggiungere la stagione :/"}), 401


@app.route('/stagione', methods=['PUT'])
@cross_origin()
def update_stagione():
    """
    Aggiorna i dati di una stagione
    """

    nome = request.form['nome']
    descrizione = request.form['descrizione']
    tag = request.form['tag']
    id = request.form['id']

    # controlla che i dati necessari siano inseriti
    if not check_required_data((nome, id,)):
        return jsonify({"error": "Inserisci tutti i dati necessari !"}), 400

    # controlla che la stagione esista nel DB
    to_update = Stagione.query.filter_by(id=id).first()
    if to_update:
        to_update.nome = nome
        to_update.descrizione = descrizione
        to_update.tag = tag

        try:
            db.session.commit()

            return jsonify({'message': 'Stagione aggiornata con successo !'}), 200

        except:
            return jsonify({'error': 'Impossibile aggiornare i dati !'}), 400
        
    return jsonify({'error': 'Stagione inesistente !'}),400


@app.route('/stagione/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_stagione(id):
    """
    Elimina una data stagione
    """

    # controlla se la stagione esiste
    to_remove = Stagione.query.filter_by(id=id).first()
    if to_remove:
        try:
            db.session.delete(to_remove)
            db.session.commit()

            # elimina tutti gli episodi appartenenti alla stagione
            episodi_to_remove = Episodio.query.filter_by(stagione_id=id).all()
            for episodio in episodi_to_remove:
                delete_episodio(episodio.id)

            return jsonify({'message': 'Stagione eliminata !'}), 200
        except:
            return jsonify({'error': 'Impossibile eliminare la stagione !'}), 400

    return jsonify({'error': 'La stagione non esiste !'}), 400


## ----------------------- EPISODI ----------------------- ##
@app.route('/episodio/<int:id>', methods=['GET'])
@cross_origin()
def get_episodio(id):
    """
    Ritorna i dati del singolo episodio
    """

    episodio = Episodio.query.filter_by(id=id).first()

    episodio_json = episodio.as_dict()

    return jsonify({'response': episodio_json}), 200


@app.route('/episodi_of/<int:id>', methods=['GET'])
@cross_origin()
def episodi_by_stagione(id):
    """
    Ritorna i dati di tutti gli episodi di una data stagione
    """

    episodi = Episodio.query.filter_by(stagione_id=id).all()

    episodi = natsorted(episodi, key=lambda x: x.nome)  # ordina le stagioni in base al nome

    episodi_json = [x.as_dict() for x in episodi]

    return jsonify({'response': episodi_json}), 200


@app.route('/episodio', methods=['POST'])
@cross_origin()
def add_episodio():
    """
    Aggiunge un nuovo episodio
    """

    nome = request.form['nome']
    descrizione = request.form['descrizione']
    tag = request.form['tag']
    stagione_id = request.form['stagione_id']
    file = request.files['file']

    # controlla che i dati necessari siano inseriti
    if not check_required_data((nome, stagione_id, file.filename,)):
        return jsonify({"error": "Inserisci tutti i dati necessari !"}), 400

    # controlla che non esista un episodio con gli stessi dati
    existing_episodio = Episodio.query.filter_by(nome=nome, stagione_id=stagione_id).first()
    if existing_episodio:
        return jsonify({"error": "L'episodio esiste già !"}), 400

    else:
        # creazione nuovo episodio
        new_episodio = Episodio(nome=nome, descrizione=descrizione, tag=tag, stagione_id=stagione_id, path='tmp')
        try:
            db.session.add(new_episodio)    # aggiunge al db il nuovo episodio
            db.session.flush()              # aggiorna la sessione del db senza rendere permanenti i cambiamenti
            
            # crea il nuovo nome del file e il path dove andra' salvato
            serie_id = Stagione.query.filter_by(id=stagione_id).first().serie_id
            new_filename, file_path = process_file(file.filename, app.config['UPLOAD_FOLDER'], new_episodio.id, stagione_id=stagione_id, serie_id=serie_id)

            new_episodio.path = new_filename    # aggiorna il path con il nuovo file_name
            db.session.flush()                  # aggiorna la sessione del db

            file.save(file_path)            # salva il file su disco
            db.session.commit()             # salva le modifiche nel db

            return jsonify({"message": f"Episodio {nome} aggiunto con successo !"}), 200

        except:
            return jsonify({"error": "Impossibile aggiungere l'episodio :/"}), 401


@app.route('/episodio', methods=['PUT'])
@cross_origin()
def update_episodio():
    """
    Aggiorna i dati di un episodio esistente
    """

    nome = request.form['nome']
    descrizione = request.form['descrizione']
    tag = request.form['tag']
    file = request.files['file']
    id = request.form['id']
    file_path = ''

    # controlla che i dati necessari siano inseriti
    if not check_required_data((nome, id,)):
        return jsonify({"error": "Inserisci tutti i dati necessari !"}), 400

    # controlla se l'episodio esiste
    to_update = Episodio.query.filter_by(id=id).first()
    if to_update:
        to_update.nome = nome
        to_update.descrizione = descrizione
        to_update.tag = tag

        # ottiene il file path che deve essere aggiornato con il nuovo file
        if file.filename != '':
            stagione_id = to_update.stagione_id
            serie_id = Stagione.query.filter_by(id=stagione_id).first().serie_id

            _, file_path = process_file(file.filename, app.config['UPLOAD_FOLDER'], id, stagione_id=stagione_id, serie_id=serie_id)

        # modifica i dati dell'episodio
        try:
            # se e' stato inserito salva il file
            if file_path != '':
                file.save(file_path)

            db.session.commit()

            return jsonify({'message': 'Episodio aggiornato con successo !'}), 200

        except:
            return jsonify({'error': 'Impossibile aggiornare i dati !'}), 400
        
    return jsonify({'error': 'Episodio inesistente !'}),400


@app.route('/episodio/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_episodio(id):
    """
    Elimina un dato episodio
    """

    # controlla che l'episodio esista
    to_remove = Episodio.query.filter_by(id=id).first()
    if to_remove:
        # ottiene il path del file da eliminare
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], to_remove.path)

        # elimina dal db l'episodio e rimuove il file dal disco
        try:
            db.session.delete(to_remove)
            os.remove(file_path)
            db.session.commit()

            return jsonify({'message': 'Episodio eliminato !'}), 200

        except:
            return jsonify({'error': 'Impossibile eliminare l\'episodio !'}), 400

    return jsonify({'error': 'L\'episodio non esiste !'}), 400


@app.route('/cerca', methods=['POST'])
def cerca():
    def to_dict(array: list) -> list:
        return [x.as_dict() for x in array]

    ricerca = request.form['ricerca']
    
    # ricerca
    serie = Serie.query.filter((Serie.nome.like(f"%{ricerca}%")) | ((Serie.tag.like(f"%{ricerca}%")))).all()
    stagioni = Stagione.query.filter((Stagione.nome.like(f"%{ricerca}%")) | ((Stagione.tag.like(f"%{ricerca}%")))).all()
    episodi = Episodio.query.filter((Episodio.nome.like(f"%{ricerca}%")) | ((Episodio.tag.like(f"%{ricerca}%")))).all()

    # print(serie, stagioni, episodi)

    # conversione per JSON
    serie_json = to_dict(serie)
    stagioni_json = to_dict(stagioni)
    episodi_json = to_dict(episodi)

    # dizionario finale
    result = {
        'serie': serie_json,
        'stagioni': stagioni_json,
        'episodi': episodi_json
    }

    # print(result)

    return jsonify({'response': result}), 200
