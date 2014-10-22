#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-25"
from suds.client import Client
import base64
import time


def upload_product_info(product, file_name, file_data):
    url = 'http://127.0.0.1:5000/soap/productService?wsdl'
    client = Client(url)
    rsp1 = save_product(client, product.product_code, product.product_name, product.introduce,
                        product.detail_info, product.guide_price, product.pack_list)
    print rsp1
    if rsp1[0] == '010':

        rsp2 = save_image(client, rsp1[2], '01', file_name, file_data)
        time.sleep(0.5)
        rsp3 = save_product_custom_service(client, product.product_code, product.phone_num, '')
        print rsp2, rsp3
        if rsp2[0] == '033' and rsp3[0] == '040':
            return [1, 'save ok!']
        else:
            return [0, rsp2[1] + ',' + rsp3[1]]
    else:
        return [0, rsp1[1]]


def query_audit_status(domain_name):
    url = 'http://127.0.0.1:5000/soap/auditService?wsdl'
    client = Client(url)

    rsp = client.service.query_audit_status('zhangsan','123456','www.6921734900241.com')
 #    (QueryDomainStatRsp){
 #      code = "060"
 #      audit_time = 2014-09-11 11:00:59
 #      domain_name = "www.6921734900241.com"
 #      reason = "营业执照审核不通过,看不清;通讯地址审核不通过,与营业执照地址不同"
 #      msg = "Query status Successed!!"
 #      audit_status = "3"
 #    }.encode('utf-8')

    if rsp['code'] == '060':
        reason = unicode(rsp['reason'].encode('gbk'),'gbk')
        return [1, rsp['msg'], {'reason': reason, 'audit_status':rsp['audit_status'],
                                'domain_name':rsp['domain_name'], 'audit_time':rsp['audit_time']
                                }]
    else:
        return [0, rsp['msg'],None]


def upload_data(domain_name,fdata):
    #print domain_name,file_prove_name,f1data,files_image_name,f2data
    
    url = 'http://127.0.0.1:5000/soap/auditService?wsdl'
    client = Client(url)

    rsp = client.service.upload_data("wanwang","123456",domain_name,fdata)

    if rsp['code'] == '050':
    
        return [1, rsp['msg']]
    else:
        return [0, rsp['msg']]


def save_product(client,product_code,product_name,introduce,detail_info,guide_price,pack_list):
    result = client.service.save_product(product_code,product_name,
                                         introduce,detail_info,
                                         guide_price, pack_list)
    code = result['code']
    msg = result['msg']
    pk = result['p_id']

    return [code,msg,pk]


def save_image(client,ref_id, category,file_name, file_data):
    result = client.service.save_image(ref_id, category,file_name, file_data)
    code = result['code']
    msg = result['msg']
    pk = result['f_id']
    return [code, msg, pk]


def save_product_custom_service(client,product_code, phone_num,address):

    result = client.service.save_product_custom_service(product_code, phone_num,address)
    code = result['code']
    msg = result['msg']
    pk = result['c_id']
    return [code,msg,pk]



# r = query_audit_status('www.6921734900241.com')
# print r