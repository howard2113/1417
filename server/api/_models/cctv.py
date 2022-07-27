#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

'''
 {
            "id": "C000079",
            "img": "https://traffic.tbkc.gov.tw/cctvs/C000079/",
            "name": "自立一路/建國三路口",
            "px": 120.29647,
            "py": 22.63792,
            "roadsection": "自立一路/建國三路口",
            "url": "https://cctv6.kctmc.nat.gov.tw/1dd04532/snapshot"
        },
'''


class CctvInfo(db.Model):
    __tablename__ = 'cctv_info'
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50), comment='路線名')
    img = db.Column(db.String(500), comment='方位圖')
    lng = db.Column(db.Float, comment='經度')
    lat = db.Column(db.Float, comment='緯度')
    roadsection = db.Column(db.String(500), server_default='', comment='路口')
    url = db.Column(db.String(500), comment='串流源')
    src_time = db.Column(db.DateTime, comment='源資料時間')
    update_time = db.Column(db.DateTime, server_default=db.func.now(), comment='撈取時間')

    def __init__(self, name, img, lng, lat, roadsection, url, src_time):
        self.name = name
        self.img = img
        self.lng = lng
        self.lat = lat
        self.roadsection = roadsection
        self.url = url
        self.src_time = src_time

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class BusDynamicSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = CctvInfo
        sqla_session = db.session

    name = fields.String(required=True)
    img = fields.String(required=True)
    lng = fields.Float(required=True)
    lat = fields.Float(required=True)
    roadsection = fields.String(required=True)
    url = fields.String(required=True)
    src_time = fields.DateTime(required=True)
