#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class InterRegionMonthAttribute(db.Model):
    __tablename__ = 'interRegionMonthAttribute'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recTime = db.Column(db.DateTime)
    category = db.Column(db.Integer)
    isWorkday = db.Column(db.Integer)
    oAttribute = db.Column(db.Integer)
    count = db.Column(db.Integer)

    def __init__(self, recTime, category, isWorkday, oAttribute,count):
        self.recTime = recTime
        self.category = category
        self.isWorkday = isWorkday
        self.oAttribute = oAttribute
        self.count = count

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class InterRegionMonthAttributeSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = InterRegionMonthAttribute
        sqla_session = db.session

    id = fields.Number(dump_only=True)    
    recTime = fields.DateTime(required=True,format='%Y-%m-%d %H:%M:%S')
    category = fields.Integer(required=True)
    isWorkday = fields.Integer(required=True)
    oAttribute = fields.Integer(required=True)
    count = fields.Integer(required=True)

