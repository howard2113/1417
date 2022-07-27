#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


class construction_(db.Model):
    __tablename__ = 'construction'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(50))
    type = db.Column(db.String(50))
    reason = db.Column(db.String(50))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    

    def __init__(self, location, reason, start_date, end_date):
        self.location = location
        self.reason = reason
        self.start_date = start_date
        self.end_date = end_date

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class constructionSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = construction_
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    location = fields.String(required=True)
    type = fields.String(required=True)
    reason = fields.String(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
