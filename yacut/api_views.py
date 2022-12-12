
from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.models import get_api_object, new_api_object
from yacut.error_handlers import APIErrors


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if not data:
        raise APIErrors('Отсутствует тело запроса')
    if 'url' not in data:
        raise APIErrors('\"url\" является обязательным полем!')
    new_url = new_api_object(data)
    return jsonify(new_url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    db_object = get_api_object(short_id)
    original_url = db_object.original
    return jsonify({'url': original_url}), HTTPStatus.OK
