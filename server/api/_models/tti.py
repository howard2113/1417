#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class HourVolume(db.Model):
    __tablename__ = 'hourVolume'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recTime = db.Column(db.DateTime)
    roadId = db.Column(db.String(20))
    travelTime = db.Column(db.Integer)
    count = db.Column(db.Integer)
    pairRate = db.Column(db.Float)
    speed = db.Column(db.Float)
    def __init__(self, recTime, roadId, travelTime, count, pairRate, speed):
        self.recTime = recTime
        self.roadId = roadId
        self.travelTime = travelTime
        self.count = count
        self.pairRate = pairRate
        self.speed = speed

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class HourVolumeSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = HourVolume
        sqla_session = db.session

    id = fields.Number(dump_only=True)    
    recTime = fields.DateTime(required=True,format='%Y-%m-%d %H:%M:%S')
    roadId  = fields.String(required=True)
    travelTime = fields.Integer(required=True)
    count = fields.Integer(required=True)
    pairRate = fields.Float(required =True)
    speed = fields.Float(required =True)


class FreeFlow(db.Model):
    __tablename__ = 'freeFlow'
    
    id = db.Column(db.Integer, primary_key=True)
    recTime = db.Column(db.DateTime)
    roadId = db.Column(db.String(20))
    speed = db.Column(db.Float)
    def __init__(self, recTime, roadId, speed):
        self.recTime = recTime
        self.roadId = roadId
        self.speed = speed

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class FreeFlowSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = FreeFlow
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    recTime = fields.DateTime(required=True,format='%Y-%m-%d %H:%M:%S')
    roadId = fields.String(required=True)
    speed = fields.Float(required=True)
