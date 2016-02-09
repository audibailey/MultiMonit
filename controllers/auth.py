import cherrypy

#
# The below code is adapted from:
#     http://tools.cherrypy.org/wiki/AuthenticationAndAccessRestrictions
# (not sure what the license is).
#
# The code is a CherryPy tool for authorization (e.g. to confirm that a user is logged in, before
# letting them access a page).
#
# For example, if I want to protect all of the exposed methods in a controller, I can do the
# following:
#
# from controllers.auth import is_logged_in
#
# class MyUserController(BaseController):
#
#     _cp_config = {
#         'auth.require': [is_logged_in()]
#     }
#
# It is also possible to do this for individual methods by using decorators.

SESSION_KEY = '_cp_username'


def check_auth(*args, **kwargs):
    """A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as a list of
    conditions that the user must fulfill"""
    conditions = cherrypy.request.config.get('auth.require', None)

    if conditions is None:
        return

    login_page = "/Home/Login"
    if not cherrypy.session or not cherrypy.session.get('logged_in_user'):
        raise cherrypy.HTTPRedirect(login_page)

    user_id = cherrypy.session['logged_in_user']
    if user_id:
        for condition in conditions:
            # A condition is just a callable that returns true or false
            if not condition():
                raise cherrypy.HTTPRedirect(login_page)
    else:
        raise cherrypy.HTTPRedirect(login_page)


cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth, 99)


def require(*conditions):
    """A decorator that appends conditions to the auth.require config
    variable."""

    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'auth.require' not in f._cp_config:
            f._cp_config['auth.require'] = []
        f._cp_config['auth.require'].extend(conditions)
        return f

    return decorate


# Conditions are callables that return True
# if the user fulfills the conditions they define, False otherwise
#
# They can access the current username as cherrypy.request.login
#
# Define those at will however suits the application.

def member_of(group_name):
    def check():
        if group_name == 'moderators':
            return 'logged_in_user_is_moderator' in cherrypy.session and cherrypy.session['logged_in_user_is_moderator']

    return check


def is_logged_in():
    def check():
        return cherrypy.session and 'logged_in_user' in cherrypy.session

    return check


def name_is(reqd_username):
    return lambda: reqd_username == cherrypy.request.login


# These might be handy

def any_of(*conditions):
    """Returns True if any of the conditions match"""

    def check():
        for c in conditions:
            if c():
                return True
        return False

    return check


# By default all conditions are required, but this might still be
# needed if you want to use it inside of an any_of(...) condition
def all_of(*conditions):
    """Returns True if all of the conditions match"""

    def check():
        for c in conditions:
            if not c():
                return False
        return True

    return check
