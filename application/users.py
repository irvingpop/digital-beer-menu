from functools import wraps
from flask import redirect, abort, url_for, session
from flask_dance.contrib.google import google

ADMINS = [
    "irving@popovetsky.com",
    "jesse@apexbar.com",
    "sheriff@apexbar.com",
    "staff@apexbar.com"
]


def login_required(func):
    """Requires standard login credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not google.authorized:
            return redirect(url_for('google.login'))
        if not authorize_user():
            abort(401)
        return func(*args, **kwargs)
    return decorated_view


def get_current_user():
    if google.authorized:
        if '_user_id' in session:
            return session['_user_id']
        else:
            resp = google.get("/oauth2/v1/userinfo")
            assert resp.ok, resp.text
            email = resp.json()["email"]
            session['_user_id'] = email
            return email
    else:
        return None


def create_login_url():
    return url_for('google.login')


def create_logout_url():
    return url_for('google.logout')


def authorize_user():
    current_user = get_current_user()
    if current_user in ADMINS:
        return True
    return False


def template_auth_params():
    current_user = {}
    current_user["id"] = get_current_user()
    current_user["is_authorized"] = authorize_user()
    current_user["login_url"] = create_login_url()
    current_user["logout_url"] = "/logout"
    return current_user


def logout():
    if '_user_id' in session:
        session.pop('_user_id')
    if 'google_oauth_token' in session:
        session.pop('google_oauth_token')
    return redirect("/")
