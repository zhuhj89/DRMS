#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-18"

"""
    validators.py
    ~~~~~~~~~~~~~

    :license: BSD, see LICENSE for more details.
"""
from wtforms.validators import regexp

from flask.ext.babel import lazy_gettext as _

USERNAME_RE = r'^[\w.+-]+$'

is_username = regexp(USERNAME_RE, 
                     message=_("You can only use letters, numbers or dashes"))

