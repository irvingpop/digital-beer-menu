from google.cloud import ndb
from application import models
from wtforms_appengine.ndb import model_form

import datetime

from flask_caching import Cache
from application import app, util

cache = Cache(with_jinja2_ext=False)
cache.init_app(app, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': '/tmp'})

syskey = app.config['SYSKEY']


def clear_caches_beermenu():
    cache.delete_memoized(get_jqgrid_dict)
    cache.delete_memoized(get_beermenu)
    cache.delete_memoized(get_linestatus)
    cache.delete_memoized(get_auditlog)
    return True


@cache.memoize()
def get_beermenu():
    beermenu = models.BeerMenu.query().filter(models.BeerMenu.active == True).fetch()    # noqa
    freshest = models.FreshestBeer.get_or_insert(syskey)
    beermenu_sorted = sorted(
        beermenu,
        key=lambda self: util.strip_accents(
            self.name.lower()))
    return beermenu_sorted, freshest

# return dict that is ready for jsonify,  in jqgrid expected format
# TODO: _search handler
# TODO: pagination handler


@cache.memoize()
def get_jqgrid_dict(request):
    """
    :param request:
    :return data:
    """

    beermenu_keys = models.BeerMenu.query()
    beermenu = ndb.get_multi(beermenu_keys.fetch(keys_only=True))
    beermenu_sorted = sorted(
        beermenu, key=lambda self: (
            util.strip_accents(
                self.brewery.lower()), util.strip_accents(
                self.name.lower())))
    freshest = models.FreshestBeer.get_or_insert(syskey)

    rows = []
    for p in beermenu_sorted:
        pdict = p.to_dict()
        pdict['id'] = p.key.id()
        pdict['beerid'] = p.key.id()

        # blank field for action
        pdict['act'] = ' '

        # fix purdate formatting for json serialization
        if p.purdate is not None:
            pdict['purdate'] = p.purdate.strftime("%Y-%m-%d")

        if p.active is True:
            pdict['active'] = "true"
        else:
            pdict['active'] = "false"

        # set freshest beer id
        if pdict['id'] == freshest.beerid:
            pdict['freshest'] = 'true'
        else:
            pdict['freshest'] = 'false'

        rows.append(pdict)

    data = dict(total=1, page=1, records=beermenu_keys.count(), rows=rows)
    return data


def beermenu_set_freshest(beerid):
    freshest = models.FreshestBeer.get_or_insert(syskey)
    freshest.beerid = beerid
    freshest.put()


def beermenu_add_item(request, user):
    form = model_form(models.BeerMenu)
    form_object = form(formdata=request.form)
    if not form_object.errors and form_object.validate():
        item = models.BeerMenu()
        form_object.populate_obj(item)
        # why the F does false not get detected correctly
        if request.form['active'] == 'false':
            item.active = False
        item_key = item.put()
        if request.form['freshest'] == "true":
            beermenu_set_freshest(item_key.id())
        # write audit log
        item_beerid = item_key.id()
        new_item = item.to_dict()
        write_auditlog(None, new_item, item_beerid, user, request.form['oper'])
        response = 'OK:\n user: %s\n oper: %s\n beerid: %s\n changed: %s\n' % (
            user, request.form['oper'], item_beerid, new_item)
        clear_caches_beermenu()
        return response
    else:
        response = '%s\n %s' % (form_object.errors, form_object.validate())
        return response


def beermenu_edit_item(request, user):
    reqid = int(request.form['id'])
    item = models.BeerMenu.get_by_id(reqid, parent=None)
    old_item = item.to_dict().copy()
    if item:
        form = model_form(models.BeerMenu)
        form_object = form(formdata=request.form)
        if not form_object.errors and form_object.validate():
            form_object.populate_obj(item)
            # why the F does false not get detected correctly
            if request.form['active'] == 'false':
                item.active = False
            item_key = item.put()
            if request.form['freshest'] == "true":
                beermenu_set_freshest(item_key.id())
            # write audit log
            new_item = item.to_dict()
            item_beerid = item_key.id()
            write_auditlog(
                old_item,
                new_item,
                item_beerid,
                user,
                request.form['oper'])
            response = 'OK:\n user: %s\n oper: %s\n beerid: %s\n changed: %s\n' % (
                user, request.form['oper'], item_beerid, new_item)
            clear_caches_beermenu()
            return response
        else:
            response = '%s\n %s' % (form_object.errors, form_object.validate())
            return response
    else:
        return 'item not found!!\n'


def beermenu_del_item(request, user):
    reqid = int(request.form['id'])
    item = models.BeerMenu.get_by_id(reqid, parent=None)
    if item:
        # handle freshest
        old_item = item.to_dict().copy()
        freshest = models.FreshestBeer.get_or_insert(syskey)
        if item.key.id() == freshest.beerid:
            freshest.beerid = 0
            freshest.put()
        item_beerid = item.key.id()
        item.key.delete()
        write_auditlog(old_item, None, item_beerid, user, request.form['oper'])
        response = 'OK:\n user: %s\n oper: %s\n beerid: %s\n changed: %s\n' % (
            user, request.form['oper'], item_beerid, old_item)
        clear_caches_beermenu()
        return response
    else:
        return 'item not found!!\n'


def write_auditlog(old_item, new_item, beerid, user, oper):
    """
    Writes out entries to audit log DB
    :param old_item:
    :param new_item:
    :param beerid:
    :param user:
    :param oper:
    """
    auditlog = models.BeerMenuAuditLog()
    auditlog.beerid = beerid
    auditlog.user = user
    auditlog.oper = oper
    if old_item:
        auditlog.orig_values = old_item
    if new_item:
        auditlog.new_values = new_item
    auditlog_key = auditlog.put()
    if auditlog_key:
        return True
    else:
        return False


@cache.memoize()
def get_linestatus():
    linestatus_age = {}
    linestatus_beer = {}
    linestatus_bartender = {}
    i = 1
    while i < 51:
        results = models.BeerMenuAuditLog().query().filter(
            models.BeerMenuAuditLog.new_values.lineno == i
        ).order(
            -models.BeerMenuAuditLog.timestamp
        ).fetch(1)
        for result in results:
            now = datetime.datetime.now()
            days_since = abs((now - result.timestamp).days)
            linestatus_age[i] = days_since
            linestatus_beer[i] = '%s - %s' % (result.new_values.name,
                                              result.new_values.brewery)
            linestatus_bartender[i] = result.new_values.bartender
            break
        if not results:
            linestatus_age[i] = 0
        i += 1

    return linestatus_age, linestatus_beer, linestatus_bartender


@cache.memoize()
def get_auditlog():
    auditlog = models.BeerMenuAuditLog.query().order(
        -models.BeerMenuAuditLog.timestamp
    ).fetch(100)
    return auditlog
