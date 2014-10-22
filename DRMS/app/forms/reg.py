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


# class Search(Form):
#     search = StringField(validators = [DataRequired(message = u'请输入查询的条码'),Length(min=13, max=13, message=u'条码长度必须为13位')])


class RegForm(Form):
    code = StringField(u'商品条码:')
    Time_y = StringField(u'服务年限:/年',validators=[DataRequired(message = u'请输入服务时限,以年为单位')])
    prove = FileField(u'请上传条码证书')



class Cont(Form):
    code = StringField(u'商品条码:')
    comp = StringField(u'条码所有单位',validators=[DataRequired(message=u'请输入公司全称')])
    address = StringField(u'通讯地址:xx市xx街xx楼xx室',validators=[DataRequired(message=u'请输入详细地址:xx市xx街xx楼xx室')])
    comp_http = StringField(u'公司网站',validators=[DataRequired(message=u'公司网址')])
    contact = StringField(u'联系人',validators=[DataRequired(message=u'请输入联系人')])
    pno = StringField(u'联系电话:01012345678',validators =[DataRequired(message = u'请输入电话号码'),Length(min=8,max=11,message='请输入正确的电话号码')])
    mno = StringField(u'手机:13566668888',validators=[DataRequired(message=u'请输入手机号码'),Length(min=11,max=13,message='请输入正确的电话号码')])
    email = StringField('email:1221@123.com', validators=[DataRequired(message=u'请填写电子邮件'),Email(message=u'无效的电子邮件')])
    image = FileField(u"上传营业执照")

