from flask import render_template, redirect, url_for, request, flash
from app import *


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/serie', methods=['GET'])
def serie():
    return render_template('series.html')


@app.route('/add_serie', methods=['GET'])
def add_serie():
    return render_template('add_serie.html')