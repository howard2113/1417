#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class PathStartEnd(db.Model):
    __tablename__ = 'pathStartEnd'
    id = db.Column(db.Integer, primary_key=True)
    recTime = db.Column(db.DateTime, index=True)
    oReader = db.Column(db.String(20))
    dReader = db.Column(db.String(20))
    readerPath = db.Column(db.String(200))
    count = db.Column(db.Integer)
    category = db.Column(db.Integer)


    def __init__(self, recTime, oReader, dReader, readerPath, count, category):
        self.recTime = recTime
        self.oReader = oReader
        self.dReader = dReader
        self.readerPath = readerPath
        self.count = count 
        self.category = category

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class PathStartEndSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = PathStartEnd
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    recTime = fields.DateTime(required=True,format='%Y-%m-%d %H:%M:%S')
    oReader = fields.String(required=True)
    dReader = fields.String(required=True)
    readerPath = fields.String(required=True)
    count = fields.Integer(required=True)
