"""
wiim.api.models

Models classes and schemas for API
using collation utf8mb4_unicode_ci

:copyright: © 2018 by José Almeida.
:license: CC BY-NC 4.0, see LICENSE for more details.
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import mysql
from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


# ----> MODELS <-----

class Site(db.Model):
    """ Site model """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    comment = db.Column(db.String(120), nullable=False)
    # foreign key: one site have many zones
    # zones = db.relationship('Zone', backref='site', lazy='dynamic')

    def __repr__(self):
        return '<Site: {}>'.format(self.name)


class Zone(db.Model):
    """ Zone model """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    comment = db.Column(db.String(120), nullable=False)
    # foreign key: one zone have one site
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)
    site = db.relationship('Site')
    # foreign key: one zone have many processes
    # processes = db.relationship('Process', backref='zone', lazy='dynamic')

    def __repr__(self):
        return '<Zone: {}>'.format(self.name)


process_tags = db.Table(
    # many to many table
    'process_tags',
    db.Column('process_id', db.Integer, db.ForeignKey('process.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)


class Process(db.Model):
    """ Process model """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    comment = db.Column(db.String(120))
    # foreign key: one process have one zone
    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'), nullable=False)
    zone = db.relationship('Zone')

    def __repr__(self):
        return '<Process: {}>'.format(self.name)


class Server(db.Model):
    """ OPCUA server model """

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(64), nullable=False)
    # foreign key: one server have many tags
    # tags = db.relationship('Tag', backref='server', lazy='dynamic')

    def __repr__(self):
        return '<Server: {}>'.format(self.uid)


class Tag(db.Model):
    """ Tags or control variables model """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    alias = db.Column(db.String(64), nullable=False)
    comment = db.Column(db.String(120))
    unit = db.Column(db.String(64))
    icon = db.Column(db.String(255))
    # foreign key: one tag have one server
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)
    server = db.relationship('Server')
    # foreign key: one tag have many records
    # records = db.relationship('Record', backref='tag', lazy='dynamic')

    def __repr__(self):
        return '<Tag: {}>'.format(self.name)


class Record(db.Model):
    """ Record model """
    __table_args__ = {'mysql_engine': 'MyISAM'}  # table engine

    id = db.Column(db.Integer, primary_key=True)
    time_opc = db.Column(mysql.DATETIME(fsp=3), nullable=False)
    time_db = db.Column(mysql.TIMESTAMP(fsp=3), nullable=False)
    value = db.Column(db.String(120), nullable=False)
    quality = db.Column(db.String(64), nullable=False)
    # foreign key: one record have one tag
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)
    tag = db.relationship('Tag')

    def __repr__(self):
        return '<Record: {}>'.format(self.value)


# ----> SCHEMAS <-----

class SiteSchema(ma.ModelSchema):
    """ docstring for SiteSchema """

    class Meta:
        # Fields to expose
        fields = ('name', 'comment')
        model = Site


class ZoneSchema(ma.ModelSchema):
    """ docstring for ZoneSchema """

    class Meta:
        # Fields to expose
        fields = ('name', 'comment', 'site')
        model = Zone

    site = fields.Nested(SiteSchema)


class ProcessSchema(ma.ModelSchema):
    """ docstring for ProcessSchema """

    class Meta:
        # Fields to expose
        fields = ('name', 'comment', 'zone')
        model = Process

    zone = fields.Nested(ZoneSchema)


class ServerSchema(ma.ModelSchema):
    """ docstring for ServerSchema """

    class Meta:
        # Fields to expose
        fields = ('uid',)
        model = Server


class TagSchema(ma.ModelSchema):
    """ docstring for TagSchema """

    class Meta:
        # Fields to expose
        # fields = ('name', 'alias', 'comment', 'unit', 'icon', 'server')
        model = Tag

    server = fields.Nested(ServerSchema)


class RecordSchema(ma.ModelSchema):
    """ docstring for RecordSchema """

    class Meta:
        # Fields to expose
        # fields = ('time_opc', 'time_db', 'value', 'quality', 'tag')
        model = Record

    tag = fields.Nested(TagSchema)

    # Smart hyperlinking
    # _links = ma.Hyperlinks({
    #     'self': ma.URLFor('tag_detail', id='<id>')
    # })
