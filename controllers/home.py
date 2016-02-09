# Import Required Libraries
import cherrypy
from controllers.base import BaseController
from models import Config, Parsing


class HomeController(BaseController):
    # CherryPy load the Index Page (Setup)
    @cherrypy.expose
    def index(self):
        # Check if there is a config.
        if Config.readConfig() == []:
            # If True Return the template
            return self.render_template('home/index.html')
        else:
            # Else redirect the User to the Dashboard
            raise cherrypy.HTTPRedirect("Home/dash")

    # CherryPy load the Dashboard Page
    @cherrypy.expose
    def dash(self, **params):
        # Attempts to read the config.
        if Config.readConfig():
            # If True it saves the data to a variable
            URLS = Config.readConfig()
            refresh = Config.readConfigRefresh()
        else:
            # Else it uses the Arguements to create a config.
            Config.mkfile(params)
            URLS = Config.readConfig()
        # Checks if the config file was success fule
        if URLS:
            # Runs the script in the Parsing Model. Parses the XML Files from URL
            parse = Parsing.system()

        # Returns the template with Parsed XML Data and The Refresh Integer from the Config.
        return self.render_template('home/dash.html', template_vars={'data': parse, 'refresh': refresh})

    # CherryPy load the Settings Page
    @cherrypy.expose
    def settings(self):
        URLS = Config.readConfig()
        refresh = Config.readConfigRefresh()
        # Return the template
        return self.render_template('home/settings.html', template_vars={'refresh': refresh, 'urls': URLS})

    # CherryPy load the Confimed Settings Page
    @cherrypy.expose
    def confirmed(self, **params):
        # Update the config
        print params
        Config.updateConfig()
        # Return the template
        # return self.render_template('home/confirmed.html')
        raise cherrypy.HTTPRedirect("Home/dash")
