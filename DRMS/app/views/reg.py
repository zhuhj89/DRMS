#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import render_template, Blueprint, request, redirect, flash, url_for
from flask.ext.login import current_user, login_required
from app.forms.reg import  Cont,RegForm
from app.models.db_reg import Domain, DomainData
from app.extensions import db, photos
from app.utils.interface import upload_product_info,upload_data
import uuid
import base64
from datetime import datetime,timedelta
from epp_client.interaction import receive_xml
import os,sys

reg = Blueprint("reg", __name__)
   
@reg.route('/', methods=("GET", "POST"))
@reg.route('/search',methods=("GET", "POST"))
@login_required
def domain_search():
    if request.method =='POST':
        name = request.form['code']
        if name.isdigit() and len(name) == 13:
            req_xml = {"domain":{"check":{"name":name}}}
            rsp = receive_xml(req_xml)
            if rsp['attrib']['code'] == '1000':
                if rsp['attrib']['avail'] == '0':
                    flash(u"该条码已注册")
                    return render_template('/reg/search.html')
                if rsp['attrib']['avail'] == '1':
                    flash(u"该条码未注册")
                    result = u'未注册'
                    return render_template('/reg/search.html',code=name,result=result)
            else:
                flash(u"系统连接错误")
                return redirect(url_for('site.index'))

        else:

            flash(u"该条码必须是13位数字")
            return render_template('/reg/search.html')
    return render_template('/reg/search.html')


@reg.route('/reg', methods=("GET", "POST"))
@login_required
def domain_reg():
    codes =  request.args.get('codes')
    contact = current_user.user.email
    contact_check = {"contact":{"check":{"id":contact}}}
    rp = receive_xml(contact_check)
    if rp["attrib"]['code'] == '1000':
        if rp["attrib"]['avail'] == '1':
            form = RegForm(code=codes)
            if request.method == 'POST':
                names = request.form['code']
                period = request.form['Time_y']
                req_xml = {
                    "domain":{
                        "create":{
                            "name":names,
                            "period":period,
                            "hostObj":"2.cnnic.com",
                            "registrant":"ClientX",
                            "contact":contact
                            }
                        }
                    }
                rsp = receive_xml(req_xml)
                if rsp['attrib']['code'] == '1000':
                    domain_pro = Domain()
                    domain_pro.domain_code = names
                    domain_pro.create_time = datetime.now()
                    domain_pro.create_duration = request.form['Time_y']
                    f = DomainData.query.filter(DomainData.user_id == current_user.id).first().id
                    print f,"=============+++++++++++++++"
                    domain_pro.domain_data_id = f
                    #domain_pro.modified_time = datetime.now()
                    domain_pro.user_id = current_user.id

                    # file_prove = request.files['prove']
                    # file_prove_name = str(uuid.uuid4()) + ".jpg"
                    # photos.save(file_prove,name = file_prove_name)
                    # url_prove = photos.url(file_prove_name)
                    # domain_pro.prove = url_prove 
                    p = Domain.query.filter(Domain.domain_code == domain_pro.domain_code).first()
                    if p is None:
                        db.session.add(domain_pro)
                    else:
                        db.session.merge(domain_pro)

                    # fpath = photos.path(file_prove_name)
                    # f = open(fpath,'rb')
                    # fdata = base64.b64encode(f.read())
                    # domain_name = form.code.data
                    # res1 = upload_data(domain_name,fdata)
           
                    # if res1[0] == 1:
                    #     flash(u'资料上传成功')
                    # else:
                    #     flash(u'资料上传失败 原因: %s' % res1[1])
                    #     render_template('/reg/reg.html',form=form)

                    flash(u'域名注册成功')
                    return redirect(url_for('site.index'))
                else:
                    flash(u'域名注册失败')
                    return render_template('/reg/reg.html',form=form)
            else:
                return render_template('/reg/reg.html',form=form)
        if rp["attrib"]['avail'] == '0':
            flash(u'请先创建注册信息')
            return redirect(url_for('reg.domian_con',codes = codes))
    else:
        flash(u'系统错误')
        return render_template('/reg/search.html')

    return render_template('/reg/reg.html',form=form)

@reg.route('/con',methods=("GET", "POST"))
@login_required
def domian_con():
    codes =  request.args.get('codes')
    form = Cont()
    if request.method == 'POST':
        comp = form.comp.data
        address = form.address.data
        contact = form.contact.data
        pno = form.pno.data
        mno = form.mno.data
        email = form.email.data
        user_id = current_user.user.email
        req_xml = {
            "contact":{
                "create":{
                    "id":user_id,
                    "name":contact,
                    "street":address,
                    "voice":pno,
                    "fax":mno,
                    "email":email,
                    "cc":"cn",
                    "city":"beijing",
                    "sp":"VA",
                    "pc":"20166-6503"
                    }
                }
            }
        rsp = receive_xml(req_xml)
        if rsp['attrib']['code'] == '1000':
            data_pro = DomainData()
            data_pro.comp = comp
            data_pro.address = address
            data_pro.contact = contact
            data_pro.pno = pno
            data_pro.mno = mno
            data_pro.email = email
            data_pro.user_id = current_user.id
            # files_image = request.files['image']
            # files_image_name = str(uuid.uuid4()) + '.jpg'
            # photos.save(files_image,name = files_image_name)
            # url_image = photos.url(files_image_name)
            # data_pro.image = url_image
            p = DomainData.query.filter(DomainData.user_id == data_pro.user_id).first()
            if p is None:
                db.session.add(data_pro)
            else:
                db.session.merge(data_pro)

            # fpath = photos.path(files_image_name)
            # f = open(fpath,'rb')
            # fdata = base64.b64encode(f.read())
            # domain_name = codes
            # print domain_name,"&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
            # res1 = upload_data(domain_name,fdata)
   
            # if res1[0] == 1:
            #     flash(u'资料上传成功')
            # else:
            #     flash(u'资料上传失败 原因: %s' % res1[1])
            #     render_template('/reg/con.html',form=form)
            
            flash(u'信息添加成功,现在可进行域名注册')
            print codes,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
            return redirect(url_for('reg.domain_search',code = codes))

        else:
            flash(u'信息已存在,请勿重复添加')
            print codes,"--------------------------------------------------------------"
            #return render_template('/reg/reg.html',codes = codes)
            return redirect(url_for('reg.domain_search',codes = codes))
            #return redirect(url_for('site.index'))
    return render_template('/reg/con.html',form=form)
