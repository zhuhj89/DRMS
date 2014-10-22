#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    the domain manage view
"""
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-18"

from flask import Blueprint,Module,render_template,request, redirect, url_for, flash
from flask.ext.login import login_required,current_user
from app.models import ResolveType,DnsInfo,Domain,DomainData
from app.extensions import db
from app.utils.interface import query_audit_status
from epp_client.interaction import receive_xml
from sqlalchemy import and_
import os, sys
from datetime import  datetime,timedelta


domain = Blueprint('domain', __name__)



@domain.route('/list', methods=("GET", "POST"))
@login_required
def domain_list():

    user_id = current_user.user.id
    domain_list = Domain.query.filter(Domain.user_id == user_id).all()

    return render_template('/domain/domain_list.html', domain_list=domain_list)

@domain.route('/show', methods=("GET", "POST"))
@login_required
def domain_show():
    """
       show the one domain detail
    """
    domain_code = request.args.get('domain_code')
    print domain_code
    if domain_code:
        print domain_code
        domain = Domain.query.filter(Domain.domain_code == domain_code).first()
        print domain.create_duration
        disable_time = domain.create_time + timedelta(days=int(domain.create_duration)*365)
        print disable_time
        print domain.domain_data.contact
        return render_template('/domain/domain_show.html', domain=domain,disable_time=disable_time)


@domain.route('/detail', methods=("GET", "POST"))
@login_required
def domain_detail():
    """
       show the one domain detail
    """
    domain_code = request.args.get('domain_code')
    if domain_code:
        print domain_code
        domain = Domain.query.filter(Domain.domain_code == domain_code).first()
        print domain.domain_data.contact
        return render_template('/domain/domain_detail.html', domain=domain)



@domain.route('/dns_update', methods=("GET", "POST"))
@login_required
def dns_update():
    """
        domain dns update
    """
    id = request.args.get('id', None)
    if id:
        dns = DnsInfo.query.get(id)

    next = request.args.get('next', None)

    if request.method == 'POST':
        dns.url = request.form['url']
        dns.resolve_type_id = request.form['resolve_type']
        db.session.merge(dns)

        req_xml = {
            "domain": {
                "update": {
                    "name": dns.domain_name,
                    "chg": {
                        "record": {
                            "type": dns.resolve_type_id,
                            'url': dns.url
                        }
                    }
                }
            }
        }
        print req_xml
        rsp = receive_xml(req_xml)
        print rsp
        if rsp['attrib']['code'] == '1000':
            flash(u'域名解析成功')
            return redirect(url_for('domain.dns_list'))
        else:
            flash(u'域名解析失败')
            types = ResolveType.query.filter().all()
            return render_template('/domain/domain_resolve.html', dns=dns, domain_name=dns.domain_name, next=next, types=types,title=u'域名解析更新')
    else:
        flash(u'存在解析记录')
        types = ResolveType.query.filter().all()
        return render_template('/domain/domain_resolve.html', dns=dns, domain_name=dns.domain_name, next=next, types=types,title=u'域名解析更新')

@domain.route('/dns_save', methods=("GET", "POST"))
@login_required
def dns_save():
    """
        domain name resolve add
    """
    domain_code = request.args.get('domain_code', None)
    domain_name = domain_code + '.niot.cn'

    if domain_name:
        dns = DnsInfo.query.filter(DnsInfo.domain_name == domain_name).first()
        if dns:

            return redirect(url_for('domain.dns_update', id=dns.id, next=url_for('domain.domain_show',domain_code=domain_code)))

    if request.method == 'POST':
        dns = DnsInfo()
        dns.domain_name = domain_name
        dns.url = request.form['url']
        dns.resolve_type_id = request.form['resolve_type']
        req_xml = {
            "domain": {
                "update": {
                    "name": dns.domain_name,
                    "chg": {
                        "record": {
                            "type": dns.resolve_type_id,
                            'url': dns.url
                        }
                    }
                }
            }
        }
        rsp = receive_xml(req_xml)
        print rsp
        if rsp['attrib']['code'] == '1000':
            db.session.add(dns)
            flash(u'域名解析成功')
        return redirect(url_for('domain.domain_show'))
    else:

        types = ResolveType.query.filter().all()
        return render_template('/domain/domain_resolve.html', domain_name=domain_name, next=url_for('domain.domain_show',domain_code=domain_code), types=types,title=u'域名解析添加')


@domain.route('/dns_list', methods=("GET", "POST"))
@login_required
def dns_list():
    """
        list the login user's all domain's dns
    """
    domain_names = ['1234657890123.niot.cn']
    dns = DnsInfo.query.filter(and_(DnsInfo.status == '1', DnsInfo.domain_name.in_(domain_names))).all()
    return render_template('/domain/domain_resolve_list.html', dns=dns)

@domain.route('/dns_del', methods=("GET", "POST"))
@login_required
def dns_delete():
    """
        delete one domain's dns
    """
    id = request.args.get('id')
    if id:
        print id
        dns = DnsInfo.query.get(id)
        dns.status = '0'
    return redirect(url_for('domain.dns_list'))

@domain.route('/query_status', methods=("GET", "POST"))
@login_required
def query_status():
    """
        query the domain's audit status by webservice interface
    """
    domain_code = request.args.get('domain_code')
    domain_name = domain_code + '.niot.cn'
    domain = Domain.query.filter(Domain.domain_code == domain_code).first()
    result = query_audit_status(domain_name)
    print result
    if result[0] == 1:
        print "ok"
        return render_template('/domain/domain_show.html', status=result[2], domain=domain)
    else:
        flash('%s' % result[1])
        print result[1]
        return redirect(url_for('domain.domain_show',domain_code=domain_code))
