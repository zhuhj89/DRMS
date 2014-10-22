#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-18"
from flask import Blueprint, redirect, url_for, render_template, request,flash
from app.forms.admin import LoginForm
from epp_client.interaction import receive_xml

admin = Blueprint('admin', __name__)


@admin.route('/', methods=("GET", "POST"))
def admin_sin():
    form = LoginForm()
    if request.method == 'POST':
        clID = request.form['admin']
        pw = request.form['password']
        print clID,pw
        req_xml = {"session":{"login":{"clID":clID,"pw":pw}}}
        print req_xml
        rsp = receive_xml(req_xml)
        print rsp
        if rsp['attrib']['code'] == '1000':
            flash(u'登陆成功')
            return redirect(url_for('site.index'))
        else:
            flash(u'登陆失败')
            return render_template('/admin/admin.html',form=form)
    
    return render_template('/admin/admin.html',form=form)