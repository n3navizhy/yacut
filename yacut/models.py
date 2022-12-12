import random
import re
import sys

from http import HTTPStatus
from datetime import datetime
from flask import url_for, render_template, flash
from yacut import db
from yacut.error_handlers import APIErrors
from settings import SHORT_LINK_LENGTH, LINK_SAMPLE, LETTERS


FIELD_NAMES = {'original': 'url', 'short': 'custom_id'}
not_unique_error = 'Имя {} уже занято!'


def check_short_id(custom_id):
    return URLMap.query.filter_by(short=custom_id).first() is None


def get_unique_short_id():
    custom_id = ''.join(random.choices(LETTERS, k=SHORT_LINK_LENGTH))
    for i in range(sys.getrecursionlimit()):
        if check_short_id(custom_id):
            return custom_id
        return get_unique_short_id()
    raise Exception("БД переполнено")


def new_api_object(data):
    if 'custom_id' in data:
        custom_id = data.get('custom_id')
        if not check_short_id(custom_id):
            raise APIErrors(f'Имя "{custom_id}" уже занято.')
        if custom_id == '' or custom_id is None:
            data['custom_id'] = get_unique_short_id()
        elif not re.match(LINK_SAMPLE, custom_id):
            raise APIErrors('Указано недопустимое имя для короткой ссылки')
    else:
        data['custom_id'] = get_unique_short_id()
    new_url = URLMap()
    new_url.from_dict(data)
    db.session.add(new_url)
    db.session.commit()
    return new_url


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


def get_object(short_id):
    return URLMap.query.filter(URLMap.short == short_id).first_or_404()


def get_api_object(short_id):
    db_object = URLMap.query.filter(URLMap.short == short_id).first()
    if db_object is None:
        raise APIErrors('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return db_object


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.Text, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('index_view', _external=True) + self.short
        )

    def from_dict(self, data):
        for field_db, field_inp in FIELD_NAMES.items():
            if field_inp in data:
                setattr(self, field_db, data[field_inp])
