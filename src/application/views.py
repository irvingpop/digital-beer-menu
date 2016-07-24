"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""


#google
from google.appengine.api import users

# flask
from flask import render_template, flash, url_for, redirect, request, jsonify, Response

# this app
from application import app, content_admin, util
from decorators import login_required, admin_required

login_url = users.create_login_url()
logout_url = users.create_logout_url('/')

syskey = app.config['SYSKEY']


def home():
    user = users.get_current_user()
    authorized = util.authorize_user(user)
    location = 'frontpage'
    return render_template(
        'home-nofun.html',
        content=content_admin.get_content_cache(),
        location=location,
        user=user,
        authorized=authorized,
        login_url=login_url,
        logout_url=logout_url)


def faq():
    user = users.get_current_user()
    authorized = util.authorize_user(user)
    return render_template(
        'faq.html',
        content=content_admin.get_content_cache(),
        user=user,
        authorized=authorized,
        login_url=login_url,
        logout_url=logout_url)


def menu():
    user = users.get_current_user()
    authorized = util.authorize_user(user)
    beermenu, freshest = util.get_beermenu()
    return render_template(
        'menu.html',
        beermenu=beermenu,
        freshest=freshest.beerid,
        user=user,
        authorized=authorized,
        login_url=login_url,
        logout_url=logout_url)


def barmenu():
    beermenu, freshest = util.get_beermenu()
    return render_template(
        'barmenu.html',
        beermenu=beermenu,
        freshest=freshest.beerid)


def bottlemenu():
    user = users.get_current_user()
    authorized = util.authorize_user(user)
    bottlemenu = util.get_bottlemenu()
    return render_template(
        'bottlemenu.html',
        beermenu=bottlemenu,
        user=user,
        authorized=authorized,
        login_url=login_url,
        logout_url=logout_url)


@login_required
def admin():
    user = users.get_current_user()
    authorized = util.authorize_user(user)
    return render_template(
        'admin.html',
        nofooter=True,
        user=user,
        authorized=authorized,
        login_url=login_url,
        logout_url=logout_url)


@login_required
def admin_bottlemenu():
    user = users.get_current_user()
    authorized = util.authorize_user(user)
    return render_template(
        'bottleadmin.html',
        nofooter=True,
        user=user,
        authorized=authorized,
        login_url=login_url,
        logout_url=logout_url)


@login_required
def admin_data():
    data = util.get_jqgrid_dict(request)
    return jsonify(data)


@login_required
def admin_data_bottlemenu():
    data = util.get_jqgrid_dict_bottle(request)
    return jsonify(data)


@login_required
def admin_edit():
    user = users.get_current_user()
    if request.method == 'POST':
        oper = request.form['oper']
        if oper == "add":
            response = util.beermenu_add_item(request, user)
            return Response(response)
        if oper == "edit":
            response = util.beermenu_edit_item(request, user)
            return Response(response)
        if oper == "del":
            response = util.beermenu_del_item(request, user)
            return Response(response)


@login_required
def admin_edit_bottlemenu():
    user = users.get_current_user()
    if request.method == 'POST':
        oper = request.form['oper']
        if oper == "add":
            response = util.bottlemenu_add_item(request, user)
            return Response(response)
        if oper == "edit":
            response = util.bottlemenu_edit_item(request, user)
            return Response(response)
        if oper == "del":
            response = util.bottlemenu_del_item(request, user)
            return Response(response)


@login_required
def admin_linestatus():
    user = users.get_current_user()
    authorized = util.authorize_user(user)
    linestatus_age, linestatus_beer, linestatus_bartender = util.get_linestatus()
    return render_template(
        'linestatus.html',
        linestatus_age=linestatus_age,
        linestatus_beer=linestatus_beer,
        linestatus_bartender=linestatus_bartender,
        user=user,
        authorized=authorized,
        login_url=login_url,
        logout_url=logout_url)


@login_required
def admin_auditlog():
    user = users.get_current_user()
    authorized = util.authorize_user(user)
    auditlog = util.get_auditlog()
    return render_template(
        'auditlog.html',
        auditlog=auditlog,
        user=user,
        authorized=authorized,
        login_url=login_url,
        logout_url=logout_url)


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    warm0 = content_admin.check_sane_defaults()
    warm1 = util.get_beermenu()
    warm2 = util.get_bottlemenu()
    warm3 = util.get_jqgrid_dict(None)
    warm4 = util.get_jqgrid_dict_bottle(None)
    warm5 = util.get_auditlog()
    warm6 = util.get_linestatus()
    warm7 = content_admin.get_content_cache()
    return True
