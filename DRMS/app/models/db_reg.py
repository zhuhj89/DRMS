#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-22"
from app.extensions import db
from datetime import datetime
class Domain(db.Model):
    """
     product into orm
    """
    __tablename__ = 'domain'

    id = db.Column(db.Integer, primary_key=True)
    domain_code = db.Column(db.String(32), unique=True, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now) # 用户注册时间
    create_duration = db.Column(db.String(32))
    user_id = db.Column(db.String(50), nullable=False)
    prove = db.Column(db.String(500))
    domain_data_id = db.Column(db.Integer,db.ForeignKey('domain_data.id'))

class DomainData(db.Model):

    __tablename__ = 'domain_data'
    
    id = db.Column(db.Integer, primary_key=True)
    comp = db.Column(db.String(500))
    address = db.Column(db.String(500))
    contact = db.Column(db.String(100))
    pno = db.Column(db.String(15))
    tno = db.Column(db.String(15))
    email = db.Column(db.String(100))
    image = db.Column(db.String(500))
    user_id = db.Column(db.String(50))
    domains = db.relationship('Domain',backref ="domain_data" )
    

