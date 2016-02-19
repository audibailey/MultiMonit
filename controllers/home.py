# Import Required Libraries
import cherrypy
from controllers.base import BaseController
from models import Config, Parsing


class HomeController(BaseController):
    # CherryPy load the Index Page (Setup)
    @cherrypy.expose
    def index(self):
        config = Config.readconfig()
        # Check if there is a config.
        if config != 0:
            # Else redirect the User to the Dashboard
            raise cherrypy.HTTPRedirect("Home/dash")
        else:
            # If True Return the template
            return self.render_template('home/index.html')


    # CherryPy load the Dashboard Page
    @cherrypy.expose
    def dash(self, **params):
        config = Config.readconfig()
        # Attempts to read the config.
        if config == 0:
            # Else it uses the Arguements to create a config.
            data = {str(key):str(value) for key,value in params.items()}
            url = []
            for i, v in data.items():
                url.append(v)
            Config.mkconfig(url)
        else:
            # If True it saves the data to a variable
            URLS = config["URLS"]
            refresh = config["refresh"]

        # Runs the script in the Parsing Model. Parses the XML Files from URL
        parse = Parsing.system()
        refresh = config["refresh"]


        # Returns the template with Parsed XML Data and The Refresh Integer from the Config.
        return self.render_template('home/dash.html', template_vars={'data': parse, 'refresh': refresh})

    # CherryPy load the Settings Page
    @cherrypy.expose
    def settings(self):
        config = Config.readconfig()
        URLS = config["URLS"]
        refresh = config["refresh"]
        # Return the template
        return self.render_template('home/settings.html', template_vars={'refresh': refresh, 'urls': URLS})

    # CherryPy load the Confimed Settings Page
    @cherrypy.expose
    def confirmed(self, **params):
        url = []
        for k, v in params.items():
            if k != "refresh":
                url = v
            else:
                refresh = v

        Config.updateconfig(url, refresh)
        # Return the template
        # return self.render_template('home/confirmed.html')
        raise cherrypy.HTTPRedirect("dash")
