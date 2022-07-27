#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class CmsStatus(db.Model):
    __tablename__ = 'cms_status'
    id = db.Column(db.String(20), primary_key=True)
    size = db.Column(db.String(10), comment='看板尺寸')
    location = db.Column(db.String(200), comment='道路名稱')
    lon = db.Column(db.Float, comment='經度')
    lat = db.Column(db.Float, comment='緯度')
    messgae_state = db.Column(db.Integer, comment='訊息狀態')
    cycle_state = db.Column(db.Integer, comment='循環狀態')
    updatetime = db.Column(db.DateTime, comment='更改時間')

    def __init__(self, id, size, location, lon, lat, messgae_state, cycle_state, cycle_message, updatetime):
        self.id = id
        self.size = size
        self.location = location
        self.lon = lon
        self.lat = lat
        self.messgae_state = messgae_state
        self.cycle_state = cycle_state
        self.updatetime = updatetime

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class CmsStatusSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = CmsStatus
        sqla_session = db.session

    id = fields.String(required=True)
    size = fields.String(required=True)
    location = fields.String(required=True)
    lon = fields.Float(required=True)
    lat = fields.Float(required=True)
    messgae_state = fields.Integer(required=True)
    cycle_state = fields.Integer(required=True)
    updatetime = fields.DateTime(required=True)