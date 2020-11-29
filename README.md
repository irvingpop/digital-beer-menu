Digital Beer Menu project
====================================

This project uses Google App Engine's Python 3 Standard Environment for hosting.

It's awesome because it is virtually free (costs pennies per month at most), ridiculously reliable, and super secure.

# Dev Notes

## Running in local dev
1. Install and configure the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
1. Run `poetry install`  (Note: you must install https://python-poetry.org/ first)
1. run the gcloud datastore emulator locally and instruct your app to use it:
    ```
    gcloud beta emulators datastore start &
    $(gcloud beta emulators datastore env-init)
    ```
1. Configure secrets in a `.flaskenv` file - see `.flaskenv.example`
1. Run the app:
    ```
    poetry run python3 run.py
    ```

# Deploying
1. Configure secrets in a `env-production.yaml` file - see `env-production.yaml.example`
1. `gcloud app deploy` to deploy
1. Configure OAuth credentials: https://console.developers.google.com/apis/credentials

# Migrating data from another beermenu project
1. Export data using the [Entities Export](https://console.cloud.google.com/datastore/entities/export) feature in the gcloud datastore UI
1. Download them to your machine
    ```
    gsutil -m cp -r gs://bucket/datestamp .
    ```
1. Import them to the datastore
    ```
    curl -X POST localhost:8081/v1/projects/beermenu-v3:import \
      -H 'Content-Type: application/json' \
      -d '{"input_url":"/Users/irving/Downloads/beermenu-backup-2020-11-29/2020-11-29T01:55:10_56249.overall_export_metadata"}'
    ```

You can also move backups between projects by downloading the export to your local machine, and then uploading them to a bucket in another project and importing.


Credits
-------

kamalgill's [gae-init project](https://github.com/gae-init/gae-init)

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
