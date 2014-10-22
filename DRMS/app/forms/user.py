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
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask.ext.babel import gettext, lazy_gettext as _
from flask.ext.login import current_user
from app.models import User
class LoginForm(Form):


    email = StringField('email', validators=[
        DataRequired(message=u'请填写电子邮件'),
        Email(message=u'无效的电子邮件')])
    password = PasswordField('password', validators=[
        DataRequired(message=u'请填写密码'),
        Length(min=5, max=20, message=u'密码应为5到20位字符')])
    next = HiddenField('next')
    remember = BooleanField('remember')

    def __init__(self, *args, **kargs):
        Form.__init__(self, *args, **kargs)
        self.user = None

    # def validate_email(self, field):
    #     # 验证邮箱是否注册
    #     user = User.query.filter(User.email.like(field.data)).first()
    #     if not user:
    #         print self.email.errors
    #         raise ValidationError(u'该邮箱尚未在本站注册')
    #     else:
    #         self.user = user

    def validate(self):

        user = User.query.filter(User.email.like(self.email.data)).first()
        if not user:
            self.email.errors = ValidationError(u'该邮箱尚未在本站注册')
        elif not user.check_password(self.password.data):

            self.password.errors = ValidationError(u'密码不正确')
        else:
            self.user = user

        return len(self.errors) == 0



class SignupForm(Form):


    email = StringField('email', validators=[
        DataRequired(message=u'请填写电子邮件'),
        Email(message=u'无效的电子邮件')])
    nickname = StringField('nickname', validators=[
        DataRequired(message=u'请填写昵称'),
        Length(min=2, max=20, message=u'昵称应为2到20字符')])
    password = PasswordField('password', validators=[
        DataRequired(message=u'请填写密码'),
        Length(min=5, max=20, message=u'密码应为5到20位字符')])
    repassword = PasswordField('repassword', validators=[
        DataRequired(message=u'请填写确认密码'),
        EqualTo('password', message=u'两次输入的密码不一致')])
    next = HiddenField('next')

    code = StringField(_("Signup Code"))

    next = HiddenField()


    def validate_username(self, field):
        user = User.query.filter(User.username.like(field.data)).first()
        if user:
            raise ValidationError(u"用户名已经被注册")

    def validate_email(self, field):
        user = User.query.filter(User.email.like(field.data)).first()
        if user:
            raise ValidationError(u'该邮箱已被注册')


class EditPassForm(Form):

    old_password= PasswordField(u'当前密码', validators=[DataRequired(message=u'请提供当前密码')])
    password = PasswordField(u'新密码', validators=[ \
            DataRequired(message=u'请填写新密码，不能少与5位字符'), \
            EqualTo('confirm', message=u'两次输入的密码不一致'), \
            Length(min=5, max=20, message=u'密码应为5到20位字符')
    ])
    confirm = PasswordField(u'确认密码', validators=[DataRequired(message=u'请再次输入新密码')])
    next = HiddenField()
    def validate_old_password(form, field):
        if not current_user.user.check_password(field.data):
            raise ValidationError(u'提供的原始密码不正确')





