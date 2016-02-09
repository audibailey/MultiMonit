import inspect
import cherrypy
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from controllers.jinjahelper import JinjaHelper
from models.loghelper import Logger


class BaseController:
    def render_template(self, path, template_vars=None):
        template_vars = template_vars if template_vars else {}
        try:
            session = cherrypy.session

            # set variables in the page so you know whether or not a user is logged in. I
            # use this because I have different menus defined in the layout, and a user
            # will see a different menu when they're logged in. This code is optional;
            # remove it if you have different code for handling sessions.
            template_vars['logged_in'] = '0'
            template_vars['isUserLoggedIn'] = False
            if session:
                if 'logged_in_user' in session and session['logged_in_user'] is not None:
                    template_vars['isUserLoggedIn'] = True
                    template_vars['logged_in'] = '1'
                    template_vars['logged_in_user'] = session['logged_in_user']
                    template_vars['logged_in_username'] = session['logged_in_username']

            # set our base path for loading templates, and load the template view file
            jh = JinjaHelper(cherrypy.site['base_path'])
            tpl = jh.get_template(path)

            if not tpl:
                Logger.error('Error rendering template: ' + path, None, True)

            return tpl.render(template_vars)
        except Exception as ex:
            Logger.error('Error rendering template', ex, True)
