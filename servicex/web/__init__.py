from flask import current_app as app

from .home import home
from .sign_in import sign_in
from .sign_out import sign_out
from .auth_callback import auth_callback
from .api_token import api_token
from .create_profile import create_profile
from .view_profile import view_profile
from .edit_profile import edit_profile


def add_web_routes():
    # Web Frontend Routes
    app.add_url_rule('/', 'home', home)
    app.add_url_rule('/sign-in', 'sign_in', sign_in)
    app.add_url_rule('/sign-out', 'sign_out', sign_out)
    app.add_url_rule('/auth-callback', 'auth_callback', auth_callback)
    app.add_url_rule('/api-token', 'api_token', api_token)
    app.add_url_rule('/profile', 'profile', view_profile)
    app.add_url_rule('/profile/new', 'create_profile', create_profile,
                     methods=['GET', 'POST'])
    app.add_url_rule('/profile/edit', 'edit_profile', edit_profile,
                     methods=['GET', 'POST'])
