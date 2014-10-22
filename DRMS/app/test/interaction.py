#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "gaoguming"
__email__ = "gaoguming@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09"

from lxml import etree

from epp_client.view.c_session import Session
from epp_client.view.c_contact import Contact
from epp_client.view.c_domain import Domain
from epp_client.view.c_host import Host
from epp_client.view.r_analysis import Analysis
from epp_client.view.socket_client import connection_transfer_xml_twisted as CTX
import os,sys
path = os.path.split(os.path.realpath(__file__))[0]

def open_sd():
    f = open(os.path.join(path,"__SEID"))
    s=f.readlines()
    f.close()
    if s:
        return s[0].strip()
    else:
        return ' '

def receive_xml(node):
    SE = Session()
    CT = Contact()
    DN = Domain()
    HT = Host()
    RA = Analysis()

    r_dict = node


    for i in r_dict.keys():

        if "domain" in i:
            r_d = r_dict["domain"]
            seid = open_sd()
            m_x = DN.receive_xml(r_d,seid)
            Context = etree.tostring(m_x, encoding='UTF-8', standalone=False, pretty_print=True)
            print "----------"
            print Context
            result_xml = CTX(Context)
            DICT = RA.receive_xml(result_xml)
            return DICT     

        if "contact" in i:
            r_d = r_dict["contact"]
            m_x = CT.receive_xml(r_d)
            Context = etree.tostring(m_x, encoding='UTF-8', standalone=False, pretty_print=True)
            result_xml = CTX(Context)
            DICT = RA.receive_xml(result_xml)
            return DICT
            print DICT
        if "host" in i:
            r_d = r_dict["host"]
            m_x = HT.receive_xml(r_d)
            Context = etree.tostring(m_x, encoding='UTF-8', standalone=False, pretty_print=True)
            result_xml = CTX(Context)
            DICT = RA.receive_xml(result_xml)
            return DICT
        if "session" in i:
            r_d = r_dict["session"]
            m_x = SE.receive_xml(r_d)
            Context = etree.tostring(m_x, encoding='UTF-8', standalone=False, pretty_print=True)
            print Context
            result_xml = CTX(Context)
            DICT = RA.receive_xml(result_xml)
            try:
                dicts = DICT['r_date']
                key = dicts.keys()
                if "seid" in key:
                    seid = dicts["seid"]
                    f = open(os.path.join(path,"__SEID"),"w")
                    f.write(seid)
                    f.close()
            except:
                pass    
            return DICT


