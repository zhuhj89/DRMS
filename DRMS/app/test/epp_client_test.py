#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-26"

from epp_client.interaction import receive_xml
import os
seseses = {"session":{"login":{"clID":"dome","pw":"dome"}}}
xml_obj = receive_xml(seseses)

# context_check_xml_dict ={"domain":{"update":{"name":"1234657890123.niot.cn","chg":{"record":{"type":'1','url':"http://baidu.com"}}}}}
# xml_obj= receive_xml(context_check_xml_dict)
print xml_obj['attrib']['code']

print os.path.abspath('.')

