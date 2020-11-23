# -*- coding: utf-8 -*-
"""
models.py

App Engine datastore models

"""
from google.cloud import ndb
from flask_admin_patch.view import NdbModelView
from application import util, users, content_admin
from flask import redirect, request


class BeerMenu(ndb.Model):
    name = ndb.StringProperty()
    brewery = ndb.StringProperty()
    origin = ndb.StringProperty()
    abv = ndb.FloatProperty(indexed=False)
    size = ndb.FloatProperty(indexed=False)
    meas = ndb.StringProperty()
    price = ndb.FloatProperty(indexed=False)
    active = ndb.BooleanProperty()
    url = ndb.StringProperty()
    bartender = ndb.StringProperty()
    lineno = ndb.IntegerProperty(indexed=False)
    purdate = ndb.DateProperty(indexed=False)
    costper = ndb.FloatProperty(indexed=False)


class BeerMenuModelforAuditLog(ndb.Model):
    name = ndb.StringProperty()
    brewery = ndb.StringProperty()
    origin = ndb.StringProperty()
    abv = ndb.FloatProperty(indexed=False)
    size = ndb.FloatProperty(indexed=False)
    meas = ndb.StringProperty()
    price = ndb.FloatProperty(indexed=False)
    active = ndb.BooleanProperty()
    url = ndb.StringProperty()
    bartender = ndb.StringProperty()
    lineno = ndb.IntegerProperty(indexed=True)
    purdate = ndb.DateProperty(indexed=False)
    costper = ndb.FloatProperty(indexed=False)


class FreshestBeer(ndb.Model):
    beerid = ndb.IntegerProperty()


class BeerMenuAuditLog(ndb.Model):
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    beerid = ndb.IntegerProperty(indexed=False)
    oper = ndb.StringProperty()
    user = ndb.StringProperty()
    orig_values = ndb.StructuredProperty(BeerMenuModelforAuditLog)
    new_values = ndb.StructuredProperty(BeerMenuModelforAuditLog)


class BottleMenu(ndb.Model):
    name = ndb.StringProperty()
    brewery = ndb.StringProperty()
    origin = ndb.StringProperty()
    abv = ndb.FloatProperty(indexed=False)
    size = ndb.FloatProperty(indexed=False)
    meas = ndb.StringProperty()
    price = ndb.FloatProperty(indexed=False)
    style = ndb.StringProperty()
    active = ndb.BooleanProperty()
    url = ndb.StringProperty()

# Content Admin
class Content(ndb.Model):
    name = ndb.StringProperty()
    title = ndb.StringProperty()
    content = ndb.TextProperty()

class PageAdmin(NdbModelView):
    # form_overrides = dict(text=CKTextAreaField)
    create_template = 'content_create.html'
    edit_template = 'content_edit.html'

    # list_template = 'content_list.html'
    column_list = ('name', 'title')
    can_delete = False
    can_create = False

    # force a clear of the memached content data after any content update
    def after_model_change(self, form, model, is_created):
        content_admin.clear_content_cache()

    def is_accessible(self):
        return users.authorize_user()

    def inaccessible_callback(self, name, **kwargs):
        #redirect to login page if user doesn't have access
        return redirect(users.create_login_url())
