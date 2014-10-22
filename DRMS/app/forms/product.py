#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-22"
from flask.ext.wtf import Form
from wtforms import TextAreaField, HiddenField, BooleanField, FileField,\
        PasswordField, SubmitField, StringField, ValidationError,validators
from wtforms.validators import DataRequired, Email, EqualTo, Length



class ProductForm(Form):
    product_code = StringField(u'商品条码', validators=[
        DataRequired(message=u'请输入商品条码'),
        Length(min=13, max=13, message=u'条码长度必须为13位')])
    product_name = StringField(u'商品名', validators=[DataRequired(message=u'请输入商品名')])
    introduce = StringField(u'商品简介', validators= [Length(min=10, max=100, message=u'50字以内')])
    detail_info = TextAreaField(u'商品详细信息')
    guide_price = StringField(u'指导价')
    phone_num = StringField(u'售后电话')
    pack_list = StringField(u'包装清单')
    product_image = FileField(u"上传商品图片")
