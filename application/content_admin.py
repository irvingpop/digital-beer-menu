# -*- coding: utf-8 -*-
"""
content_admin.py

Content Admin tools via flask_admin

"""
from application import app, models
from google.cloud import ndb
from flask_admin import Admin
from flask_caching import Cache

cache = Cache(with_jinja2_ext=False)
cache.init_app(app, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': '/tmp'})

# Load defaults
EXPECTED_CONTENT_ITEMS = ["info_left", "info_right", "faq"]

# Content Management stuff via flask_admin
content_admin = Admin(app, name="Content Admin", url='/content_admin', template_mode='bootstrap2')
content_admin.add_view(models.PageAdmin(models.Content))

# Only expected to run during the first startup, maybe warmup isn't the right place to call this from but that's what I got
def check_sane_defaults():
    for item in EXPECTED_CONTENT_ITEMS:
        content_items = models.Content.query(models.Content.name == item).get()
        if content_items is None:
            new_item = models.Content()
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
    for row in models.Content.query():
      rd = row.to_dict()
      contents[rd['name']] = rd

    return contents

def clear_content_cache():
    cache.delete_memoized(get_content_cache)
    return True
