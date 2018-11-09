"""
wiim.api.controller

Include routes management for API

:copyright: © 2018 by José Almeida.
:license: CC BY-NC 4.0, see LICENSE for more details.
"""

from flask import Blueprint, make_response, abort, request, send_file, jsonify
from flask_caching import Cache
from werkzeug.exceptions import HTTPException
# application imports
from wiim import qrcode
from wiim.api.services import TagService, RecordService

# Cache requests
cache = Cache()

# Define the blueprint: 'api', set its url prefix: app.url/api
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


# ----> PROCESSES <-----

@api_bp.route('/processes', strict_slashes=False, methods=['GET'])
@cache.cached()
def get_processes():
    """ Get all processes """
    # return jsonify({'tags': tags})


@api_bp.route('/processes/<int:id>', strict_slashes=False, methods=['GET'])
@cache.cached()
def get_process():
    """ Get process with specified id """
    # tag = [tag for tag in tags if tag['id'] == id]
    # if len(tag) == 0:
    #     abort(404)  # not found error

    # return jsonify({'tag': tag[0]})


# ----> TAGS <-----

@api_bp.route('/tags', strict_slashes=False, methods=['GET'])
@cache.cached()
def get_tags():
    """ Get all Tags """
    # pagination page, only positive values
    page = int(request.args.get('page', 1))
    # number of results displayed
    count = int(request.args.get('count', 0))

    return jsonify(TagService.get_all(page, count))


@api_bp.route('/tags/<int:id>', strict_slashes=False, methods=['GET'])
@cache.cached()
def get_tag(id):
    """ Get Tag with specified id """
    return jsonify(TagService.get(id))


@api_bp.route('/tags/create', strict_slashes=False, methods=['POST'])
@cache.cached()
def create_tag():
    """ Create a new Tag """
    # checks request exists and have title attribute
    if not request.json or not {'name', 'alias', 'server_id'}.issubset(set(request.json)):
        abort(400)  # bad request error

    return jsonify(TagService.create(**request.json)), 201  # created


@api_bp.route('/tags/qrcode/<int:id>', strict_slashes=False, methods=['GET'])
@cache.cached(timeout=3600)  # cache for 1 hour
def get_qrcode(id):
    """ Get QRCode image for Tag """
    img = qrcode.generate('tag', id)

    return send_file(img, mimetype='image/png')


# ----> RECORDS <-----

@api_bp.route('/records', strict_slashes=False, methods=['GET'])
@cache.cached()
def get_records():
    """ Return all Records """
    # pagination page, only positive values
    page = int(request.args.get('page', 1))
    # number of results displayed
    count = int(request.args.get('count', 0))

    return jsonify(RecordService.get_all(page, count))


@api_bp.route('/records/<int:id>', strict_slashes=False, methods=['GET'])
@cache.cached()
def get_record(id):
    """ Return Record with specified id """
    return jsonify(RecordService.get(id))


@api_bp.route('/records/create', strict_slashes=False, methods=['POST'])
@cache.cached()
def create_record():
    """ Create a new Record """
    # checks request exists and have title attribute
    if not request.json or not {'time_opc', 'value', 'tag_id'}.issubset(set(request.json)):
        abort(400)  # bad request error

    return jsonify(RecordService.create(**request.json)), 201  # created


# ----> ERRORS <-----

@api_bp.errorhandler(Exception)
def handle_error(e):
    # HTTP error exception
    if isinstance(e, HTTPException):
        return make_response(jsonify({
            'status': 'error',
            'code': str(e.code),
            'name': e.name,
            'message': e.description
        }), e.code)

    # default error with bad request code
    return make_response(jsonify({
        'status': 'error',
        'msg': str(e)
    }), 400)
