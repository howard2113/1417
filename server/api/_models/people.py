#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


class SubGridCount(db.Model):
    __tablename__ = 'sub_grid_count'
    name = db.Column(db.String(200), primary_key=True)
    count = db.Column(db.Integer)
    src_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, name, count, src_time):
        self.name = name
        self.count = count
        self.src_time = src_time

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class SubGridCountSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = SubGridCount
        sqla_session = db.session

    name = fields.String(required=True)
    count = fields.Integer(required=True)
    src_time = fields.DateTime(required=True)
# ====================================================================================================================

class MrtCount(db.Model):
    __tablename__ = 'mrt_count'
    train_type = db.Column(db.String(200))
    station_name = db.Column(db.String(200), primary_key=True)
    transaction_date = db.Column(db.DateTime, primary_key=True)
    enter = db.Column(db.Integer)
    exit = db.Column(db.Integer)
    enter_count = db.Column(db.Integer)
    exit_count = db.Column(db.Integer)
    enter_rank = db.Column(db.Integer)
    exit_rank = db.Column(db.Integer)
    src_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, train_type, station_name, transaction_date, enter, exit, enter_count, exit_count, enter_rank, exit_rank, src_time):
        self.train_type = train_type
        self.station_name = station_name
        self.transaction_date = transaction_date
        self.enter = enter
        self.exit = exit
        self.enter_count = enter_count
        self.exit_count = exit_count
        self.enter_rank = enter_rank
        self.exit_rank = exit_rank
        self.src_time = src_time

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class MrtCountSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = MrtCount
        sqla_session = db.session

    train_type = fields.String(required=True)
    station_name = fields.String(required=True)
    transaction_date = fields.DateTime(required=True)
    enter = fields.Integer(required=True)
    exit = fields.Integer(required=True)
    enter_count = fields.Integer(required=True)
    exit_count = fields.Integer(required=True)
    enter_rank = fields.Integer(required=True)
    exit_rank = fields.Integer(required=True)
    src_time = fields.DateTime(required=True)
# ====================================================================================================================

class CvpRtGridData(db.Model):
    __tablename__ = 'cvp_rt_grid_data'
    gid = db.Column(db.String(100), primary_key=True)
    population = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    src_time = db.Column(db.DateTime, primary_key=True)
    update_time = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, gid, population, lat, lon, src_time):
        self.gid = gid
        self.population = population
        self.lat = lat
        self.lon = lon
        self.src_time = src_time


    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class CvpRtGridDataSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = CvpRtGridData
        sqla_session = db.session

    gid = fields.String(required=True)
    population = fields.Integer(required=True)
    lat = fields.Float(required=True)
    lon = fields.Float(required=True)
    src_time = fields.DateTime(required=True)
    update_time = fields.DateTime(required=True)
# ====================================================================================================================

class CvpTwrtData(db.Model):
    __tablename__ = 'cvp_twrt_data'
    name = db.Column(db.String(100), primary_key=True, comment='????????????')
    north = db.Column(db.Integer, comment='????????????')
    south = db.Column(db.Integer, comment='????????????')
    west = db.Column(db.Integer, comment='????????????')
    east = db.Column(db.Integer, comment='????????????')
    north_east = db.Column(db.Integer, comment='???????????????')
    north_west = db.Column(db.Integer, comment='???????????????')
    south_east = db.Column(db.Integer, comment='???????????????')
    south_west = db.Column(db.Integer, comment='???????????????')
    north_percent = db.Column(db.Float, comment='?????????????????????')
    south_percent = db.Column(db.Float, comment='?????????????????????')
    west_percent = db.Column(db.Float, comment='?????????????????????')
    east_percent = db.Column(db.Float, comment='?????????????????????')
    north_east_percent = db.Column(db.Float, comment='????????????????????????')
    north_west_percent = db.Column(db.Float, comment='????????????????????????')
    south_east_percent = db.Column(db.Float, comment='????????????????????????')
    south_west_percent = db.Column(db.Float, comment='????????????????????????')
    src_time = db.Column(db.DateTime, comment='?????????????????????')
    update_time = db.Column(db.DateTime, server_default=db.func.now(), primary_key=True, comment='????????????')

    def __init__(self, name, north, south, west, east, north_east, north_west, south_east, south_west, north_percent, south_percent, west_percent, east_percent,
                 north_east_percent, north_west_percent, south_east_percent, south_west_percent, src_time):
        self.name = name
        self.north = north
        self.south = south
        self.west = west
        self.east = east
        self.north_east = north_east
        self.north_west = north_west
        self.south_east = south_east
        self.south_west = south_west
        self.north_percent = north_percent
        self.south_percent = south_percent
        self.west_percent = west_percent
        self.east_percent = east_percent
        self.north_east_percent = north_east_percent
        self.north_west_percent = north_west_percent
        self.south_east_percent = south_east_percent
        self.south_west_percent = south_west_percent
        self.src_time = src_time

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class CvpTwrtDataSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = CvpTwrtData
        sqla_session = db.session

    name = fields.String(required=True)
    north = fields.Integer(required=True)
    south = fields.Integer(required=True)
    west = fields.Integer(required=True)
    east = fields.Integer(required=True)
    north_east = fields.Integer(required=True)
    north_west = fields.Integer(required=True)
    south_east = fields.Integer(required=True)
    south_west = fields.Integer(required=True)
    north_percent = fields.Float(required=True)
    south_percent = fields.Float(required=True)
    west_percent = fields.Float(required=True)
    east_percent = fields.Float(required=True)
    north_east_percent = fields.Float(required=True)
    north_west_percent = fields.Float(required=True)
    south_east_percent = fields.Float(required=True)
    south_west_percent = fields.Float(required=True)
    src_time = fields.DateTime(required=True)
    update_time = fields.DateTime(required=True)

# ====================================================================================================================

class CvpTwrtCityData(db.Model):
    __tablename__ = 'cvp_twrt_city_data'
    name = db.Column(db.String(100), primary_key=True, comment='????????????')
    A = db.Column(db.Integer, comment='???????????????')
    B = db.Column(db.Integer, comment='???????????????')
    C = db.Column(db.Integer, comment='???????????????')
    D = db.Column(db.Integer, comment='???????????????')
    E = db.Column(db.Integer, comment='???????????????')
    F = db.Column(db.Integer, comment='???????????????')
    G = db.Column(db.Integer, comment='???????????????')
    H = db.Column(db.Integer, comment='???????????????')
    I = db.Column(db.Integer, comment='???????????????')
    J = db.Column(db.Integer, comment='???????????????')
    K = db.Column(db.Integer, comment='???????????????')
    M = db.Column(db.Integer, comment='???????????????')
    N = db.Column(db.Integer, comment='???????????????')
    O = db.Column(db.Integer, comment='???????????????')
    P = db.Column(db.Integer, comment='???????????????')
    Q = db.Column(db.Integer, comment='???????????????')
    T = db.Column(db.Integer, comment='???????????????')
    U = db.Column(db.Integer, comment='???????????????')
    V = db.Column(db.Integer, comment='???????????????')
    W = db.Column(db.Integer, comment='???????????????')
    X = db.Column(db.Integer, comment='???????????????')
    Z = db.Column(db.Integer, comment='???????????????')
    total = db.Column(db.Integer, comment='?????????')
    src_time = db.Column(db.DateTime, comment='?????????????????????')
    update_time = db.Column(db.DateTime, server_default=db.func.now(), primary_key=True, comment='????????????')

    def __init__(self, name, A, B, C, D, E, F, G, H, I, J, K, M, N, O, P, Q, T, U, V, W, X, Z, total, src_time, update_time):
        self.name = name
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.E = E
        self.F = F
        self.G = G
        self.H = H
        self.I = I
        self.J = J
        self.K = K
        self.M = M
        self.N = N
        self.O = O
        self.P = P
        self.Q = Q
        self.T = T
        self.U = U
        self.V = V
        self.W = W
        self.X = X
        self.Z = Z
        self.total = total
        self.src_time = src_time
        self.update_time = update_time

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class CvpTwrtCityDataSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = CvpTwrtCityData
        sqla_session = db.session

    name = fields.String(required=True)
    A = fields.Integer(required=True)
    B = fields.Integer(required=True)
    C = fields.Integer(required=True)
    D = fields.Integer(required=True)
    E = fields.Integer(required=True)
    F = fields.Integer(required=True)
    G = fields.Integer(required=True)
    H = fields.Integer(required=True)
    I = fields.Integer(required=True)
    J = fields.Integer(required=True)
    K = fields.Integer(required=True)
    M = fields.Integer(required=True)
    N = fields.Integer(required=True)
    O = fields.Integer(required=True)
    P = fields.Integer(required=True)
    Q = fields.Integer(required=True)
    T = fields.Integer(required=True)
    U = fields.Integer(required=True)
    V = fields.Integer(required=True)
    W = fields.Integer(required=True)
    X = fields.Integer(required=True)
    Z = fields.Integer(required=True)
    total = fields.Integer(required=True)
    src_time = fields.DateTime(required=True)
    update_time = fields.DateTime(required=True)

# ====================================================================================================================
class CvpPopuData(db.Model):
    __tablename__ = 'cvp_popu_data'
    name = db.Column(db.String(100), primary_key=True, comment='????????????')
    count = db.Column(db.Integer, comment='????????????')
    realname_count = db.Column(db.Integer, server_default='0', comment='?????????????????????')
    h0 = db.Column(db.Integer, comment='0????????????')
    h1 = db.Column(db.Integer, comment='1????????????')
    h2 = db.Column(db.Integer, comment='2????????????')
    h3 = db.Column(db.Integer, comment='3????????????')
    h4 = db.Column(db.Integer, comment='4????????????')
    h5 = db.Column(db.Integer, comment='5????????????')
    h6 = db.Column(db.Integer, comment='6????????????')
    h7 = db.Column(db.Integer, comment='7????????????')
    h8 = db.Column(db.Integer, comment='8????????????')
    h9 = db.Column(db.Integer, comment='9????????????')
    h10 = db.Column(db.Integer, comment='10????????????')
    h11 = db.Column(db.Integer, comment='11????????????')
    h12 = db.Column(db.Integer, comment='12????????????')
    h13 = db.Column(db.Integer, comment='13????????????')
    h14 = db.Column(db.Integer, comment='14????????????')
    h15 = db.Column(db.Integer, comment='15????????????')
    h16 = db.Column(db.Integer, comment='16????????????')
    h17 = db.Column(db.Integer, comment='17????????????')
    h18 = db.Column(db.Integer, comment='18????????????')
    h19 = db.Column(db.Integer, comment='19????????????')
    h20 = db.Column(db.Integer, comment='20????????????')
    h21 = db.Column(db.Integer, comment='21????????????')
    h22 = db.Column(db.Integer, comment='22????????????')
    h23 = db.Column(db.Integer, comment='23????????????')
    src_time = db.Column(db.DateTime, comment='?????????????????????')
    update_time = db.Column(db.DateTime, server_default=db.func.now(), comment='????????????')

    def __init__(self, name, count, realname_count, h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16, h17, h18, h19, h20, h21, h22, h23, src_time):
        self.name = name
        self.count = count
        self.realname_count = realname_count
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


class CvpPopuDataSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = CvpPopuData
        sqla_session = db.session

    name = fields.String(required=True)
    count = fields.Integer(required=True)
    realname_count = fields.Integer(required=True)
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

#================================================================
'''
"Age19":1739,"Age29":2550,"Age39":3451,"Age49":3943,"Age59":4254,"Age60":5986
'''

class CvpTwrtAgeData(db.Model):
    __tablename__ = 'cvp_twrt_age_data'
    name = db.Column(db.String(100), primary_key=True, comment='????????????')
    age_19 = db.Column(db.Integer, comment='19?????????')
    age_29 = db.Column(db.Integer, comment='19-29???')
    age_39 = db.Column(db.Integer, comment='29-39???')
    age_49 = db.Column(db.Integer, comment='39-49???')
    age_59 = db.Column(db.Integer, comment='49-59???')
    age_60 = db.Column(db.Integer, comment='???????????????')
    total = db.Column(db.Integer, comment='?????????')
    src_time = db.Column(db.DateTime, comment='?????????????????????')
    update_time = db.Column(db.DateTime, server_default=db.func.now(), primary_key=True, comment='????????????')

    def __init__(self, name, age_19, age_29, age_39, age_49, age_59, age_60, total, src_time, update_time):
        self.name = name
        self.age_19 = age_19
        self.age_29 = age_29
        self.age_39 = age_39
        self.age_49 = age_49
        self.age_59 = age_59
        self.age_60 = age_60
        self.total = total
        self.src_time = src_time
        self.update_time = update_time

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class CvpTwrtAgeDataSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = CvpTwrtCityData
        sqla_session = db.session

    name = fields.String(required=True)
    age_19 = fields.Integer(required=True)
    age_29 = fields.Integer(required=True)
    age_39 = fields.Integer(required=True)
    age_49 = fields.Integer(required=True)
    age_59 = fields.Integer(required=True)
    age_60 = fields.Integer(required=True)
    total = fields.Integer(required=True)
    src_time = fields.DateTime(required=True)
    update_time = fields.DateTime(required=True)

# ====================================================================================================================