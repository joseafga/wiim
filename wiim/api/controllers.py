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
from .services import Record, Tag, Server, Process, Zone, Site
from .services import RecordService, TagService, ServerService, \
    ProcessService, ZoneService, SiteService

# Cache requests
cache = Cache()

# Define the blueprint: 'api', set its url prefix: app.url/api
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


# ----> GET MULTIPLES <-----

@api_bp.route('/sites', methods=['GET'])
@cache.cached()
def get_sites():
    """ Get all Sites """
    # pagination page, only positive values
    page = int(request.args.get('page', 1))
    # number of results displayed
    count = int(request.args.get('count', 0))

    return jsonify(SiteService.get_all(page, count))


@api_bp.route('/zones', methods=['GET'])
@api_bp.route('/sites/<int:id>/zones', methods=['GET'])
@cache.cached()
def get_zones(id=None):
    """ Get all Zones """
    # pagination page, only positive values
    page = int(request.args.get('page', 1))
    # number of results displayed
    count = int(request.args.get('count', 0))

    if id is None:
        return jsonify(ZoneService.get_all(page, count))

    # get only zones from specified site
    filters = (Zone.site_id == id)

    return jsonify(ZoneService.get_all(page, count, filters))


@api_bp.route('/processes', methods=['GET'])
@api_bp.route('/zones/<int:id>/processes', methods=['GET'])
@cache.cached()
def get_processes(id=None):
    """ Get all Processes """
    # pagination page, only positive values
    page = int(request.args.get('page', 1))
    # number of results displayed
    count = int(request.args.get('count', 0))

    if id is None:
        return jsonify(ProcessService.get_all(page, count))

    # get only processes from specified server
    filters = (Process.zone_id == id)

    return jsonify(ProcessService.get_all(page, count, filters))


@api_bp.route('/servers', methods=['GET'])
@cache.cached()
def get_servers():
    """ Get all Servers """
    # pagination page, only positive values
    page = int(request.args.get('page', 1))
    # number of results displayed
    count = int(request.args.get('count', 0))

    return jsonify(ServerService.get_all(page, count))


@api_bp.route('/tags', methods=['GET'])
@api_bp.route('/process/<int:id>/tags', methods=['GET'])
@api_bp.route('/servers/<int:id>/tags', methods=['GET'])
@cache.cached()
def get_tags(id=None):
    """ Get all Tags """
    # pagination page, only positive values
    page = int(request.args.get('page', 1))
    # number of results displayed
    count = int(request.args.get('count', 0))

    if id is None:
        return jsonify(TagService.get_all(page, count))

    # get only processes from specified server
    filters = (Tag.server_id == id)

    return jsonify(TagService.get_all(page, count, filters))


@api_bp.route('/records', methods=['GET'])
@api_bp.route('/tags/<int:id>/records', methods=['GET'])
@cache.cached()
def get_records():
    """ Return all Records """
    # pagination page, only positive values
    page = int(request.args.get('page', 1))
    # number of results displayed
    count = int(request.args.get('count', 0))

    if id is None:
        return jsonify(RecordService.get_all(page, count))

    # get only processes from specified server
    filters = (Record.tag_id == id)

    return jsonify(RecordService.get_all(page, count, filters))


# ----> GET SINGLE <-----

@api_bp.route('/sites/<int:id>', methods=['GET'])
@cache.cached()
def get_site(id):
    """ Get Sites with specified id """
    return jsonify(SiteService.get_by_id(id))


@api_bp.route('/zones/<int:id>', methods=['GET'])
@cache.cached()
def get_zone(id):
    """ Get Zones with specified id """
    return jsonify(ZoneService.get_by_id(id))


@api_bp.route('/processes/<int:id>', methods=['GET'])
@cache.cached()
def get_process(id):
    """ Get process with specified id """
    return jsonify(ProcessService.get_by_id(id))


@api_bp.route('/servers/<int:id>', methods=['GET'])
@cache.cached()
def get_server(id):
    """ Get Servers with specified id """
    return jsonify(ServerService.get_by_id(id))


@api_bp.route('/tags/<int:id>', methods=['GET'])
@cache.cached()
def get_tag(id):
    """ Get Tag with specified id """
    return jsonify(TagService.get_by_id(id))


@api_bp.route('/records/<int:id>', methods=['GET'])
@cache.cached()
def get_record(id):
    """ Return Record with specified id """
    return jsonify(RecordService.get_by_id(id))


# ----> CREATE <-----

@api_bp.route('/sites', methods=['POST'])
def create_site():
    """ Create a new Site """
    # checks request exists and have title attribute
    if not request.json or not {'name'}.issubset(set(request.json)):
        abort(400)  # bad request error

    return jsonify(SiteService.create(**request.json)), 201  # created


@api_bp.route('sites/<int:site_id>/zones', methods=['POST'])
def create_zone(site_id):
    """ Create a new Zone """
    # checks request exists and have title attribute
    if not request.json or not {'name'}.issubset(set(request.json)):
        abort(400)  # bad request error

    # set site id
    request.json['site_id'] = site_id

    return jsonify(ZoneService.create(**request.json)), 201  # created


@api_bp.route('/processes', methods=['POST'])
def create_process():
    """ Create a new Tag """
    # checks request exists and have title attribute
    if not request.json or not {'name', 'zone_id'}.issubset(set(request.json)):
        abort(400)  # bad request error

    return jsonify(ProcessService.create(**request.json)), 201  # created


@api_bp.route('/servers', methods=['POST'])
def create_server():
    """ Create a new Server """
    # checks request exists and have title attribute
    if not request.json or not {'uid'}.issubset(set(request.json)):
        abort(400)  # bad request error

    return jsonify(ServerService.create(**request.json)), 201  # created


@api_bp.route('/servers/<int:server_id>/tags', methods=['POST'])
def create_tag(server_id):
    """ Create a new Tag """
    # checks request exists and have title attribute
    if not request.json or not {'name', 'alias', 'processes'}.issubset(set(request.json)):
        abort(400)  # bad request error

    # set server id
    request.json['server_id'] = server_id

    return jsonify(TagService.create(**request.json)), 201  # created


@api_bp.route('/records', methods=['POST'])
def create_record():
    """ Create a new Record """
    # checks request exists and have title attribute
    if not request.json or not {'time_opc', 'value', 'tag_id'}.issubset(set(request.json)):
        abort(400)  # bad request error

    return jsonify(RecordService.create(**request.json)), 201  # created


# ----> DELETE <-----

@api_bp.route('/sites/<int:id>', methods=['DELETE'])
def destroy_site(id):
    """ Delete site with specified id """
    return jsonify(SiteService.destroy_by_id(id)), 204  # deleted


@api_bp.route('/zones/<int:id>', methods=['DELETE'])
def destroy_zone(id):
    """ Delete zone with specified id """
    return jsonify(ZoneService.destroy_by_id(id)), 204  # deleted


@api_bp.route('/processes/<int:id>', methods=['DELETE'])
def destroy_process(id):
    """ Delete process with specified id """
    return jsonify(ProcessService.destroy_by_id(id)), 204  # deleted


@api_bp.route('/servers/<int:id>', methods=['DELETE'])
def destroy_server(id):
    """ Delete server with specified id """
    return jsonify(ServerService.destroy_by_id(id)), 204  # deleted


@api_bp.route('/tags/<int:id>', methods=['DELETE'])
def destroy_tag(id):
    """ Delete tag with specified id """
    return jsonify(TagService.destroy_by_id(id)), 204  # deleted


@api_bp.route('/records/<int:id>', methods=['DELETE'])
def destroy_record(id):
    """ Delete record with specified id """
    return jsonify(RecordService.destroy_by_id(id)), 204  # deleted


# ----> QRCODE <-----

@api_bp.route('/processes/qrcode/<int:id>', methods=['GET'])
@cache.cached(timeout=3600)  # cache for 1 hour
def get_process_qrcode(id):
    """ Get QRCode image for Tag """
    img = qrcode.generate('process', id)

    return send_file(img, mimetype='image/png')


@api_bp.route('/tags/qrcode/<int:id>', methods=['GET'])
@cache.cached(timeout=3600)  # cache for 1 hour
def get_tag_qrcode(id):
    """ Get QRCode image for Tag """
    img = qrcode.generate('tag', id)

    return send_file(img, mimetype='image/png')


# ----> TODO <-----

@api_bp.route('/tags/test', methods=['GET'])
def since_tag():
    """ Delete tag with specified id """
    return jsonify(TagService.since())


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
    return make_response(jsonify(error={
        'msg': str(e)
    }), 400)
