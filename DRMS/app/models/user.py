#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-18"
from app.extensions import db
from datetime import datetime
from flask import url_for, abort
from app.utils.commion import md5
from flask import request
from flask.ext.sqlalchemy import BaseQuery


class UserInfo(db.Model):
    """
    用户信息表
    """
    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True)
    motoo = db.Column(db.String(255)) # 座右铭
    introduction = db.Column(db.Text) # 个人简介
    phone = db.Column(db.String(15), unique=True, nullable=True) # 手机号码
    phone_status = db.Column(db.Integer, nullable=True) # 手机可见度: 0-不公开 1-公开 2-向成员公开
    photo = db.Column(db.String(255), nullable=True) # 存一张照片，既然有线下的聚会的，总得认得人才行

    user = db.relationship('User', backref='info', uselist=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
    def __repr__(self):
        return "<UserInfo (%s)>" % self.user.id


class User(db.Model):
    """
    用户表
    修改email地址时需要经过验证
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False) # 登陆使用的
    email_status = db.Column(db.Integer, nullable=True, default=0) # 邮箱可见度: 0-不公开 1-公开 2-向成员公开
    nickname = db.Column(db.String(50), unique=True, nullable=False) # 昵称, 显示时用的
    _password = db.Column("password", db.String(80), nullable=False) # 密码
    is_email_verified = db.Column(db.Boolean, nullable=False, default=True)
    is_login = db.Column(db.Integer,  default=0)  # 用户页面
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.now) # 用户注册时间
    modified_time = db.Column(db.DateTime, nullable=False, default=datetime.now) # 用户更新时间
    last_login_time = db.Column(db.DateTime) # 最后一次登陆时间
    privilege = db.Column(db.Integer, default=3) # 权重：3-普通用户 4-管理员
    user_info_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.nickname

    def __repr__(self):
        return "<%s>" % self

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = md5(password)

    def check_password(self, password):
        return self.password == md5(password)

    password = db.synonym("_password",
                          descriptor=property(_get_password,
                                              _set_password))
    @property
    def url(self):
        if self.slug:
            return url_for('user.profile', slug=self.slug)
        return url_for('user.profile', user_id=self.id)

    def get_avatar_url(self, size=20):
        url_tpl = 'http://www.gravatar.com/avatar/%s?size=%s&d=%s%s'
        return url_tpl % (md5(self.email), size, request.url_root, url_for('static', filename='images/avatars/default.png'))




def from_identity(identity):
    """
    Loads user from flaskext.principal.Identity instance and
    assigns permissions from user.

    A "user" instance is monkeypatched to the identity instance.

    If no user found then None is returned.
    """

    try:
        user = User.query.get(int(identity.name))
    except ValueError:
        user = None

    if user:
        identity.provides.update(user.provides)

    identity.user = user

    return user

def authenticate(login, password):

    user = User.query.filter(db.or_(User.nickname==login,
                              User.email==login)).first()

    if user:
        authenticated = user.check_password(password)
    else:
        authenticated = False

    return user, authenticated

def search(key):
    query = User.query.filter(db.or_(User.email==key,
                               User.nickname.ilike('%'+key+'%'),
                               User.nickname.ilike('%'+key+'%')))
    return query

# def get_by_username(username):
#     user = User.query.filter(User.username==username).first()
#     if user is None:
#         abort(404)
#     return user
