#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-22"

from flask import render_template, Blueprint, request, redirect, flash, url_for
from flask.ext.login import current_user, login_required
from app.forms.product import ProductForm
from app.models.product import ProcutInfo, ImageInfo
from app.extensions import db, photos
from app.utils.interface import upload_product_info
import uuid
import base64

product = Blueprint("product", __name__)




@product.route('/upload', methods=("GET", "POST"))
@login_required
def product_upload():
    #
    print current_user.is_authenticated()
    # if not current_user.is_authenticated():
    #     return redirect(url_for('user.signin'))
    product_code = request.args.get('domain_code')
    product = ProcutInfo.query.filter(ProcutInfo.product_code == product_code).first()
    if product:
        product_form = ProductForm(product_code=product.product_code, product_name=product.product_name,
                                   detail_info=product.detail_info, guide_price=product.guide_price,
                                   introduce=product.introduce, pack_list=product.pack_list,
                                   phone_num=product.phone_num,
                                   csrf_enabled=False)
        form = product_form
        images= product.images
    else:
        form = ProductForm(request.values, csrf_enabled=False)
        images =None
    if form.validate_on_submit():
        product = ProcutInfo()
        form.populate_obj(product)
        file = request.files['product_image']
        filename = str(uuid.uuid4()) + '.jpg'
        photos.save(file, name=filename)
        url = photos.url(filename)
        image = ImageInfo()
        image.name = filename
        image.url = url
        product.images = [image]
        p = ProcutInfo.query.filter(ProcutInfo.product_code == product.product_code).first()
        if p is None:
            db.session.add(product)
        else:
            db.session.merge(product)
        fpath = photos.path(filename)
        f = open(fpath, 'rb')
        fdata = base64.b64encode(f.read())
        rsp = upload_product_info(product, filename, fdata)
        print rsp
        if rsp[0] == 1:
            flash(u'资料上传成功', 'success')
            return redirect(url_for('site.index'))
        else:
            pass
    else:
        return  render_template('/product/info_upload.html', form=form,images=images)