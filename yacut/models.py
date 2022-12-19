import random
import re

from datetime import datetime
from flask import url_for

from settings import SHORT_LINK_LENGTH, LINK_SAMPLE, LETTERS
from yacut import db

FIELD_NAMES = {'original': 'url', 'short': 'custom_id'}

ATTEMPTS = 999


def check_short_id(custom_id):
    return URLMap.query.filter_by(short=custom_id).first() is None


def get_unique_short_id():
    for i in range(ATTEMPTS):
        custom_id = ''.join(random.choices(LETTERS, k=SHORT_LINK_LENGTH))
        if check_short_id(custom_id):
            return custom_id
    raise ValueError("БД переполнено")


def new_object(custom_id, url):
    if custom_id is not None:
        if not check_short_id(custom_id):
            raise NameError
        if custom_id == '' or custom_id is None:
            custom_id = get_unique_short_id()
        elif not re.match(LINK_SAMPLE, custom_id) or len(custom_id) >= 16:
            raise ValueError
    else:
        custom_id = get_unique_short_id()
    new_url = URLMap(
        original=url,
        short=custom_id,
    )
    db.session.add(new_url)
    db.session.commit()
    return new_url


def get_object_or_404(short_id):
    return URLMap.query.filter(URLMap.short == short_id).first_or_404()


def get_api_object(short_id):
    db_object = URLMap.query.filter(URLMap.short == short_id).first()
    if db_object is None:
        raise NameError
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

