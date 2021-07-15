from flask import render_template, redirect, url_for, request, flash
from app import *


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/serie', methods=['GET'])
def serie():
    return render_template('series.html')


@app.route('/serie/<int:id>', methods=['GET'])
def serie_by_id(id):
    return render_template('serie_by_id.html', serie_id=id)

@app.route('/add_serie', methods=['GET'])
def add_serie():
    return render_template('add_serie.html')

@app.route('/stagione/<int:id>', methods=['GET'])
def stagione(id):
    return render_template('stagione.html', stagione_id=id)

@app.route('/episodio/<int:id>', methods=['GET'])
def episodio(id):
    return render_template('episodio.html', episodio_id=id)