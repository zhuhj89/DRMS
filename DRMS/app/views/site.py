#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-18"

from flask import render_template,Blueprint
site = Blueprint("site", __name__)

@site.route('/')
def index():
    return  render_template('index.html')