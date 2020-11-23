from google.cloud import ndb
from application import models
from wtforms_appengine.ndb import model_form

from xml.dom.minidom import parse
import urllib, base64, datetime
from flask_caching import Cache
from application import app, util

cache = Cache(with_jinja2_ext=False)
cache.init_app(app, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': '/tmp'})

syskey = app.config['SYSKEY']

def clear_caches_bottlemenu():
    cache.delete_memoized(get_jqgrid_dict_bottle)
    cache.delete_memoized(get_bottlemenu)
    return True

@cache.memoize()
def get_bottlemenu():
    bottlemenu = models.BottleMenu.query(models.BottleMenu.active == True).fetch()
    bottlemenu_sorted = sorted(bottlemenu, key=lambda self: util.strip_accents(self.name.lower()))
    return bottlemenu_sorted

@cache.memoize()
def get_jqgrid_dict_bottle(request):
        """
        :param request:
        :return data:
        """

        bottlemenu_keys = models.BottleMenu.query()
        bottlemenu = ndb.get_multi(bottlemenu_keys.fetch(keys_only=True))
        bottlemenu_sorted = sorted(bottlemenu, key=lambda self: (util.strip_accents(self.brewery.lower()), util.strip_accents(self.name.lower())))

        rows = []
        for p in bottlemenu_sorted:
            pdict = p.to_dict()
            pdict['id'] = p.key.id()
            pdict['beerid'] = p.key.id()
            # blank field for action
            pdict['act'] = ' '
            if p.active is True:
                pdict['active'] = "true"
            else:
                pdict['active'] = "false"
            rows.append(pdict)

        data = dict(total=1, page=1, records=bottlemenu_keys.count(), rows=rows)
        return data

def bottlemenu_add_item(request, user):
    form = model_form(models.BottleMenu)
    form_object = form(formdata=request.form)
    if not form_object.errors and form_object.validate():
        item = models.BottleMenu()
        form_object.populate_obj(item)
        if request.form['active'] == 'false':
            item.active = False
        item_key = item.put()
        # write audit log
        item_beerid = item_key.id()
        new_item = item.to_dict()
        response = 'OK:\n user: %s\n oper: %s\n beerid: %s\n changed: %s\n' % (user, request.form['oper'], item_beerid, new_item)
        clear_caches_bottlemenu()
        return response
    else:
        response = '%s\n %s' % (form_object.errors, form_object.validate())
        return response


def bottlemenu_edit_item(request, user):
    reqid = int(request.form['id'])
    item = models.BottleMenu.get_by_id(reqid, parent=None)
    if item:
        form = model_form(models.BottleMenu)
        form_object = form(formdata=request.form)
        if not form_object.errors and form_object.validate():
            form_object.populate_obj(item)
            if request.form['active'] == 'false':
                item.active = False
            item_key = item.put()
            # write audit log
            new_item = item.to_dict()
            item_beerid = item_key.id()
            response = 'OK:\n user: %s\n oper: %s\n beerid: %s\n changed: %s\n' % (user, request.form['oper'], item_beerid, new_item)
            clear_caches_bottlemenu()
            return response
        else:
            response = '%s\n %s' % (form_object.errors, form_object.validate())
            return response
    else:
        return 'item not found!!\n'


def bottlemenu_del_item(request, user):
    reqid = int(request.form['id'])
    item = models.BottleMenu.get_by_id(reqid, parent=None)
    if item:
        # handle freshest
        old_item = item.to_dict().copy()
        item_beerid = item.key.id()
        item.key.delete()
        response = 'OK:\n user: %s\n oper: %s\n beerid: %s\n changed: %s\n' % (user, request.form['oper'], item_beerid, old_item)
        clear_caches_bottlemenu()
        return response
    else:
        return 'item not found!!\n'
