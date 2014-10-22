#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-22"
from app.extensions import db


class ProcutInfo(db.Model):
    """
     product into orm
    """
    __tablename__ = 'product_info'

    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(13))
    product_name = db.Column(db.String(32))
    introduce = db.Column(db.String(100))
    detail_info = db.Column(db.String(1000))
    guide_price = db.Column(db.String(8))
    phone_num = db.Column(db.String(15))
    pack_list = db.Column(db.String(500))
    images = db.relationship('ImageInfo', backref=db.backref('product'))




class ImageInfo(db.Model):
    """
      image info orm
    """
    __tablename__ = 'images_info'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    url = db.Column(db.String(500))
    ref_id = db.Column(db.Integer, db.ForeignKey('product_info.id'), nullable=False)



