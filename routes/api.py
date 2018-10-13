from flask import Blueprint, jsonify

import data

api_app = Blueprint('api', __name__, url_prefix='/api')

@api_app.route('/countries')
def countries():
    return jsonify(data.get_countries())


@api_app.route('/country/<int:code>')
def country_by_code(code):
    return jsonify(data.country_for_code(code))
