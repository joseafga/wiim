"""
wiim.api.controllers

Include routes and database functions for API

:copyright: © 2018 by José Almeida.
:license: CC BY-NC 4.0, see LICENSE for more details.
"""

from flask import Blueprint, make_response, abort, request, jsonify
from werkzeug.exceptions import HTTPException
# application imports
from wiim.api.models import db, Process, Tag, Record, TagSchema, RecordSchema

# Define the blueprint: 'api', set its url prefix: app.url/api
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


# ----> PROCESSES <-----

@api_bp.route('/processes', methods=['GET'])
def get_processes():
    ''' Return all processes '''
    # return jsonify({'tags': tags})


@api_bp.route('/processes/<int:id>', methods=['GET'])
def get_process(id):
    ''' Return process with specified id '''
    # tag = [tag for tag in tags if tag['id'] == id]
    # if len(tag) == 0:
    #     abort(404)  # not found error

    # return jsonify({'tag': tag[0]})


# ----> TAGS <-----

@api_bp.route('/tags', methods=['GET'])
def get_tags(page=1):
    ''' Return all tags '''
    # return jsonify({'tags': Tag.query.all})
    tags_schema = TagSchema(many=True)

    tags = Tag.query.paginate(1, 100).items
    tags = tags_schema.dump(tags).data

    return jsonify({'tags': tags})


@api_bp.route('/tags', methods=['POST'])
def create_tag():
    ''' Create a new tag '''
    # checks request exists and have title attribute
    if not request.json or not {'name', 'alias', 'server_id'}.issubset(set(request.json)):
        abort(400)  # bad request error

    # create Tag object
    tag = Tag(
        name=request.json['name'],
        alias=request.json['alias'],
        server_id=request.json['server_id']
    )
    tag.comment = request.json.get('comment', "")
    tag.unit = request.json.get('unit', "")
    tag.icon = request.json.get('icon', "")
    # commit to database
    db.session.add(tag)
    db.session.commit()

    # get schema and dump
    # tag_schema = TagSchema()
    # tag = tag_schema.dump(tag).data
    # return jsonify({'tag': tag}), 201  # created

    return jsonify(success={
        'message': 'Tag was created successfully!'
    }), 201  # created


@api_bp.route('/tags/<int:id>', methods=['GET'])
def get_tag(id):
    ''' Return tag with specified id '''
    # tag = [tag for tag in tags if tag['id'] == id]
    # if len(tag) == 0:
    #     abort(404)  # not found error

    # return jsonify({'tag': tag[0]})


# ----> RECORDS <-----

@api_bp.route('/records', methods=['GET'])
def get_records(page=1):
    ''' Return all records '''
    # return jsonify({'records': Record.query.all})
    records_schema = RecordSchema(many=True)

    records = Record.query.paginate(1, 100).items
    records = records_schema.dump(records).data

    return jsonify({'records': records})


@api_bp.route('/records', methods=['POST'])
def create_record():
    ''' Create a new tag '''
    # checks request exists and have title attribute
    if not request.json or not {'time_opc', 'value', 'tag_id'}.issubset(set(request.json)):
        abort(400)  # bad request error

    # create Record object
    record = Record(
        time_opc=request.json['time_opc'],
        value=request.json['value'],
        tag_id=request.json['tag_id']
    )
    record.quality = request.json.get('quality', 'Unknown')
    # commit to database
    db.session.add(record)
    db.session.commit()

    return jsonify(success={
        'message': 'Record was created successfully!'
    }), 201  # created


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
