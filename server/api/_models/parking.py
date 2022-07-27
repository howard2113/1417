#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


# [{
#   "name(停車場名稱)" : "string",
#   "areaname(行政區域)" : "string",
#   "volumn(總格位)" : "int",
#   "lat(緯度)" : "float/decimal",
#   "lng(經度)" : "float/decimal",
# }]

class Static(db.Model):
    __tablename__ = 'parking_outer_static'
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50))
    v_type = db.Column(db.Integer, comment='汽車=1，機車=2')
    areaname = db.Column(db.String(10))
    volumn = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    fare_description = db.Column(db.String(500))
    src_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, name, v_type, areaname, volumn, lat, lng, fare_description, src_time):
        self.name = name
        self.v_type = v_type
        self.areaname = areaname
        self.volumn = volumn
        self.lat = lat
        self.lng = lng
        self.fare_description = fare_description
        self.src_time = src_time

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class StaticSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Static
        sqla_session = db.session

    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    v_type = fields.Integer(required=True)
    areaname = fields.String(required=True)
    volumn = fields.Integer(required=True)
    lat = fields.Float(required=True)
    lng = fields.Float(required=True)
    fare_description = fields.String(required=True)
    src_time = fields.DateTime(required=True)
    update_time = fields.DateTime(required=True)


class ParkingOuterLeftSpaceRealTime(db.Model):
    __tablename__ = 'parking_outer_left_space_dynamic'
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100))
    v_type = db.Column(db.Integer, comment='汽車=1，機車=2')
    volumn = db.Column(db.Integer)
    leftspace = db.Column(db.Integer)
    h0 = db.Column(db.Integer)
    h1 = db.Column(db.Integer)
    h2 = db.Column(db.Integer)
    h3 = db.Column(db.Integer)
    h4 = db.Column(db.Integer)
    h5 = db.Column(db.Integer)
    h6 = db.Column(db.Integer)
    h7 = db.Column(db.Integer)
    h8 = db.Column(db.Integer)
    h9 = db.Column(db.Integer)
    h10 = db.Column(db.Integer)
    h11 = db.Column(db.Integer)
    h12 = db.Column(db.Integer)
    h13 = db.Column(db.Integer)
    h14 = db.Column(db.Integer)
    h15 = db.Column(db.Integer)
    h16 = db.Column(db.Integer)
    h17 = db.Column(db.Integer)
    h18 = db.Column(db.Integer)
    h19 = db.Column(db.Integer)
    h20 = db.Column(db.Integer)
    h21 = db.Column(db.Integer)
    h22 = db.Column(db.Integer)
    h23 = db.Column(db.Integer)
    src_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, id, name, v_type, volumn, leftspace, h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16, h17, h18, h19, h20, h21, h22, h23, src_time):
        self.id = id
        self.name = name
        self.v_type = v_type
        self.leftspace = leftspace
        self.volumn = volumn
        self.h0 = h0
        self.h1 = h1
        self.h2 = h2
        self.h3 = h3
        self.h4 = h4
        self.h5 = h5
        self.h6 = h6
        self.h7 = h7
        self.h8 = h8
        self.h9 = h9
        self.h10 = h10
        self.h11 = h11
        self.h12 = h12
        self.h13 = h13
        self.h14 = h14
        self.h15 = h15
        self.h16 = h16
        self.h17 = h17
        self.h18 = h18
        self.h19 = h19
        self.h20 = h20
        self.h21 = h21
        self.h22 = h22
        self.h23 = h23
        self.src_time = src_time

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class ParkingOuterLeftSpaceRealTimeSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ParkingOuterLeftSpaceRealTime
        sqla_session = db.session

    id = fields.String(required=True)
    name = fields.String(required=True)
    v_type = fields.Integer(required=True)
    volumn = fields.Integer(required=True)
    leftspace = fields.Integer(required=True)
    h0 = fields.Integer(required=True)
    h1 = fields.Integer(required=True)
    h2 = fields.Integer(required=True)
    h3 = fields.Integer(required=True)
    h4 = fields.Integer(required=True)
    h5 = fields.Integer(required=True)
    h6 = fields.Integer(required=True)
    h7 = fields.Integer(required=True)
    h8 = fields.Integer(required=True)
    h9 = fields.Integer(required=True)
    h10 = fields.Integer(required=True)
    h11 = fields.Integer(required=True)
    h12 = fields.Integer(required=True)
    h13 = fields.Integer(required=True)
    h14 = fields.Integer(required=True)
    h15 = fields.Integer(required=True)
    h16 = fields.Integer(required=True)
    h17 = fields.Integer(required=True)
    h18 = fields.Integer(required=True)
    h19 = fields.Integer(required=True)
    h20 = fields.Integer(required=True)
    h21 = fields.Integer(required=True)
    h22 = fields.Integer(required=True)
    h23 = fields.Integer(required=True)
    src_time = fields.DateTime(required=True)
    update_time = fields.DateTime(required=True)
#
#
# class ParkingOuterLeftSpace24hMean(db.Model):
#     __tablename__ = 'parking_outer_left_space_24h_mean'
#     id = db.Column(db.String(10), primary_key=True)
#     name = db.Column(db.String(100))
#     volumn = db.Column(db.Integer)
#     h0 = db.Column(db.Integer)
#     h1 = db.Column(db.Integer)
#     h2 = db.Column(db.Integer)
#     h3 = db.Column(db.Integer)
#     h4 = db.Column(db.Integer)
#     h5 = db.Column(db.Integer)
#     h6 = db.Column(db.Integer)
#     h7 = db.Column(db.Integer)
#     h8 = db.Column(db.Integer)
#     h9 = db.Column(db.Integer)
#     h10 = db.Column(db.Integer)
#     h11 = db.Column(db.Integer)
#     h12 = db.Column(db.Integer)
#     h13 = db.Column(db.Integer)
#     h14 = db.Column(db.Integer)
#     h15 = db.Column(db.Integer)
#     h16 = db.Column(db.Integer)
#     h17 = db.Column(db.Integer)
#     h18 = db.Column(db.Integer)
#     h19 = db.Column(db.Integer)
#     h20 = db.Column(db.Integer)
#     h21 = db.Column(db.Integer)
#     h22 = db.Column(db.Integer)
#     h23 = db.Column(db.Integer)
#     collect_count = db.Column(db.Integer)
#     date = db.Column(db.Date, primary_key=True)
#     src_time = db.Column(db.DateTime)
#     update_time = db.Column(db.DateTime, server_default=db.func.now())
#
#     def __init__(self, id, name, volumn, h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16, h17, h18, h19, h20, h21, h22, h23, collect_count, date, src_time):
#         self.id = id
#         self.name = name
#         self.volumn = volumn
#         self.h0 = h0
#         self.h1 = h1
#         self.h2 = h2
#         self.h3 = h3
#         self.h4 = h4
#         self.h5 = h5
#         self.h6 = h6
#         self.h7 = h7
#         self.h8 = h8
#         self.h9 = h9
#         self.h10 = h10
#         self.h11 = h11
#         self.h12 = h12
#         self.h13 = h13
#         self.h14 = h14
#         self.h15 = h15
#         self.h16 = h16
#         self.h17 = h17
#         self.h18 = h18
#         self.h19 = h19
#         self.h20 = h20
#         self.h21 = h21
#         self.h22 = h22
#         self.h23 = h23
#         self.collect_count = collect_count
#         self.date = date
#         self.src_time = src_time
#
#     def create(self):
#         db.session.add(self)
#         db.session.commit()
#         return self
#
#
# class ParkingOuterLeftSpace24hMeanSchema(ModelSchema):
#     class Meta(ModelSchema.Meta):
#         model = ParkingOuterLeftSpace24hMean
#         sqla_session = db.session
#
#     id = fields.String(required=True)
#     name = fields.String(required=True)
#     volumn = fields.Integer(required=True)
#     h0 = fields.Integer(required=True)
#     h1 = fields.Integer(required=True)
#     h2 = fields.Integer(required=True)
#     h3 = fields.Integer(required=True)
#     h4 = fields.Integer(required=True)
#     h5 = fields.Integer(required=True)
#     h6 = fields.Integer(required=True)
#     h7 = fields.Integer(required=True)
#     h8 = fields.Integer(required=True)
#     h9 = fields.Integer(required=True)
#     h10 = fields.Integer(required=True)
#     h11 = fields.Integer(required=True)
#     h12 = fields.Integer(required=True)
#     h13 = fields.Integer(required=True)
#     h14 = fields.Integer(required=True)
#     h15 = fields.Integer(required=True)
#     h16 = fields.Integer(required=True)
#     h17 = fields.Integer(required=True)
#     h18 = fields.Integer(required=True)
#     h19 = fields.Integer(required=True)
#     h20 = fields.Integer(required=True)
#     h21 = fields.Integer(required=True)
#     h22 = fields.Integer(required=True)
#     h23 = fields.Integer(required=True)
#     collect_count = fields.Integer(required=True)
#     date = fields.Date(required=True)
#     src_time = fields.DateTime(required=True)
#     update_time = fields.DateTime(required=True)
