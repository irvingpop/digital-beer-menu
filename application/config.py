"""
settings.py

Configuration for Flask app

Important: Place your keys in the secret_keys.py module,
           which should be kept out of version control.

"""

import os


class Config(object):
    # key for storing the beer id
    SYSKEY = 'production'

    # Set secret keys for CSRF protection
    SECRET_KEY = os.environ.get("CSRF_SECRET_KEY")
    CSRF_SESSION_KEY = os.environ.get("SESSION_KEY")
    CSRF_ENABLED = True

    # flask-dance
    secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
    GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
