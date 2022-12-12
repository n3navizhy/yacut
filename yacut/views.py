
from flask import redirect, render_template

from yacut import app
from yacut.forms import CutForm
from .models import URLMap, new_object, get_unique_short_id, check_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = CutForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    custom_id = form.custom_id.data
    short_link = new_object(form, custom_id)
    return render_template('index.html', url=short_link, form=form)


@app.route('/<short_id>')
def follow_link(short_id):
    return redirect(URLMap().get_object(short_id))

