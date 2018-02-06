# -*- coding: utf-8 -*-
"""
content_admin.py

Content Admin tools via flask_admin

"""
from flask import render_template, flash, url_for, redirect, request, jsonify, Response
from application import app
from google.appengine.ext import ndb
from google.appengine.api import users
import flask_admin
from flask_admin.contrib import appengine
from wtforms import fields, widgets
from wtforms_appengine.ndb import ModelConverter

# caching
from flask.ext.cache import Cache
cache = Cache(with_jinja2_ext=False)
cache.init_app(app, config={'CACHE_TYPE': 'gaememcached'})

class Content(ndb.Model):
    name = ndb.StringProperty()
    title = ndb.StringProperty(indexed=False)
    content = ndb.TextProperty(indexed=False)

class PageAdmin(appengine.view.NdbModelView):
    # form_overrides = dict(text=CKTextAreaField)
    create_template = 'content_create.html'
    edit_template = 'content_edit.html'
    # list_template = 'content_list.html'
    column_list = ('name', 'title')
    can_delete = False
    can_create = False
    # force a clear of the memached content data after any content update
    def after_model_change(self, form, model, is_created):
        clear_content_cache()
    def is_accessible(self):
        return users.is_current_user_admin()
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(users.create_login_url(request.url))

# Content Management stuff via flask_admin
content_admin = flask_admin.Admin(app, name="Content Admin", url='/content_admin')
content_admin.add_view(PageAdmin(Content))

# Load defaults
EXPECTED_CONTENT_ITEMS = ["info_left", "info_right", "faq"]

# Only expected to run during the first startup, maybe warmup isn't the right place to call this from but that's what I got
def check_sane_defaults():
    for item in EXPECTED_CONTENT_ITEMS:
        content_items = Content.query(Content.name == item).get()
        if content_items is None:
            new_item = Content()
            new_item.name = item
            new_item.title = "Default"
            new_item.content = "<p>Put some stuff here</p>"
            new_item.put()

    clear_content_cache()

    return True

# return a dict of all the contents in one shot, so they're cached together
@cache.memoize()
def get_content_cache():
    contents = {}
    for row in Content.query():
      rd = row.to_dict()
      contents[rd['name']] = rd

    return contents

def clear_content_cache():
    cache.delete_memoized(get_content_cache)
    return True
