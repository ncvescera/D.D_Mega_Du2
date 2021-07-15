from flask import request, send_from_directory, jsonify
from flask_cors import cross_origin
from app import *
from models import *
import json
from werkzeug.utils import secure_filename
import os
from natsort import natsorted, ns


@app.route('/play/<int:id>')
def play_episodio(id):
    episodio = Episodio.query.filter_by(id=id).first()

    return send_from_directory(app.config['UPLOAD_FOLDER'], episodio.path)


@app.route('/serie', methods=['GET'])
@cross_origin()
def all_serie():
    series = Serie.query.all()

    series_json = [x.as_dict() for x in series] # trasforma ogni serie in dizionario per essere convertito in json

    return jsonify({"response": series_json}), 200


@app.route('/serie/<int:id>', methods=['GET'])
@cross_origin()
def get_serie(id):
    serie = Serie.query.filter_by(id=id).first()

    serie_json = serie.as_dict()

    return jsonify({'response': serie_json}), 200


@app.route('/serie', methods=['POST'])
@cross_origin()
def add_serie():
    # prende i dati del form  
    nome            = request.form['nome']
    descrizione     = request.form['descrizione']
    tag             = request.form['tag']
    
    existing_serie = Serie.query.filter_by(nome=nome).first()

    if existing_serie:
        return jsonify({"error": "La serie esiste già !"}), 400
    else:
        new_serie = Serie(nome=nome, descrizione=descrizione, tag=tag)

        try:
            db.session.add(new_serie)
            db.session.commit()

            return jsonify({"message": f"Serie {nome} aggiunta con successo !"}), 200

        except:
            return jsonify({"error": "Impossibile aggiungere la serie :/"}), 401


@app.route('/serie/<int:id>', methods=['DELETE'])
@cross_origin()
def rimuovi_serie(id):
    #TODO: eliminare a cascata gli episodi e le stagioni !!!

    to_remove = Serie.query.filter_by(id=id).first()

    if to_remove:
        try:
            db.session.delete(to_remove)
            db.session.commit()

            return jsonify({'message': 'Serie eliminata !'}), 200
        except:
            return jsonify({'error': 'Impossibile eliminare la serie !'}), 400

    return jsonify({'error': 'La serie non esiste !'}), 400


@app.route('/serie', methods=['PUT'])
@cross_origin()
def aggiorna_serie():
    nome = request.form['nome']
    descrizione = request.form['descrizione']
    tag = request.form['tag']
    id = request.form['id']

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


## --- STAGIONI --- ##

@app.route('/stagione', methods=['POST'])
@cross_origin()
def add_stagione():
    # prende i dati del form  
    nome            = request.form['nome']
    descrizione     = request.form['descrizione']
    tag             = request.form['tag']
    serie_id        = request.form['serie_id']

    existing_stagione = Stagione.query.filter_by(nome=nome, serie_id=serie_id).first()

    if existing_stagione:
        return jsonify({"error": "La stagione esiste già !"}), 400
    else:
        new_stagione = Stagione(nome=nome, descrizione=descrizione, tag=tag, serie_id=serie_id)

        try:
            db.session.add(new_stagione)
            db.session.commit()

            return jsonify({"message": f"Stagione {nome} aggiunta con successo !"}), 200

        except:
            return jsonify({"error": "Impossibile aggiungere la stagione :/"}), 401


@app.route('/stagioni_of/<int:serie_id>', methods=['GET'])
@cross_origin()
def stagioni_by_serie(serie_id):
    stagioni = Stagione.query.filter_by(serie_id=serie_id)

    stagioni = natsorted(stagioni, key=lambda x: x.nome)  # ordina le stagioni in base al nome
    
    stagioni_json = [x.as_dict() for x in stagioni]

    return jsonify({"response": stagioni_json}), 200


@app.route('/stagione/<int:id>', methods=['GET'])
@cross_origin()
def get_stagione(id):
    stagione = Stagione.query.filter_by(id=id).first()

    stagione_json = stagione.as_dict()

    return jsonify({'response': stagione_json}), 200


@app.route('/stagione/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_stagione(id):
    #TODO: eliminare a cascata tutti gli episodi appartenenti alla stagione

    to_remove = Stagione.query.filter_by(id=id).first()

    if to_remove:
        try:
            db.session.delete(to_remove)
            db.session.commit()

            return jsonify({'message': 'Stagione eliminata !'}), 200
        except:
            return jsonify({'error': 'Impossibile eliminare la stagione !'}), 400

    return jsonify({'error': 'La stagione non esiste !'}), 400


@app.route('/stagione', methods=['PUT'])
@cross_origin()
def update_stagione():
    nome = request.form['nome']
    descrizione = request.form['descrizione']
    tag = request.form['tag']
    id = request.form['id']

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


## --- EPISODI --- ##

@app.route('/episodio', methods=['POST'])
@cross_origin()
def add_episodio():
    nome = request.form['nome']
    descrizione = request.form['descrizione']
    tag = request.form['tag']
    stagione_id = request.form['stagione_id']
    file = request.files['file']

    existing_episodio = Episodio.query.filter_by(nome=nome, stagione_id=stagione_id).first()

    if existing_episodio:
        return jsonify({"error": "L'episodio esiste già !"}), 400
    else:
        # controlli su file
        if file.filename == '':
                return jsonify({'error': 'File non immesso !'}), 400

        # cambio del nome del file per essere salvato
        serie_id = Stagione.query.filter_by(id=stagione_id).first().serie_id
        filename = secure_filename(file.filename)

        new_nome = f"{serie_id}_{stagione_id}_{nome.replace(' ', '_')}"
        ext = filename.split('.')[-1]
        new_filename = f"{new_nome}.{ext}"

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

        # creazione nuovo episodio
        new_episodio = Episodio(nome=nome, descrizione=descrizione, tag=tag, stagione_id=stagione_id, path=new_filename)

        try:
            db.session.add(new_episodio)    # aggiunge al db il nuovo episodio
            file.save(file_path)            # salva il file su disco
            db.session.commit()             # salva le modifiche nel db

            return jsonify({"message": f"Episodio {nome} aggiunto con successo !"}), 200

        except:
            return jsonify({"error": "Impossibile aggiungere l'episodio :/"}), 401


@app.route('/episodi_of/<int:id>', methods=['GET'])
@cross_origin()
def episodi_by_stagione(id):
    episodi = Episodio.query.filter_by(stagione_id=id).all()

    episodi = natsorted(episodi, key=lambda x: x.nome)  # ordina le stagioni in base al nome

    episodi_json = [x.as_dict() for x in episodi]

    return jsonify({'response': episodi_json}), 200


@app.route('/episodio/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_episodio(id):
    to_remove = Episodio.query.filter_by(id=id).first()

    if to_remove:
        file_path = file_path = os.path.join(app.config['UPLOAD_FOLDER'], to_remove.path)

        try:
            db.session.delete(to_remove)
            os.remove(file_path)
            db.session.commit()

            return jsonify({'message': 'Episodio eliminato !'}), 200
        except:
            return jsonify({'error': 'Impossibile eliminare l\'episodio !'}), 400

    return jsonify({'error': 'L\'episodio non esiste !'}), 400


@app.route('/episodio/<int:id>', methods=['GET'])
@cross_origin()
def get_episodio(id):
    episodio = Episodio.query.filter_by(id=id).first()

    episodio_json = episodio.as_dict()

    return jsonify({'response': episodio_json}), 200


@app.route('/episodio', methods=['PUT'])
@cross_origin()
def update_episodio():
    nome = request.form['nome']
    descrizione = request.form['descrizione']
    tag = request.form['tag']
    file = request.files['file']
    id = request.form['id']
    file_path = ''

    to_update = Episodio.query.filter_by(id=id).first()
    if to_update:
        to_update.nome = nome
        to_update.descrizione = descrizione
        to_update.tag = tag

        # carica e salva il nuovo file
        stagione_id = to_update.stagione_id
        if file.filename != '':
            serie_id = Stagione.query.filter_by(id=stagione_id).first().serie_id
            filename = secure_filename(file.filename)

            new_nome = f"{serie_id}_{stagione_id}_{nome.replace(' ', '_')}"
            ext = filename.split('.')[-1]
            new_filename = f"{new_nome}.{ext}"

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

        try:
            if file_path != '':
                file.save(file_path)

            db.session.commit()

            return jsonify({'message': 'Episodio aggiornato con successo !'}), 200

        except:
            return jsonify({'error': 'Impossibile aggiornare i dati !'}), 400
        
    return jsonify({'error': 'Episodio inesistente !'}),400