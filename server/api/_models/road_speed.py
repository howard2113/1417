#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


class RoadStaticVD(db.Model):
    __tablename__ = 'road_static_vd'
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    start_pos = db.Column(db.String(100))
    end_pos = db.Column(db.String(100))
    src_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, name,  lat, lon, start_pos, end_pos, src_time, update_time):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.src_time = src_time
        self.update_time = update_time

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class SectionVDSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = RoadStaticVD
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    lat = fields.Float(required=True)
    lon = fields.Float(required=True)
    start_pos = fields.Float(required=True)
    end_pos = fields.Float(required=True)
    src_time = fields.DateTime(required=True)
    update_time = fields.DateTime(required=True)



'''
    "id(路段id)" : "string", 
    "name(路段名稱)" : "string",
    "areaname(行政區)" : "string",
    "lat(緯度)" : "float/decimal",
    "lng(經度)" : "float/decimal",
=======================================
    road_id
    road_direction
    o_lat
    o_lon
    d_lat
    d_lon
    freeflowspeed
'''


class SectionGVP(db.Model):
    __tablename__ = 'road_section_gvp'
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    area_name = db.Column(db.String(100))
    direction = db.Column(db.String(50))
    start_pos = db.Column(db.String(100))
    end_pos = db.Column(db.String(100))
    geometry = db.Column(db.Text)
    src_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, name, area_name, direction, start_pos, end_pos, geometry, src_time, update_time):
        self.name = name
        self.area_name = area_name
        self.direction = direction
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.geometry = geometry
        self.src_time = src_time
        self.update_time = update_time

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class SectionGVPSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = SectionGVP
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    area_name = fields.String(required=True)
    direction = fields.String(required=True)
    start_pos = fields.Float(required=True)
    end_pos = fields.Float(required=True)
    geometry = fields.String(required=True)
    src_time = fields.DateTime(required=True)
    update_time = fields.DateTime(required=True)




class RoadDynamicSpeed(db.Model):
    __tablename__ = 'road_dynamic_speed'
    id = db.Column(db.String(50), primary_key=True)
    l_id = db.Column(db.String(50), primary_key=True)
    area_name = db.Column(db.String(100))
    name = db.Column(db.String(100))
    dev = db.Column(db.Integer, comment='vd=0, gvp=1')
    tti = db.Column(db.Float)
    speed = db.Column(db.Float)
    h0 = db.Column(db.Float)
    h1 = db.Column(db.Float)
    h2 = db.Column(db.Float)
    h3 = db.Column(db.Float)
    h4 = db.Column(db.Float)
    h5 = db.Column(db.Float)
    h6 = db.Column(db.Float)
    h7 = db.Column(db.Float)
    h8 = db.Column(db.Float)
    h9 = db.Column(db.Float)
    h10 = db.Column(db.Float)
    h11 = db.Column(db.Float)
    h12 = db.Column(db.Float)
    h13 = db.Column(db.Float)
    h14 = db.Column(db.Float)
    h15 = db.Column(db.Float)
    h16 = db.Column(db.Float)
    h17 = db.Column(db.Float)
    h18 = db.Column(db.Float)
    h19 = db.Column(db.Float)
    h20 = db.Column(db.Float)
    h21 = db.Column(db.Float)
    h22 = db.Column(db.Float)
    h23 = db.Column(db.Float)
    src_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, id, l_id, area_name, name, dev, tti, speed, h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16, h17, h18, h19, h20, h21, h22, h23, src_time):
        self.id = id
        self.l_id = l_id
        self.area_name = area_name
        self.name = name
        self.dev = dev
        self.tti = tti
        self.speed = speed
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


class RoadDynamicSpeedSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = RoadDynamicSpeed
        sqla_session = db.session

    id = fields.String(required=True)
    l_id = fields.String(required=True)
    name = fields.String(required=True)
    dev = fields.String(required=True)
    tti = fields.Float(required=True)
    speed = fields.Float(required=True)
    h0 = fields.Float(required=True)
    h1 = fields.Float(required=True)
    h2 = fields.Float(required=True)
    h3 = fields.Float(required=True)
    h4 = fields.Float(required=True)
    h5 = fields.Float(required=True)
    h6 = fields.Float(required=True)
    h7 = fields.Float(required=True)
    h8 = fields.Float(required=True)
    h9 = fields.Float(required=True)
    h10 = fields.Float(required=True)
    h11 = fields.Float(required=True)
    h12 = fields.Float(required=True)
    h13 = fields.Float(required=True)
    h14 = fields.Float(required=True)
    h15 = fields.Float(required=True)
    h16 = fields.Float(required=True)
    h17 = fields.Float(required=True)
    h18 = fields.Float(required=True)
    h19 = fields.Float(required=True)
    h20 = fields.Float(required=True)
    h21 = fields.Float(required=True)
    h22 = fields.Float(required=True)
    h23 = fields.Float(required=True)
    src_time = fields.DateTime(required=True)
    update_time = fields.DateTime(required=True)


