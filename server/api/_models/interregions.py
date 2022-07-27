#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class InterRegion(db.Model):
    __tablename__ = 'interRegion'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recTime = db.Column(db.DateTime)
    oReader = db.Column(db.String(20))
    dReader = db.Column(db.String(20))
    category = db.Column(db.Integer)
    count = db.Column(db.Integer)

    def __init__(self, recTime, oReader, dReader, category, count):
        self.recTime = recTime
        self.oReader = oReader
        self.dReader = dReader
        self.category = category
        self.count = count

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class InterRegionSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = InterRegion
        sqla_session = db.session

    id = fields.Number(dump_only=True)    
    recTime = fields.DateTime(required=True,format='%Y-%m-%d %H:%M:%S')
    oReader = fields.String(required=True)
    dReader = fields.String(required=True)
    category = fields.Integer(required=True)
    count = fields.Integer(required=True)

