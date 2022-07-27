#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class Holiday(db.Model):
    __tablename__ = 'Holiday'
    # id = db.Column(db.Integer, primary_key=True)
    Date_datetime = db.Column(db.DateTime, primary_key=True)
    Date_nvarchar = db.Column(db.String(10))
    isHoliday = db.Column(db.Integer)
    isWorkday = db.Column(db.Integer)
    isWeekend = db.Column(db.Integer)
    isNational = db.Column(db.Integer)
    isOther = db.Column(db.Integer)
    isMakup = db.Column(db.Integer)
    weekNo = db.Column(db.Integer)

    def __init__(self, Date_datetime, Date_nvarchar, isHoliday, isWorkday, isWeekend, isNational, isOther, isMakup, weekNo):
        self.Date_datetime = Date_datetime
        self.Date_nvarchar = Date_nvarchar
        self.isHoliday = isHoliday
        self.isWorkday = isWorkday
        self.isWeekend = isWeekend
        self.isNational = isNational
        self.isOther = isOther
        self.isMakup = isMakup
        self.weekNo = weekNo 

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class HolidaySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Holiday
        sqla_session = db.session

    Date_datetime = fields.DateTime(required=True,format='%Y-%m-%d %H:%M:%S')
    Date_nvarchar = fields.String(required=True)
    isHoliday = fields.Integer(required=True)
    isWorkday = fields.Integer(required=True)
    isWeekend = fields.Integer(required=True)
    isNational = fields.Integer(required=True)
    isOther = fields.Integer(required=True)
    isMakup = fields.Integer(required=True)
    weekNo = fields.Integer(required=True)
