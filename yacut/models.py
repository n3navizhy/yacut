import random

from datetime import datetime
from flask import url_for, render_template, flash
from yacut import db
from settings import LETTERS

FIELD_NAMES = {'original': 'url', 'short': 'custom_id'}
not_unique_error = 'Имя {} уже занято!'


def check_short_id(custom_id):
    if URLMap.query.filter_by(short=custom_id).first() is None:
        return True
    return False


def get_unique_short_id():
    custom_id = ''.join(random.choice(LETTERS) for i in range(6))
    if check_short_id(custom_id):
        return custom_id
    return get_unique_short_id()


def new_object(form, custom_id):
    if not custom_id:
        custom_id = get_unique_short_id()
    elif not check_short_id(custom_id):
        flash(not_unique_error.format(custom_id), 'error-message')
        return render_template('index.html', form=form)
    short = URLMap(
        original=form.original_link.data,
        short=custom_id,
    )
    db.session.add(short)
    db.session.commit()
    return short


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.Text, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def get_object(self, short_id):
        return self.query.filter(URLMap.short ==
                                 short_id).first_or_404().original

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('index_view', _external=True) + self.short
        )

    def from_dict(self, data):
        for field_db, field_inp in FIELD_NAMES.items():
            if field_inp in data:
                setattr(self, field_db, data[field_inp])
