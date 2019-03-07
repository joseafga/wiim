"""
wiim.api.controller

Include routes management for API

:copyright: © 2018 by José Almeida
:license: AGPLv3/Commercial, see LICENSE file for more details
"""

from flask import Blueprint, make_response, request, send_file, jsonify
from flask_caching import Cache
from werkzeug.exceptions import HTTPException
# application imports
from wiim import qrcode
# from .services import Record, Tag, Server, Process, Zone, Site
from .services import record_service, tag_service, server_service,\
    process_service, zone_service, site_service, timeline_service

# Cache requests
cache = Cache()

# Define the blueprint: 'api', set its url prefix: app.url/api
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


# ----> GET MULTIPLES <-----

@api_bp.route('/sites', methods=['GET'])
@cache.cached()
def get_sites():
    """ Get all Sites """
    # get params from que url query
    count = int(request.args.get('count', 0))
    since = int(request.args.get('since', 0))
    order = request.args.get('order', None)

    return jsonify(site_service.get_all(count, since_id=since, order_by=order))


@api_bp.route('/zones', methods=['GET'])
@api_bp.route('/sites/<int:id>/zones', methods=['GET'])
@cache.cached()
def get_zones(id=None):
    """ Get all Zones """
    # get params from que url query
    count = int(request.args.get('count', 0))
    since = int(request.args.get('since', 0))
    order = request.args.get('order', None)

    if id is None:
        return jsonify(zone_service.get_all(count, since_id=since, order_by=order))

    # get only zones from specified site
    return jsonify(zone_service.get_all(
        count,
        since_id=since,
        order_by=order,
        filters={'site_id': id}
    ))


@api_bp.route('/processes', methods=['GET'])
@api_bp.route('/zones/<int:id>/processes', methods=['GET'])
@cache.cached()
def get_processes(id=None):
    """ Get all Processes """
    # get params from que url query
    count = int(request.args.get('count', 0))
    since = int(request.args.get('since', 0))
    order = request.args.get('order', None)

    if id is None:
        return jsonify(process_service.get_all(count, since_id=since, order_by=order))

    # get only processes from specified zone
    return jsonify(process_service.get_all(
        count,
        since_id=since,
        order_by=order,
        filters={'zone_id': id}
    ))


@api_bp.route('/servers', methods=['GET'])
@cache.cached()
def get_servers():
    """ Get all Servers """
    # get params from que url query
    count = int(request.args.get('count', 0))
    since = int(request.args.get('since', 0))
    order = request.args.get('order', None)

    return jsonify(server_service.get_all(count, since_id=since, order_by=order))


@api_bp.route('/tags', methods=['GET'])
@api_bp.route('/servers/<int:id>/tags', methods=['GET'])
@cache.cached()
def get_tags(id=None):
    """ Get all Tags """
    # get params from que url query
    count = int(request.args.get('count', 0))
    since = int(request.args.get('since', 0))
    order = request.args.get('order', None)

    if id is None:
        return jsonify(tag_service.get_all(count, since_id=since, order_by=order))

    # get only tags from specified server
    return jsonify(tag_service.get_all(
        count,
        since_id=since,
        order_by=order,
        filters={'server_id': id}
    ))


@api_bp.route('/processes/<int:id>/tags', methods=['GET'])
@cache.cached()
def get_process_tags(id):
    """ Get all tags from process """
    # get params from que url query
    count = int(request.args.get('count', 0))
    since = int(request.args.get('since', 0))
    order = request.args.get('order', None)

    # get only tags from specified process
    return jsonify(tag_service.get_by_process(id, count, since_id=since, order_by=order))


@api_bp.route('/records', methods=['GET'])
@api_bp.route('/tags/<int:id>/records', methods=['GET'])
def get_records(id=None):
    """ Return all Records """
    # get params from que url query
    count = int(request.args.get('count', 0))
    since = int(request.args.get('since', 0))
    order = request.args.get('order', None)

    if id is None:
        tags = request.args.getlist('tags')

        if tags:
            # get tags with id in list
            return jsonify(record_service.get_by_tags(
                tags,
                count,
                since_id=since,
                order_by=order
            ))

        # get all tags
        return jsonify(record_service.get_all(count, since_id=since, order_by=order))

    # get only records from specified tag
    return jsonify(record_service.get_all(
        count,
        since_id=since,
        order_by=order,
        filters={'tag_id': id}
    ))


@api_bp.route('/processes/<int:id>/records', methods=['GET'])
def get_process_records(id=None):
    """ Return all Records from Process """
    # get params from que url query
    count = int(request.args.get('count', 0))
    since = int(request.args.get('since', 0))
    order = request.args.get('order', None)

    # get only records from specified tag
    return jsonify(record_service.get_by_process(id, count, since_id=since, order_by=order))


@api_bp.route('/processes/<int:id>/timeline', methods=['GET'])
def get_process_timeline(id=None):
    """ Return all Records from Process """
    # get params from que url query
    count = int(request.args.get('count', 0))
    since = int(request.args.get('since', 0))
    order = request.args.get('order', None)

    # get only records from specified tag
    return jsonify(timeline_service.timeline(id, count, since_id=since, order_by=order))


# ----> GET SINGLE <-----

@api_bp.route('/sites/<int:id>', methods=['GET'])
@cache.cached()
def get_site(id):
    """ Get Sites with specified id """
    return jsonify(site_service.get_by_id(id))


@api_bp.route('/zones/<int:id>', methods=['GET'])
@cache.cached()
def get_zone(id):
    """ Get Zones with specified id """
    return jsonify(zone_service.get_by_id(id))


@api_bp.route('/processes/<int:id>', methods=['GET'])
@cache.cached()
def get_process(id):
    """ Get process with specified id """
    return jsonify(process_service.get_by_id(id))


@api_bp.route('/servers/<int:id>', methods=['GET'])
@cache.cached()
def get_server(id):
    """ Get Servers with specified id """
    return jsonify(server_service.get_by_id(id))


@api_bp.route('/tags/<int:id>', methods=['GET'])
@cache.cached()
def get_tag(id):
    """ Get Tag with specified id """
    return jsonify(tag_service.get_by_id(id))


@api_bp.route('/records/<int:id>', methods=['GET'])
@cache.cached()
def get_record(id):
    """ Return Record with specified id """
    return jsonify(record_service.get_by_id(id))


# ----> CREATE <-----

@api_bp.route('/sites', methods=['POST'])
def create_site():
    """ Create a new Site """
    return jsonify(site_service.create(**request.json)), 201  # created


@api_bp.route('/sites/<int:id>/zones', methods=['POST'])
def create_zone(id):
    """ Create a new Zone """
    # set site id
    request.json['site_id'] = id

    return jsonify(zone_service.create(**request.json)), 201  # created


@api_bp.route('/zones/<int:id>/processes', methods=['POST'])
def create_process(id):
    """ Create a new Tag """
    # set zone id
    request.json['zone_id'] = id

    return jsonify(process_service.create(**request.json)), 201  # created


@api_bp.route('/servers', methods=['POST'])
def create_server():
    """ Create a new Server """
    return jsonify(server_service.create(**request.json)), 201  # created


@api_bp.route('/servers/<int:id>/tags', methods=['POST'])
def create_tag(id):
    """ Create a new Tag """
    # set server id
    request.json['server_id'] = id

    return jsonify(tag_service.create(**request.json)), 201  # created


@api_bp.route('/tags/<int:id>/records', methods=['POST'])
def create_record(id):
    """ Create a new Record """
    # set tag id
    request.json['tag_id'] = id

    return jsonify(record_service.create(**request.json)), 201  # created


# ----> DELETE <-----

@api_bp.route('/sites/<int:id>', methods=['DELETE'])
def destroy_site(id):
    """ Delete site with specified id """
    return jsonify(site_service.destroy_by_id(id)), 204  # deleted


@api_bp.route('/zones/<int:id>', methods=['DELETE'])
def destroy_zone(id):
    """ Delete zone with specified id """
    return jsonify(zone_service.destroy_by_id(id)), 204  # deleted


@api_bp.route('/processes/<int:id>', methods=['DELETE'])
def destroy_process(id):
    """ Delete process with specified id """
    return jsonify(process_service.destroy_by_id(id)), 204  # deleted


@api_bp.route('/servers/<int:id>', methods=['DELETE'])
def destroy_server(id):
    """ Delete server with specified id """
    return jsonify(server_service.destroy_by_id(id)), 204  # deleted


@api_bp.route('/tags/<int:id>', methods=['DELETE'])
def destroy_tag(id):
    """ Delete tag with specified id """
    return jsonify(tag_service.destroy_by_id(id)), 204  # deleted


@api_bp.route('/records/<int:id>', methods=['DELETE'])
def destroy_record(id):
    """ Delete record with specified id """
    return jsonify(record_service.destroy_by_id(id)), 204  # deleted


# ----> QRCODE <-----

@api_bp.route('/processes/<int:id>/qrcode', methods=['GET'])
@cache.cached(timeout=3600)  # cache for 1 hour
def get_process_qrcode(id):
    """ Get QRCode image for Tag """
    img = qrcode.generate('process:' + str(id))

    return send_file(img, mimetype='image/png')


@api_bp.route('/tags/<int:id>/qrcode', methods=['GET'])
@cache.cached(timeout=3600)  # cache for 1 hour
def get_tag_qrcode(id):
    """ Get QRCode image for Tag """
    img = qrcode.generate('tag:' + str(id))

    return send_file(img, mimetype='image/png')


# ----> TODO <-----

@api_bp.route('/tags/test', methods=['GET'])
def since_tag():
    """ Delete tag with specified id """
    return jsonify(tag_service.since())


# ----> ERRORS <-----

@api_bp.errorhandler(Exception)
def handle_error(e):
    # HTTP error exception
    if isinstance(e, HTTPException):
        return make_response(jsonify(error={
            'code': str(e.code),
            'messages': {
                e.name: e.description
            }
        }), e.code)

    # checks if errors have dict argument
    msgs = e.args[0] if type(e.args[0]) is dict else str(e)

    # default error with bad request code
    return make_response(jsonify(error={
        'messages': msgs
    }), 400)
