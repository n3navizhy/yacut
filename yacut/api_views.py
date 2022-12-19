
from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.models import get_api_object, new_object
from yacut.error_handlers import APIErrors

api_unique_error = 'Имя "{}" уже занято.'


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if not data:
        raise APIErrors('Отсутствует тело запроса')
    if 'url' not in data:
        raise APIErrors('\"url\" является обязательным полем!')
    try:
        new_url = new_object(data.get('custom_id'), data.get('url'))
    except ValueError:
        raise APIErrors('Указано недопустимое имя для короткой ссылки')
    except NameError:
        raise APIErrors(api_unique_error.format(data.get('custom_id')))
    return jsonify(new_url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    try:
        db_object = get_api_object(short_id)
    except NameError:
        raise APIErrors('Указанный id не найден', HTTPStatus.NOT_FOUND)
    original_url = db_object.original
    return jsonify({'url': original_url}), HTTPStatus.OK
