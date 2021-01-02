from google.cloud import ndb
import sys
import os
import ipdb

# for vendored libraries, living in lib
sys.path.append(os.path.join(os.path.abspath('.'), 'lib'))

from application import models

ndbclient = ndb.Client()


# now do shit like:

# ex: set all inactive bottles to active
# with ndbclient.context():
#   bottlemenu = models.BottleMenu.query(models.BottleMenu.active == False).fetch()
#   for bottle in bottlemenu:
#     bottle.active = True
#     bottle.put()

ipdb.set_trace()
