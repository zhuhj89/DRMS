#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-18"

from flask.ext.wtf import Form
from wtforms import TextAreaField, HiddenField, BooleanField, \
        PasswordField, SubmitField, StringField, ValidationError
from wtforms.validators import DataRequired



class LoginForm(Form):
    admin = StringField(u'注册商id', validators=[DataRequired(message=u'请输入注册商名')])
    password = PasswordField(u'密码', validators=[DataRequired(message=u'请填写密码')])




