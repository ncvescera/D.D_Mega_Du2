from flask import request, send_from_directory
from app import *
from models import *
import json
from werkzeug.utils import secure_filename
import os

@app.route('/test')
def test():
    return  send_from_directory(app.config['UPLOAD_FOLDER'], 'enduring value-rHj3NI2x7n0.mp4')


@app.route('/serie', methods=['GET'])
def all_serie():
    series = Serie.query.all()

    series_json = [x.as_dict() for x in series] # trasforma ogni serie in dizionario per essere convertito in json

    return f'{request.args.get("callback")}({json.dumps({"response": series_json})})', 200


@app.route('/serie/<int:id>', methods=['GET'])
def get_serie(id):
    serie = Serie.query.filter_by(id=id).first()

    serie_json = serie.as_dict()

    return json.dumps({'response': serie_json}), 200


@app.route('/serie', methods=['POST'])
def add_serie():
    # prende i dati del form
    nome            = request.form['nome']
    descrizione     = request.form['descrizione']
    tag             = request.form['tag']
    
    existing_serie = Serie.query.filter_by(nome=nome).first()

    if existing_serie:
        return json.dumps({'error': 'La serie esiste già !'}), 400
    else:
        new_serie = Serie(nome=nome, descrizione=descrizione, tag=tag)

        try:
            db.session.add(new_serie)
            db.session.commit()

            return json.dumps({'message': f'Serie {nome} aggiunta con successo !'}), 200

        except:
            return json.dumps({'error': 'Impossibile aggiungere la serie :/'}), 401


@app.route('/serie/<int:id>', methods=['DELETE'])
def rimuovi_serie(id):
    #TODO: eliminare a cascata gli episodi e le stagioni !!!

    to_remove = Serie.query.filter_by(id=id).first()

    if to_remove:
        try:
            db.session.delete(to_remove)
            db.session.commit()

            return json.dumps({'message': 'Serie eliminata !'}), 200
        except:
            return json.dumps({'error': 'Impossibile eliminare la serie !'}), 400

    return json.dumps({'error': 'La serie non esiste !'}), 400


@app.route('/serie', methods=['PUT'])
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

            return json.dumps({'message': 'Serie aggiornata con successo !'}), 200

        except:
            return json.dumps({'error': 'Impossibile aggiornare i dati !'}), 400
        
    return json.dumps({'error': 'Serie inesistente !'}),400