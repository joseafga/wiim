"""
wiim.api.services

Include Models management for API

:copyright: © 2018 by José Almeida.
:license: CC BY-NC 4.0, see LICENSE for more details.
"""

from flask import abort, current_app as app
# application imports
from .models import *


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
        """ Create a new entry """
        item = self.Model(*args, **kwargs)

        # commit to database
        db.session.add(item)
        db.session.commit()

        return dict(success={
            'message': self.name[0] + ' was created successfully!'
        })  # created

    def get_all(self, page=1, count=0, filters=None):
        """ Get all items from specified relation

        keyword arguments:
        page -- page number (default 1)
        count -- tags per page, use zero for WIIM_COUNT_LIMIT (default 0)
        filters -- filters for sqlalchemy (default None)
        """
        items_schema = self.Schema(many=True)

        # limit fetch quantity
        if not count or count > app.config['WIIM_COUNT_LIMIT']:
            count = app.config['WIIM_COUNT_LIMIT']

        query = self.Model.query

        # apply filters or not
        if filters is not None:
            # for attr, value in filters.iteritems():
            #     query = query.filter(getattr(self.Model, attr) == value)
            query = query.filter_by(**filters)  # smart filter by kwargs

        items = query.paginate(page, count).items
        items = items_schema.dump(items).data

        return {self.name[1]: items}

    def get_by_id(self, id):
        """ Get single item by id

        keyword arguments:
        id -- Item id (required)
        """
        item_schema = self.Schema()

        item = self.Model.query.get(id)
        item = item_schema.dump(item).data

        return {self.name[0]: item}

    def update():
        pass

    def destroy_by_id(self, id):
        """ Remove a entry by id

        keyword arguments:
        id -- Item id (required)
        """
        item = self.Model.query.get(id)

        # commit to database
        db.session.delete(item)
        db.session.commit()

        return dict(success={
            'message': self.name[0] + ' was destroyed successfully!'
        })  # created


class TagService(BaseService):
    """ Add since methods to Base"""

    def __init__(self, *args, **kwargs):
        super(TagService, self).__init__(*args, **kwargs)

    def create(self, *args, **kwargs):
        """ Create a new Model """
        # get processes field
        if 'processes' in kwargs:
            processes = kwargs['processes']
            del kwargs['processes']
        else:
            # raise error
            raise ValueError('Require Processes of the Tag')

        tag = Tag(*args, **kwargs)

        for process_id in processes:
            process = Process.query.get(process_id)
            # set tag to related process
            process.tags.append(tag)
            db.session.add(process)

        # commit to database
        db.session.add(tag)
        db.session.commit()

        return dict(success={
            'message': self.name[0] + ' was created successfully!'
        })  # created

    def get_by_process(self, id, page=1, count=0, filters=None):
        """ Get all tags from specified process

        keyword arguments:
        page -- page number (default 1)
        count -- tags per page, use zero for WIIM_COUNT_LIMIT (default 0)
        filters -- filters for sqlalchemy (default None)
        """
        items_schema = TagSchema(many=True)

        # limit fetch quantity
        if not count or count > app.config['WIIM_COUNT_LIMIT']:
            count = app.config['WIIM_COUNT_LIMIT']

        # query = Process.query.join(Process.tags)
        # query = Process.query.filter(Process.tags.any(**filters)).all()
        query = Tag.query.filter(Tag.process.any(Process.id == id))

        # apply filters or not
        if filters is not None:
            # for attr, value in filters.iteritems():
            #     query = query.filter(getattr(self.Model, attr) == value)
            query = query.filter_by(**filters)  # smart filter by kwargs

        items = query.paginate(page, count).items
        items = items_schema.dump(items).data

        return {self.name[1]: items}

    def since(self):
        # session = db.session
        time = 0

        tag_records_schema = TagRecordsSchema(many=True)
        query = Tag.query.filter(Tag.records.any(Record.time_db > time))
        items = query.all()
        # tag_records = session.query(Tag, Record).filter(Tag.id == Record.tag_id).all()
        # tag_records = Tag.query.all()
        # tags = []
        # for x, y in tag_records:
        #     x.record = y
        #     tags.append(x)

        items = tag_records_schema.dump(items)
        # data = tag_records_schema.dump(tag_records).data
        # print(tag_records)
        # result = tag_records_schema.dump(tag_records).data

        return {self.name[1]: items}

        # return item


# Initialize services
site_service = BaseService(('Site', 'Sites'), Site, SiteSchema)
zone_service = BaseService(('Zone', 'Zones'), Zone, ZoneSchema)
process_service = BaseService(('Process', 'Processes'), Process, ProcessSchema)
server_service = BaseService(('Server', 'Servers'), Server, ServerSchema)
tag_service = TagService(('Tag', 'Tags'), Tag, TagSchema)
record_service = BaseService(('Record', 'Records'), Record, RecordSchema)
