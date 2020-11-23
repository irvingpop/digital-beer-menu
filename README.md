Digital Beer Menu project
====================================

This project uses Google App Engine's Python 3 Standard Environment for hosting.

It's awesome because it is virtually free (costs pennies per month at most), ridiculously reliable, and super secure.

# Dev Notes

## Running in local dev
1. Install gcloud
1. `poetry install`  (Note: you must install https://python-poetry.org/ first)
1. run the gcloud datastore emulator locally: `gcloud beta emulators datastore start`
1. Instruct your app to use the datastore emulator: `$(gcloud beta emulators datastore env-init)`
1. Configure secrets in a `.flaskenv` file - see `.flaskenv.example`
1. Run the app: poetry run python3 run.py

# Deploying
1. Configure secrets in a `env-production.yaml` file - see `env-production.yaml.example`
1. `gcloud app deploy` to deploy
1. Configure OAuth credentials: https://console.developers.google.com/apis/credentials

# Migrating data from another beermenu project
1. ??



Credits
-------
kamalgill's gae-init project

Project template layout was heavily inspired by Francisco Souza's
[gaeseries Flask project][gaeseries]

Incorporates [Flask-DebugToolbar][debugtoolbar] by Matt Good et. al.
and [Flask-Cache][flaskcache] by Thadeus Burgess

Layout, form, table, and button styles provided by [Bootstrap][bootstrap]

[Font Awesome][fontawesome] by Dave Gandy

HTML5 detection provided by [Modernizr 2][modernizr] (configured with all features)


[appcfg]: http://code.google.com/appengine/docs/python/tools/uploadinganapp.html
[bootstrap]: http://twitter.github.com/bootstrap
[debugtoolbar]: https://readthedocs.org/projects/flask-debugtoolbar/
[devserver]: http://code.google.com/appengine/docs/python/tools/devserver.html
[flask]: http://flask.pocoo.org
[flaskcache]: http://pythonhosted.org/Flask-Cache/
[fontawesome]: http://fortawesome.github.com/Font-Awesome/
[html5]: http://html5boilerplate.com/
[jinja2]: http://jinja.pocoo.org/2/documentation/
[gaeseries]: http://github.com/franciscosouza/gaeseries/tree/flask
[modernizr]: http://www.modernizr.com/
[profiler]: http://packages.python.org/Flask-GAE-Mini-Profiler/
[wz]: http://werkzeug.pocoo.org/
[wzda]: https://github.com/nshah/werkzeug-debugger-appengine
