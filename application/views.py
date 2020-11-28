"""
views.py

URL route handlers
"""

# flask
from flask import render_template, request, jsonify, Response

# this app
from application import content_admin, beermenu, bottlemenu, users


def disp_home():
    location = 'frontpage'
    return render_template(
        'home-nofun.html',
        content=content_admin.get_content_cache(),
        location=location,
        current_user=users.template_auth_params())


def disp_faq():
    return render_template(
        'faq.html',
        content=content_admin.get_content_cache(),
        current_user=users.template_auth_params())


def disp_menu():
    beermenu_dict, freshest = beermenu.get_beermenu()
    return render_template(
        'menu.html',
        beermenu=beermenu_dict,
        freshest=freshest.beerid,
        current_user=users.template_auth_params())


def disp_barmenu():
    beermenu_dict, freshest = beermenu.get_beermenu()
    return render_template(
        'barmenu.html',
        beermenu=beermenu_dict,
        freshest=freshest.beerid)


def disp_bottlemenu():
    bottlemenu_dict = bottlemenu.get_bottlemenu()
    return render_template(
        'bottlemenu.html',
        beermenu=bottlemenu_dict,
        current_user=users.template_auth_params())


@users.login_required
def admin():
    return render_template(
        'admin.html',
        nofooter=True,
        current_user=users.template_auth_params())


@users.login_required
def admin_bottlemenu():
    return render_template(
        'bottleadmin.html',
        nofooter=True,
        current_user=users.template_auth_params())


@users.login_required
def admin_data():
    data = beermenu.get_jqgrid_dict(request)
    return jsonify(data)


@users.login_required
def admin_data_bottlemenu():
    data = bottlemenu.get_jqgrid_dict_bottle(request)
    return jsonify(data)


@users.login_required
def admin_edit():
    if request.method == 'POST':
        oper = request.form['oper']
        if oper == "add":
            response = beermenu.beermenu_add_item(
                request, users.get_current_user())
            return Response(response)
        if oper == "edit":
            response = beermenu.beermenu_edit_item(
                request, users.get_current_user())
            return Response(response)
        if oper == "del":
            response = beermenu.beermenu_del_item(
                request, users.get_current_user())
            return Response(response)


@users.login_required
def admin_edit_bottlemenu():
    if request.method == 'POST':
        oper = request.form['oper']
        if oper == "add":
            response = bottlemenu.bottlemenu_add_item(
                request, users.get_current_user())
            return Response(response)
        if oper == "edit":
            response = bottlemenu.bottlemenu_edit_item(
                request, users.get_current_user())
            return Response(response)
        if oper == "del":
            response = bottlemenu.bottlemenu_del_item(
                request, users.get_current_user())
            return Response(response)


@users.login_required
def admin_linestatus():
    linestatus_age, linestatus_beer, linestatus_bartender = beermenu.get_linestatus()
    return render_template(
        'linestatus.html',
        linestatus_age=linestatus_age,
        linestatus_beer=linestatus_beer,
        linestatus_bartender=linestatus_bartender,
        current_user=users.template_auth_params())


@users.login_required
def admin_auditlog():
    auditlog = beermenu.get_auditlog()
    return render_template(
        'auditlog.html',
        auditlog=auditlog,
        current_user=users.template_auth_params())


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    warm0 = content_admin.check_sane_defaults()
    warm1, _ = beermenu.get_beermenu()
    warm2 = bottlemenu.get_bottlemenu()
    warm3 = beermenu.get_jqgrid_dict(None)
    warm4 = bottlemenu.get_jqgrid_dict_bottle(None)
    warm5 = beermenu.get_auditlog()
    warm6, _, _ = beermenu.get_linestatus()
    warm7 = content_admin.get_content_cache()
    if (warm0
        and isinstance(warm1, list)
        and isinstance(warm2, list)
        and isinstance(warm3, dict)
        and isinstance(warm4, dict)
        and isinstance(warm5, list)
        and isinstance(warm6, dict)
            and isinstance(warm7, dict)):
        return render_template(
            'warmup.html',
            warmup_message='Feeling warm and toasty!')
    else:
        return render_template(
            'warmup.html',
            warmup_message='Feeling sad actually')
