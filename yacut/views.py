import random
import string

from flask import abort, flash, redirect, render_template

from yacut import app, db
from yacut.forms import CutForm
from yacut.models import URL_map

letters = string.ascii_lowercase
not_unique_error = 'Имя  уже занято!'


def check_short_id(short_id):
    if URL_map.query.filter_by(short=short_id).first() is None:
        return True
    return False


def get_unique_short_id():
    short_id = ''.join(random.choice(letters) for i in range(6))
    if check_short_id(short_id):
        return short_id
    return get_unique_short_id()


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = CutForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short_id = form.custom_id.data
    if not short_id:
        short_id = get_unique_short_id()
    elif not check_short_id(short_id):
        flash(not_unique_error)
        return render_template('index.html', form=form)
    short_link = URL_map(
        original=form.original.data,
        short=short_id,
    )
    db.session.add(short_link)
    db.session.commit()
    return render_template('index.html', url=short_link, form=form)


@app.route('/<short_id>')
def follow_link(short_id):
    db_object = URL_map.query.filter(URL_map.short == short_id).first_or_404()
    original_link = db_object.original
    return redirect(original_link)
