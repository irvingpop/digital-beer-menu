"""
urls.py

URL dispatch route mappings and error handlers

"""

from flask import render_template

from application import app
from application import views

from google.appengine.api import users
login_url = users.create_login_url()
logout_url = users.create_logout_url('/')

# Content admin
import content_admin


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

# Home page
app.add_url_rule('/', 'home', view_func=views.home)

# Public Menu page
app.add_url_rule('/menu', 'menu', view_func=views.menu)
app.add_url_rule('/menu/', 'menu', view_func=views.menu)

# FAQ
app.add_url_rule('/faq', 'faq', view_func=views.faq)

# Bar menu
app.add_url_rule('/barmenu', 'barmenu', view_func=views.barmenu)

# Admin site
app.add_url_rule('/admin', 'admin', view_func=views.admin)
app.add_url_rule('/admin/data', 'admin_data',  methods=['GET', 'POST'], view_func=views.admin_data)
app.add_url_rule('/admin/edit', 'admin_edit',  methods=['GET', 'POST'], view_func=views.admin_edit)

# Bottle Menu
app.add_url_rule('/admin/bottlemenu', 'admin_bottlemenu', view_func=views.admin_bottlemenu)
app.add_url_rule('/admin/bottlemenu_data', 'admin_data_bottlemenu',  methods=['GET', 'POST'], view_func=views.admin_data_bottlemenu)
app.add_url_rule('/admin/bottlemenu_edit', 'admin_edit_bottlemenu',  methods=['GET', 'POST'], view_func=views.admin_edit_bottlemenu)
app.add_url_rule('/bottlemenu', 'bottlemenu', view_func=views.bottlemenu)

# super admin stuff
app.add_url_rule('/admin/linestatus', 'admin_linestatus', view_func=views.admin_linestatus)
app.add_url_rule('/admin/auditlog', 'admin_auditlog', view_func=views.admin_auditlog)

## Error handlers
# Handle 404 errors
#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('404.html'), 404
#
## Handle 500 errors
#@app.errorhandler(500)
#def server_error(e):
#    return render_template('500.html'), 500


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(410)
@app.errorhandler(418)
@app.errorhandler(500)
def error_handler(e):
    user = users.get_current_user()
    try:
        e.code
    except:
        class e(object):
            code = 500
            name = 'Internal Server Error'

    return render_template(
        'error.html',
        title='%s!!1' % (e.name),
        html_class='error-page',
        error=e,
        user=user, login_url=login_url, logout_url=logout_url,
    ), e.code
