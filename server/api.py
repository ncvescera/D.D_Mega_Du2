from flask import request, send_from_directory, jsonify
from flask_cors import cross_origin
from app import *
from models import *
import json
from werkzeug.utils import secure_filename
import os

@app.route('/test')
def test():
    return  send_from_directory(app.config['UPLOAD_FOLDER'], 'enduring value-rHj3NI2x7n0.mp4')


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
    print(request.form)
    print(request.json)
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


@app.route('/stagione/<int:serie_id>', methods=['GET'])
@cross_origin()
def stagioni_py_serie(serie_id):
    stagioni = Stagione.query.filter_by(serie_id=serie_id)

    stagioni_json = [x.as_dict() for x in stagioni]

    return jsonify({"response": stagioni_json}), 200
