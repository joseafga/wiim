"""
wiim.api.controllers

Include routes and database functions for API

:copyright: © 2018 by José Almeida.
:license: CC BY-NC 4.0, see LICENSE for more details.
"""

from flask import Blueprint, make_response, abort, request, send_file, jsonify, current_app as app
from werkzeug.exceptions import HTTPException
# application imports
from wiim import qrcode
from wiim.api.controllers import TagController, RecordController

# Define the blueprint: 'api', set its url prefix: app.url/api
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


def routes(name, Controller):
    @api_bp.route('/' + name, methods=['GET'])
    def get_tags():
        """ Get all Items """
        # pagination page, only positive values
        page = abs(int(request.args.get('page', 1)))
        # number of results displayed
        count = int(request.args.get('count', app.config['WIIM_COUNT_LIMIT']))

        return jsonify(Controller.get_all(page, count))

    @api_bp.route('/' + name + '/<int:id>', methods=['GET'])
    def get_tag():
        """ Get Item with specified id """
        return jsonify(Controller.get(id))

    @api_bp.route('/' + name + '/create', methods=['POST'])
    def create_tag():
        """ Create a new Item """
        # checks request exists and have title attribute
        if not request.json or not {'name', 'alias', 'server_id'}.issubset(set(request.json)):
            abort(400)  # bad request error

        return jsonify(Controller.create(**request.json)), 201  # created


# ----> PROCESSES <-----

@api_bp.route('/processes', methods=['GET'])
def get_processes():
    """ Get all processes """
    # return jsonify({'tags': tags})


@api_bp.route('/processes/<int:id>', methods=['GET'])
def get_process():
    """ Get process with specified id """
    # tag = [tag for tag in tags if tag['id'] == id]
    # if len(tag) == 0:
    #     abort(404)  # not found error

    # return jsonify({'tag': tag[0]})


# ----> TAGS <-----

@api_bp.route('/tags', methods=['GET'])
def get_tags():
    """ Get all Tags """
    # pagination page, only positive values
    page = abs(int(request.args.get('page', 1)))
    # number of results displayed
    count = int(request.args.get('count', app.config['WIIM_COUNT_LIMIT']))

    return jsonify(TagController.get_all(page, count))


@api_bp.route('/tags/<int:id>', methods=['GET'])
def get_tag(id):
    """ Get Tag with specified id """
    return jsonify(TagController.get(id))


@api_bp.route('/tags/create', methods=['POST'])
def create_tag():
    """ Create a new Tag """
    # checks request exists and have title attribute
    if not request.json or not {'name', 'alias', 'server_id'}.issubset(set(request.json)):
        abort(400)  # bad request error

    return jsonify(TagController.create(**request.json)), 201  # created


@api_bp.route('/tags/qrcode/<int:id>', methods=['GET'])
def get_qrcode(id):
    """ Get QRCode image for Tag """
    img = qrcode.generate('tag', id)
    return send_file(img, mimetype='image/png')


# ----> RECORDS <-----

@api_bp.route('/records', methods=['GET'])
def get_records():
    """ Return all Records """
    # pagination page, only positive values
    page = abs(int(request.args.get('page', 1)))
    # number of results displayed
    count = int(request.args.get('count', app.config['WIIM_COUNT_LIMIT']))

    return jsonify(RecordController.get_all(page, count))


@api_bp.route('/records/<int:id>', methods=['GET'])
def get_record(id):
    """ Return Record with specified id """
    return jsonify(RecordController.get(id))


@api_bp.route('/records/create', methods=['POST'])
def create_record():
    """ Create a new Record """
    # checks request exists and have title attribute
    if not request.json or not {'time_opc', 'value', 'tag_id'}.issubset(set(request.json)):
        abort(400)  # bad request error

    return jsonify(RecordController.create(**request.json)), 201  # created


# ----> ERRORS <-----

@api_bp.errorhandler(Exception)
def handle_error(e):
    # HTTP error exception
    if isinstance(e, HTTPException):
        return make_response(jsonify(error={
            'code': str(e.code),
            'name': e.name,
            'message': e.description
        }), e.code)

    # default error with bad request code
    return make_response(jsonify(error=str(e)), 400)