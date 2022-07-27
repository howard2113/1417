#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class NotifyHistory(db.Model):
    __tablename__ = 'NotifyHistory'

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(20))
    type = db.Column(db.String(10))
    first_error = db.Column(db.String(30))
    address = db.Column(db.String(50))
    update_time = db.Column(db.String(50))

    def __init__(self, device_id, type, first_error, address, update_time):
        self.device_id = device_id
        self.type = type
        self.first_error = first_error
        self.address = address
        self.update_time = update_time

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class NotifyHistorySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = NotifyHistory
        sqla_session = db.session

    device_id = fields.String(required=True)
    type = fields.String(required=True)
    first_error = fields.String(required=True)
    address = fields.String(required=True)
    update_time = fields.String(required=True)

    