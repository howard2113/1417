#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class Phrases(db.Model):
    __tablename__ = 'phrases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # cms_messages_id = db.Column(db.Integer, comment='cms_messages對應父id')
    message = db.Column(db.String(12), comment='片語文字')
    color = db.Column(db.ARRAY(db.String(10)), comment='片語文字顏色')
   
    def __init__(self, message, color):
        # self.cms_messages_id = cms_messages_id
        self.message = message
        self.color = color

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class PhrasesSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Phrases
        sqla_session = db.session

    id = fields.Integer(required=True)
    # cms_messages_id = fields.Integer(required=True)
    message = fields.String(required=True)
    color = fields.List(fields.String(), required=True)