import random
import string

from flask import flash, redirect, render_template

from yacut import app, db
from yacut.forms import CutForm
from yacut.models import URLMap

letters = string.ascii_lowercase + string.digits
not_unique_error = 'Имя {} уже занято!'


def check_short_id(short_id):
    if URLMap.query.filter_by(short=short_id).first() is None:
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
        flash(f'Имя {short_id} уже занято!', 'link-taken')
        return render_template('index.html', form=form)
    short_link = URLMap(
        original=form.original.data,
        short=short_id,
    )
    db.session.add(short_link)
    db.session.commit()
    return render_template('index.html', url=short_link, form=form)


@app.route('/<short_id>')
def follow_link(short_id):
    db_object = URLMap.query.filter(URLMap.short == short_id).first_or_404()
    original_link = db_object.original
    return redirect(original_link)
