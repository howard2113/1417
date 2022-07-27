#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class CmsMessage(db.Model):
    __tablename__ = 'cms_messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    size = db.Column(db.String(10), comment='看板尺寸')
    category = db.Column(db.Integer, comment='訊息類別')
    message = db.Column(db.String(12), comment='訊息文字')
    color_array = db.Column(db.ARRAY(db.String(10)), comment='訊息文字顏色')
    message_array = db.Column(db.ARRAY(db.Integer), comment='訊息片語')
    gearing = db.Column(db.ARRAY(db.Integer), comment='連動的訊息id')
    updatetime = db.Column(db.DateTime, comment='更改時間')

    def __init__(self, size, category, message, color_array, message_array, gearing, updatetime):
        self.size = size
        self.category = category
        self.message = message
        self.color_array = color_array
        self.message_array = message_array
        self.gearing = gearing
        self.updatetime = updatetime

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class CmsMessageSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = CmsMessage
        sqla_session = db.session

    id = fields.Integer(required=True)
    size = fields.String(required=True)
    category = fields.Integer(required=True)
    message = fields.String(required=True)
    color_array = fields.List(fields.String(), required=True)
    message_array = fields.List(fields.Integer(), required=True)
    gearing = fields.List(fields.Integer(), required=True)
    updatetime = fields.DateTime(required=True)