"""
settings.py

Configuration for Flask app

Important: Place your keys in the secret_keys.py module,
           which should be kept out of version control.

"""

import os

from secret_keys import CSRF_SECRET_KEY, SESSION_KEY, SECRET_MIGRATOR_USERNAME, SECRET_MIGRATOR_PASSWORD, SECRET_MIGRATOR_URL

# key for storing the beer id
SYSKEY = 'production'

# for util.beermenu_migrate
MIGRATOR_USERNAME = SECRET_MIGRATOR_USERNAME
MIGRATOR_PASSWORD = SECRET_MIGRATOR_PASSWORD
MIGRATOR_URL = SECRET_MIGRATOR_URL

DEBUG_MODE = False
GAEMINIPROFILER_PROFILER_ADMINS = False

# Auto-set debug mode based on App Engine dev environ
if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    DEBUG_MODE = True

DEBUG = DEBUG_MODE

# Set secret keys for CSRF protection
SECRET_KEY = CSRF_SECRET_KEY
CSRF_SESSION_KEY = SESSION_KEY

CSRF_ENABLED = True

# Flask-Cache settings
CACHE_TYPE = 'gaememcached'
