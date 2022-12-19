from flask import redirect, render_template, flash

from yacut import app
from yacut.forms import CutForm
from .models import new_object, get_object_or_404

not_unique_error = 'Имя {} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = CutForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    custom_id = form.custom_id.data
    try:
        short_link = new_object(custom_id, form.original_link.data)
    except NameError:
        flash(not_unique_error.format(custom_id), 'error-message')
        return render_template('index.html', form=form)
    return render_template('index.html', url=short_link, form=form)


@app.route('/<short_id>')
def follow_link(short_id):
    return redirect(get_object_or_404(short_id).original)
