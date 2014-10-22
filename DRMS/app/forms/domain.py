#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-23"

from flask.ext.wtf import Form
from wtforms import SelectField, HiddenField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange,Regexp
from app.models import ResolveType




