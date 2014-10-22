#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" application run file"""
__author__ = "zhuhuijie"
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-17"
from flask.ext.script import Manager, Server, prompt_bool,Shell
from app.extensions import db
from app import create_app
from app.models import User,UserInfo,ProcutInfo,ImageInfo,DnsInfo,Domain,DomainData
manager = Manager(create_app("config.cfg"))

def _make_context():
    return dict(db=db)

manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command("runserver", Server('0.0.0.0',port=8080))

@manager.command
def createall():
    "Creates database tables"
    db.create_all()

@manager.command
def dropall():
    "Drops all database tables"

    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()

if __name__ == "__main__":
    manager.run()
