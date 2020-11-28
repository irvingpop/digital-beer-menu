"""
Initialize Flask app

"""
from flask import Flask
from .config import Config
from google.cloud import ndb
from flask_dance.contrib.google import make_google_blueprint

app = Flask('application')

# google.cloud.ndb initialization
ndbclient = ndb.Client()


def ndb_wsgi_middleware(wsgi_app):
    def middleware(environ, start_response):
        with ndbclient.context():
            return wsgi_app(environ, start_response)

    return middleware


app.wsgi_app = ndb_wsgi_middleware(app.wsgi_app)  # Wrap the app in middleware.

# Flask Config
app.config.from_object(Config)
app.jinja_options = dict(extensions=['jinja2.ext.loopcontrols'])

# Flask-Dance (google auth) initialization
google_bp = make_google_blueprint(scope=[
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
])
app.register_blueprint(google_bp, url_prefix="/login")

# someday I'll be good enough at Python to understand why this needs to go
# at the bottom
import application.urls    # noqa
