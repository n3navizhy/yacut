
from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.models import get_api_object, new_object
from yacut.error_handlers import APIErrors

API_UNIQUE_ERROR = 'Имя "{}" уже занято.'
INCORRECT_NAME_ERROR = 'Указано недопустимое имя для короткой ссылки'
NONE_BODY_REQUEST = 'Отсутствует тело запроса'
REQUIRED_FIELD = '"url" является обязательным полем!'
ID_NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if not data:
        raise APIErrors(NONE_BODY_REQUEST)
    if 'url' not in data:
        raise APIErrors(REQUIRED_FIELD)
    try:
        new_url = new_object(data.get('custom_id'), data.get('url'))
    except ValueError:
        raise APIErrors(INCORRECT_NAME_ERROR)
    except NameError:
        raise APIErrors(API_UNIQUE_ERROR.format(data.get('custom_id')))
    return jsonify(new_url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    try:
        db_object = get_api_object(short_id)
    except NameError:
        raise APIErrors(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    original_url = db_object.original
    return jsonify({'url': original_url}), HTTPStatus.OK
