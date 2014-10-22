#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-18"
from flask import Blueprint, redirect, url_for, render_template, request,flash,session,current_app
from flask.ext.login import current_user
from app.extensions import db,login_manager
from flask.ext import login
from flask.ext.login import login_user, login_required
from app.models import User,UserInfo, authenticate
from app.forms.user import SignupForm,LoginForm, EditPassForm
user = Blueprint('user', __name__)

class Anonymous(login.AnonymousUserMixin):
    user = User(nickname=u'游客', email='')

class LoginUser(login.UserMixin):
    """Wraps User object for Flask-Login"""

    def __init__(self, user):
        self.id = user.id
        self.user = user

login_manager.anonymous_user = Anonymous
login_manager.login_view = 'user.signin'
login_manager.login_message = u'需要登陆后才能访问本页'

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user and LoginUser(user) or None

@user.route("/login/", methods=("GET","POST"))
def signin():

    flag = request.args.get('flag')

    if current_user.is_authenticated():
        if flag:
            return redirect(url_for('admin.index'))
        return redirect(url_for('site.index'))

    form = LoginForm(login=request.args.get('login',None),
                     next=request.args.get('next',None))
    if form.validate_on_submit():
        user, authenticated = authenticate(form.email.data,
                                                      form.password.data)
        if user and authenticated:
            # session.permanent = form.remember.data
            remberme = form.remember.data
            # identity_changed.send(current_app._get_current_object(),
            #                       identity=Identity(user.id))
            login_user(user, remberme)

            next_url = form.next.data
            user.is_login = 1

            if not next_url or next_url == request.path:
                if flag:
                    next_url = url_for('admin.index', username=user.nickname)
                else:
                    next_url = url_for('site.index', username=user.nickname)
            return redirect(next_url)

        else:
            pass
            # flash(_("Sorry, invalid login"), "error")
    return render_template("user/signin.html", form=form, flag=flag)



@user.route('/edit_pass', methods=("GET","POST"))
@login_required
def edit_pass():
    form = EditPassForm(next=request.args.get('next',None))
    print request.path
    print form.next.data
    if form.validate_on_submit():
        print "*"*50

        print current_user.user.password
        current_user.user._set_password(form.password.data)
        print current_user.user.password
        print "*"*50
        flash(u'用户密码已经更新', 'success')
        # return form.redirect("user.edit_pass")
        return redirect(url_for('site.index'))
    else:
        # form.errors and flash(u'用户密码未能更新', 'error')
        return render_template('user/edit_pass.html', form=form)

@user.route('/logout')
@login_required
def signout():

    privilege = current_user.user.privilege

    user = User.query.get(current_user.user.id)
    user.is_login = 0
    print privilege
    if privilege == 3:
        to_url = url_for('site.index')
    elif privilege == 4:
        print "---------"
        to_url = url_for('admin.index')
    login.logout_user()

    return redirect(to_url)


@user.route('/signup/', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated():
        return redirect(url_for('site.index'))

    form = SignupForm(request.values, csrf_enabled=False)

    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.info = UserInfo()
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.signin'))
    else:
        print "signup"
        return render_template('user/signup.html', form=form)

