from flask import render_template, redirect, url_for, request, flash
from app import *


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')