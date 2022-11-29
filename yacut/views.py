from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from yacut import app, db
from yacut.forms import CutForm
from yacut.models import URL_map


@app.route('/')
def index_view():
    return render_template('index.html')


