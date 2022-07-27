#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class Reader(db.Model):
    __tablename__ = 'Reader'
    id = db.Column(db.Integer, primary_key=True)
    gid = db.Column(db.Integer)
    Name = db.Column(db.String(20))
    sid = db.Column(db.Integer)
    address = db.Column(db.String(150))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    Attribute = db.Column(db.String(20))
    roadname = db.Column(db.String(20))
    SectionName = db.Column(db.String(200))
    def __init__(self, gid, Name, sid, address, longitude, latitude, Attribute, roadname, SectionName):
        self.gid = gid
        self.Name = Name
        self.sid = sid
        self.address = address
        self.longitude = longitude
        self.latitude = latitude
        self.Attribute = Attribute
        self.roadname = roadname
        self.SectionName = SectionName   

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class ReaderSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Reader
        sqla_session = db.session

        id = fields.Number(dump_only=True)
        gid = fields.Integer(required=True)
        Name = fields.String(required=True)
        sid = fields.Integer(required=False)
        address = fields.String(required=True)
        longitude = fields.Float(required=True)
        latitude = fields.Float(required=True)
        Attribute = fields.String(required=True)
        roadname = fields.String(required=True)
        SectionName = fields.String(required=True)
