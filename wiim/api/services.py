"""
wiim.api.services

Include Models management for API

:copyright: © 2018 by José Almeida.
:license: CC BY-NC 4.0, see LICENSE for more details.
"""

from flask import current_app as app
# application imports
from wiim.api.models import *


class SiteService():
    """ Handle API for Sites """
    @staticmethod
    def create(name, comment=""):
        """ Create a Site

        keyword arguments:
        name -- site name (required)
        comment -- site comment or description (default "")
        """
        site = Site(
            name=name,
            comment=comment
        )

        # commit to database
        db.session.add(site)
        db.session.commit()

        return {
            'status': 'success',
            'message': 'Site was created successfully!'
        }  # created

    @staticmethod
    def get_all(page=1, count=0):
        """ Get all Sites

        keyword arguments:
        page -- page number (default 1)
        count -- tags per page, use zero for WIIM_COUNT_LIMIT (default 0)
        """
        sites_schema = SiteSchema(many=True)

        # limit fetch quantity
        if not count or count > app.config['WIIM_COUNT_LIMIT']:
            count = app.config['WIIM_COUNT_LIMIT']

        sites = Site.query.paginate(page, count).items
        sites = sites_schema.dump(sites).data

        return {'Sites': sites}

    @staticmethod
    def get_by_id(id):
        """ Get single Site

        keyword arguments:
        id -- Site id (required)
        """
        site_schema = SiteSchema()

        site = Site.query.get(id)
        site = site_schema.dump(site).data

        return site

    @staticmethod
    def update():
        pass

    @staticmethod
    def destroy():
        pass


class ZoneService():
    """ Handle API for Zones """
    @staticmethod
    def create(name, site_id, comment=""):
        """ Create a Zone

        keyword arguments:
        name -- zone name (required)
        site_id -- zone zone id (required)
        comment -- zone comment or description (default "")
        """
        zone = Zone(
            name=name,
            site_id=site_id,
            comment=comment
        )

        # commit to database
        db.session.add(zone)
        db.session.commit()

        return {
            'status': 'success',
            'message': 'Zone was created successfully!'
        }  # created

    @staticmethod
    def get_all(page=1, count=0):
        """ Get all Zones

        keyword arguments:
        page -- page number (default 1)
        count -- tags per page, use zero for WIIM_COUNT_LIMIT (default 0)
        """
        zones_schema = ZoneSchema(many=True)

        # limit fetch quantity
        if not count or count > app.config['WIIM_COUNT_LIMIT']:
            count = app.config['WIIM_COUNT_LIMIT']

        zones = Zone.query.paginate(page, count).items
        zones = zones_schema.dump(zones).data

        return {'Zones': zones}

    @staticmethod
    def get_by_id(id):
        """ Get single Zone

        keyword arguments:
        id -- Zone id (required)
        """
        zone_schema = ZoneSchema()

        zone = Zone.query.get(id)
        zone = zone_schema.dump(zone).data

        return zone

    @staticmethod
    def update():
        pass

    @staticmethod
    def destroy():
        pass


class ProcessService():
    """ Handle API for processes """
    @staticmethod
    def create(name, zone_id, comment=""):
        """ Create a Process

        keyword arguments:
        name -- process name (required)
        zone_id -- process zone id (required)
        comment -- process comment or description (default "")
        """
        process = Process(
            name=name,
            zone_id=zone_id,
            comment=comment
        )

        # commit to database
        db.session.add(process)
        db.session.commit()

        return {
            'status': 'success',
            'message': 'Process was created successfully!'
        }  # created

    @staticmethod
    def get_all(page=1, count=0):
        """ Get all Processes

        keyword arguments:
        page -- page number (default 1)
        count -- tags per page, use zero for WIIM_COUNT_LIMIT (default 0)
        """
        processes_schema = ProcessSchema(many=True)

        # limit fetch quantity
        if not count or count > app.config['WIIM_COUNT_LIMIT']:
            count = app.config['WIIM_COUNT_LIMIT']

        processes = Process.query.paginate(page, count).items
        processes = processes_schema.dump(processes).data

        return {'Processes': processes}

    @staticmethod
    def get_by_id(id):
        """ Get single Process

        keyword arguments:
        id -- Process id (required)
        """
        process_schema = ProcessSchema()

        process = Process.query.get(id)
        process = process_schema.dump(process).data

        return process

    @staticmethod
    def update():
        pass

    @staticmethod
    def destroy():
        pass


class ServerService():
    """ Handle API for Servers """
    @staticmethod
    def create(uid):
        """ Create a Server

        keyword arguments:
        uid -- server uid (required)
        """
        server = Server(uid=uid)

        # commit to database
        db.session.add(server)
        db.session.commit()

        return {
            'status': 'success',
            'message': 'Server was created successfully!'
        }  # created

    @staticmethod
    def get_all(page=1, count=0):
        """ Get all Servers

        keyword arguments:
        page -- page number (default 1)
        count -- tags per page, use zero for WIIM_COUNT_LIMIT (default 0)
        """
        servers_schema = ServerSchema(many=True)

        # limit fetch quantity
        if not count or count > app.config['WIIM_COUNT_LIMIT']:
            count = app.config['WIIM_COUNT_LIMIT']

        servers = Server.query.paginate(page, count).items
        servers = servers_schema.dump(servers).data

        return {'Servers': servers}

    @staticmethod
    def get_by_id(id):
        """ Get single Server

        keyword arguments:
        id -- Server id (required)
        """
        server_schema = ServerSchema()

        server = Process.query.get(id)
        server = server_schema.dump(server).data

        return server

    @staticmethod
    def update():
        pass

    @staticmethod
    def destroy():
        pass


class TagService():
    """ Handle API for tags """
    @staticmethod
    def create(name, alias, server_id, comment="", unit="", icon=""):
        """ Create a Tag

        keyword arguments:
        name -- tag name (required)
        alias -- tag alias for easy identification (required)
        server_id -- tag server id (required)
        comment -- tag comment or description (default "")
        unit -- tag unit measure (default "")
        icon -- tag icon (default "")
        """
        tag = Tag(
            name=name,
            alias=alias,
            comment=comment,
            unit=unit,
            icon=icon,
            server_id=server_id
        )

        # commit to database
        db.session.add(tag)
        db.session.commit()

        return {
            'status': 'success',
            'message': 'Tag was created successfully!'
        }  # created

    @staticmethod
    def get_all(page=1, count=0):
        """ Get all Tags

        keyword arguments:
        page -- page number (default 1)
        count -- tags per page, use zero for WIIM_COUNT_LIMIT (default 0)
        """
        tags_schema = TagSchema(many=True)

        # limit fetch quantity
        if not count or count > app.config['WIIM_COUNT_LIMIT']:
            count = app.config['WIIM_COUNT_LIMIT']

        tags = Tag.query.paginate(page, count).items
        tags = tags_schema.dump(tags).data

        return {'tags': tags}

    @staticmethod
    def get_by_id(id):
        """ Get single Tag

        keyword arguments:
        id -- Tag id (required)
        """
        tag_schema = TagSchema()

        tag = Tag.query.get(id)
        tag = tag_schema.dump(tag).data

        return tag

    @staticmethod
    def update():
        pass

    @staticmethod
    def destroy():
        pass


class RecordService():
    """ Handle API for tags """
    @staticmethod
    def create(time_opc, value, tag_id, quality="Unknown"):
        """ Create a Record

        keyword arguments:
        time_opc -- time passed by opcua (required)
        value -- opcua variable value (required)
        tag_id -- id of the corresponding tag (required)
        quality -- opcua signal quality (default "Unknown")
        """
        record = Record(
            time_opc=time_opc,
            value=value,
            quality=quality,
            tag_id=tag_id
        )

        # commit to database
        db.session.add(record)
        db.session.commit()

        return {
            'status': 'success',
            'message': 'Record was created successfully!'
        }  # created

    @staticmethod
    def get_all(page=1, count=0):
        """ Get all Tags

        keyword arguments:
        page -- page number (default 1)
        count -- tags per page, use zero for WIIM_COUNT_LIMIT (default 0)
        """
        records_schema = RecordSchema(many=True)

        # limit fetch quantity
        if not count or count > app.config['WIIM_COUNT_LIMIT']:
            count = app.config['WIIM_COUNT_LIMIT']

        records = Record.query.paginate(page, count).items
        records = records_schema.dump(records).data

        return {'records': records}

    @staticmethod
    def get_by_id(id):
        """ Get single Record

        keyword arguments:
        id -- Record id (required)
        """
        record_schema = RecordSchema()

        record = Record.query.get(id)
        record = record_schema.dump(record).data

        return record

    @staticmethod
    def update():
        pass

    @staticmethod
    def destroy():
        pass
