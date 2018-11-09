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
from .models import *
from .services import BaseService

# Cache requests
cache = Cache()

# Define the blueprint: 'api', set its url prefix: app.url/api
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Initialize services
SiteService = BaseService(('Tag', 'Tags'), Site, SiteSchema)
ZoneService = BaseService(('Zone', 'Zones'), Zone, ZoneSchema)
ProcessService = BaseService(('Process', 'Processes'), Process, ProcessSchema)
ServerService = BaseService(('Server', 'Servers'), Server, ServerSchema)
TagService = BaseService(('Tag', 'Tags'), Tag, TagSchema)
RecordService = BaseService(('Record', 'Records'), Record, RecordSchema)


# ----> SITES <-----

@api_bp.route('/sites', methods=['GET'])
@cache.cached()
def get_sites():
    """ Get all Sites """
    # pagination page, only positive values
    page = int(request.args.get('page', 1))
    # number of results displayed
    count = int(request.args.get('count', 0))

    return jsonify(SiteService.get_all(page, count))


@api_bp.route('/sites/<int:id>', methods=['GET'])
@cache.cached()
def get_site():
    """ Get Sites with specified id """
    return jsonify(SiteService.get_by_id(id))


@api_bp.route('/sites/create', methods=['POST'])
def create_site():
    """ Create a new Site """
    # checks request exists and have title attribute
    if not request.json or not {'name'}.issubset(set(request.json)):
        abort(400)  # bad request error

    return jsonify(SiteService.create(**request.json)), 201  # created


# ----> ZONES <-----

@api_bp.route('/zones', methods=['GET'])
@cache.cached()
def get_zones():
    """ Get all Zones """
    # pagination page, only positive values
    page = int(request.args.get('page', 1))
    # number of results displayed
    count = int(request.args.get('count', 0))

    return jsonify(ZoneService.get_all(page, count))


@api_bp.route('/zones/<int:id>', methods=['GET'])
@cache.cached()
def get_zone():
    """ Get Zones with specified id """
    return jsonify(ZoneService.get_by_id(id))


@api_bp.route('/zones/create', methods=['POST'])
def create_zone():
    """ Create a new Zone """
    # checks request exists and have title attribute
    if not request.json or not {'name', 'site_id'}.issubset(set(request.json)):
        abort(400)  # bad request error

    return jsonify(ZoneService.create(**request.json)), 201  # created


# ----> PROCESSES <-----

@api_bp.route('/processes', methods=['GET'])
@cache.cached()
def get_processes():
    """ Get all Processes """
    # pagination page, only positive values
    page = int(request.args.get('page', 1))
    # number of results displayed
    count = int(request.args.get('count', 0))

    return jsonify(ProcessService.get_all(page, count))


@api_bp.route('/processes/<int:id>', methods=['GET'])
@cache.cached()
def get_process():
    """ Get process with specified id """
    return jsonify(ProcessService.get_by_id(id))


@api_bp.route('/processes/create', methods=['POST'])
def create_process():
    """ Create a new Tag """
    # checks request exists and have title attribute
    if not request.json or not {'name', 'zone_id'}.issubset(set(request.json)):
        abort(400)  # bad request error

    return jsonify(ProcessService.create(**request.json)), 201  # created


@api_bp.route('/processes/qrcode/<int:id>', methods=['GET'])
@cache.cached(timeout=3600)  # cache for 1 hour
def get_process_qrcode(id):
    """ Get QRCode image for Tag """
    img = qrcode.generate('process', id)

    return send_file(img, mimetype='image/png')


# ----> SERVERS <-----

@api_bp.route('/servers', methods=['GET'])
@cache.cached()
def get_servers():
    """ Get all Servers """
    # pagination page, only positive values
    page = int(request.args.get('page', 1))
    # number of results displayed
    count = int(request.args.get('count', 0))

    return jsonify(ServerService.get_all(page, count))


@api_bp.route('/servers/<int:id>', methods=['GET'])
@cache.cached()
def get_server():
    """ Get Servers with specified id """
    return jsonify(ServerService.get_by_id(id))


@api_bp.route('/servers/create', methods=['POST'])
def create_server():
    """ Create a new Server """
    # checks request exists and have title attribute
    if not request.json or not {'uid'}.issubset(set(request.json)):
        abort(400)  # bad request error

    return jsonify(ServerService.create(**request.json)), 201  # created


# ----> TAGS <-----

@api_bp.route('/tags', methods=['GET'])
@cache.cached()
def get_tags():
    """ Get all Tags """
    # pagination page, only positive values
    page = int(request.args.get('page', 1))
    # number of results displayed
    count = int(request.args.get('count', 0))

    return jsonify(TagService.get_all(page, count))


@api_bp.route('/tags/<int:id>', methods=['GET'])
@cache.cached()
def get_tag(id):
    """ Get Tag with specified id """
    return jsonify(TagService.get_by_id(id))


@api_bp.route('/tags/create', methods=['POST'])
def create_tag():
    """ Create a new Tag """
    # checks request exists and have title attribute
    if not request.json or not {'name', 'alias', 'server_id'}.issubset(set(request.json)):
        abort(400)  # bad request error

    return jsonify(TagService.create(**request.json)), 201  # created


@api_bp.route('/tags/qrcode/<int:id>', methods=['GET'])
@cache.cached(timeout=3600)  # cache for 1 hour
def get_tag_qrcode(id):
    """ Get QRCode image for Tag """
    img = qrcode.generate('tag', id)

    return send_file(img, mimetype='image/png')


# ----> RECORDS <-----

@api_bp.route('/records', methods=['GET'])
@cache.cached()
def get_records():
    """ Return all Records """
    # pagination page, only positive values
    page = int(request.args.get('page', 1))
    # number of results displayed
    count = int(request.args.get('count', 0))

    return jsonify(RecordService.get_all(page, count))


@api_bp.route('/records/<int:id>', methods=['GET'])
@cache.cached()
def get_record(id):
    """ Return Record with specified id """
    return jsonify(RecordService.get_by_id(id))


@api_bp.route('/records/create', methods=['POST'])
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
