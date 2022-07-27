#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from api.utils.database import db



class Ui_record(db.Model):
    __tablename__ = 'ui_record'
    user_id = db.Column(db.Integer, primary_key=True, comment='使用者ID')
    page_configs = db.Column(db.Text, comment='UI元件設定')
    update_time = db.Column(db.DateTime, default=datetime.utcnow, comment='資料更新時間')

    def __init__(self, user_id, page_configs):
        self.user_id = user_id
        self.page_configs = page_configs

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

