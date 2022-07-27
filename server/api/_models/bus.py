#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

'''
    "id(接駁車路線id)" : "string", 
    "name(接駁車路線名稱)" : "string",
    "count(運載次數)" : "int",
    "people(運載人數)" : "int",
'''


class BusDynamic(db.Model):
    __tablename__ = 'bus_dynamic'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), comment='路線名')
    count = db.Column(db.Integer, comment='累計趟數')
    people = db.Column(db.Integer, comment='累計人數')
    full_rate = db.Column(db.Float, comment='滿載率')
    direction = db.Column(db.Integer, comment='去=1 回=2')
    src_time = db.Column(db.DateTime, comment='源資料時間')
    update_time = db.Column(db.DateTime, server_default=db.func.now(), comment='撈取時間')

    def __init__(self, name, count, people, full_rate, direction, src_time):
        self.name = name
        self.count = count
        self.people = people
        self.full_rate = full_rate
        self.direction = direction
        self.src_time = src_time

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class BusDynamicSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = BusDynamic
        sqla_session = db.session

    name = fields.Integer(required=True)
    count = fields.Integer(required=True)
    people = fields.Integer(required=True)
    full_rate = fields.Float(required=True)
    direction = fields.Integer(required=True)
    src_time = fields.DateTime(required=True)
