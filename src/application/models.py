# -*- coding: utf-8 -*-
"""
models.py

App Engine datastore models

"""
from google.appengine.ext import ndb


class BeerMenu(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    brewery = ndb.StringProperty(indexed=False)
    origin = ndb.StringProperty(indexed=False)
    abv = ndb.FloatProperty(indexed=False)
    size = ndb.FloatProperty(indexed=False)
    meas = ndb.StringProperty(indexed=False)
    price = ndb.FloatProperty(indexed=False)
    active = ndb.BooleanProperty()
    url = ndb.StringProperty(indexed=False)
    bartender = ndb.StringProperty(indexed=False)
    lineno = ndb.IntegerProperty(indexed=False)
    purdate = ndb.DateProperty(indexed=False)
    costper = ndb.FloatProperty(indexed=False)


class BeerMenuModelforAuditLog(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    brewery = ndb.StringProperty(indexed=False)
    origin = ndb.StringProperty(indexed=False)
    abv = ndb.FloatProperty(indexed=False)
    size = ndb.FloatProperty(indexed=False)
    meas = ndb.StringProperty(indexed=False)
    price = ndb.FloatProperty(indexed=False)
    active = ndb.BooleanProperty()
    url = ndb.StringProperty(indexed=False)
    bartender = ndb.StringProperty(indexed=False)
    lineno = ndb.IntegerProperty(indexed=True)
    purdate = ndb.DateProperty(indexed=False)
    costper = ndb.FloatProperty(indexed=False)


class FreshestBeer(ndb.Model):
    beerid = ndb.IntegerProperty()


class BeerMenuAuditLog(ndb.Model):
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    beerid = ndb.IntegerProperty(indexed=False)
    oper = ndb.StringProperty(indexed=False)
    user = ndb.UserProperty(indexed=False)
    orig_values = ndb.StructuredProperty(BeerMenuModelforAuditLog)
    new_values = ndb.StructuredProperty(BeerMenuModelforAuditLog)


class BottleMenu(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    brewery = ndb.StringProperty(indexed=False)
    origin = ndb.StringProperty(indexed=False)
    abv = ndb.FloatProperty(indexed=False)
    size = ndb.FloatProperty(indexed=False)
    meas = ndb.StringProperty(indexed=False)
    price = ndb.FloatProperty(indexed=False)
    style = ndb.StringProperty(indexed=False)
    active = ndb.BooleanProperty()
    url = ndb.StringProperty(indexed=False)
