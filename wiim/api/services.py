"""
wiim.api.services

Include Models management for API

:copyright: © 2018 by José Almeida.
:license: CC BY-NC 4.0, see LICENSE for more details.
"""

from flask import current_app as app
# application imports
from .models import db


class BaseService():
    """ Base service class

    keyword arguments:
    name -- tuple with (singular, plural) names(required)
    model -- model class (required)
    schema -- marshmallow schema class (required)
    """

    def __init__(self, name, model, schema):
        self.name = name
        self.Model = model
        self.Schema = schema

    def create(self, *args, **kwargs):
        """ Create a new Model """
        item = self.Model(*args, **kwargs)

        # commit to database
        db.session.add(item)
        db.session.commit()

        return {
            'status': 'success',
            'message': self.name[0] + ' was created successfully!'
        }  # created

    def get_all(self, page=1, count=0):
        """ Get all items from Model

        keyword arguments:
        page -- page number (default 1)
        count -- tags per page, use zero for WIIM_COUNT_LIMIT (default 0)
        """
        items_schema = self.Schema(many=True)

        # limit fetch quantity
        if not count or count > app.config['WIIM_COUNT_LIMIT']:
            count = app.config['WIIM_COUNT_LIMIT']

        items = self.Model.query.paginate(page, count).items
        items = items_schema.dump(items).data

        return {self.name[1]: items}

    def get_by_id(self, id):
        """ Get single Item by id

        keyword arguments:
        id -- Item id (required)
        """
        item_schema = self.Schema()

        item = self.Model.query.get(id)
        item = item_schema.dump(item).data

        return item

    def update():
        pass

    def destroy():
        pass
