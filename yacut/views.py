from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from yacut import app, db
from yacut.forms import CutForm
from yacut.models import URL_map


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = CutForm()
    if form.validate_on_submit():
        short_link = URL_map(
            original_link=form.original_link.data,
            short=form.custom_id.data,
        )
        db.session.add(short_link)
        db.session.commit()
    return render_template('index.html', form=form)


