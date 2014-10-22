#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-24"

from app.extensions import db
from datetime import datetime

class ResolveType(db.Model):
    """
        resolve_type orm table
    """
    __tablename__ = "resolve_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    dns = db.relationship('DnsInfo', backref='type', uselist=False)


class DnsInfo(db.Model):
    """
      dns info orm
    """
    __tablename__ = 'dns_info'
    id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String(32))
    resolve_type_id = db.Column(db.Integer, db.ForeignKey('resolve_type.id'), nullable=False)
    url = db.Column(db.String(50))
    status = db.Column(db.String(1))

