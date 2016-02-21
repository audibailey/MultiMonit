import cherrypy
import os
from controllers.home import *
from site_config import SiteConfig
from controllers.auth import require, member_of, name_is
from models.loghelper import Logger
from models.logger import logs
from models.dbtool import DbTool


# this method returns HTML when a 404 (page not found error) is encountered.
# You'll probably want to return custom HTML using Jinja2.
def error_page_404(status, message, traceback, version):
    a = cherrypy.request
    b = cherrypy.url()
    return "404 Error!"


# this returns an HTML error message when an exception is thrown in your code in production.
# This to avoid showing a stack trace with sensitive information.
def handle_error():
    cherrypy.response.status = 500
    cherrypy.response.body = [
        """
            <html>

                <body>

                    <h1> Error 500. Sorry, an error occurred. </h1>
                    <p> This is an internal error in relation to either the URL you used or a bug in the code. </p>
                    <p> Try changing the URL in the settings to fix the error.</p>
                    <a href="settings">Settings</a>
                    </br>
                    <p> For more information check the log.txt in the install directory</p>
                    <p> Please post an issue at <a href="https://github.com/desgyz/MultiMonit">GitHub</a> if the error persists</p>

                </body>
            </html>
        """.encode()
    ]

# Set the controller
class RootController:
    @cherrypy.expose
    def index(self, *args, **kwargs):
        c = HomeController()
        return c.index()

# function to start server
def start_server():

    # organise base path
    cherrypy.site = {
        'base_path': os.getcwd()
    }

    # make sure the directory for storing session files exists
    session_dir = cherrypy.site['base_path'] + "/sessions"
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)

    # set default password for basic auth
    userpassdict = {'admin' : 'password'}
    checkpassword = cherrypy.lib.auth_basic.checkpassword_dict(userpassdict)

    # this is where I initialize a custom tool for connecting to the database, once for each
    # request. Edit models/dbtool.py and uncomment the tools.db lines below to use this.
    # cherrypy.tools.db = DbTool()

    ##################################################################
    #                                                                #
    #                       CONFIG SECTION                           #
    #                                                                #
    ##################################################################
    server_config = {
        # This tells CherryPy what host and port to run the site on (e.g. localhost:3005/)
        # Feel free to set this to whatever you'd like.
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 3005,

        'error_page.404': error_page_404,
        'engine.autoreload.on': False,

        # this indicates that we want file-based sessions (not stored in RAM, which is the default)
        # the advantage of this is that you can stop/start CherryPy and your sessions will continue
        'tools.sessions.on': True,
        'tools.sessions.storage_type': "file",
        'tools.sessions.storage_path': session_dir,
        'tools.sessions.timeout': 180,

        # this is a custom tool for handling authorization (see auth.py)
        'tools.auth.on': False,
        'tools.auth.priority': 52,
        'tools.sessions.locking': 'early',

        # uncomment the below line to use the tool written to connect to the database
        # 'tools.db.on': True

        # basic auth settings
        'tools.auth_basic.on': True,
        'tools.auth_basic.realm': 'Default username: admin, Default password: password',
        'tools.auth_basic.checkpassword': checkpassword,
    }
    ##################################################################
    #                                                                #
    #                    END CONFIG SECTION                          #
    #                                                                #
    ##################################################################

    # error handling
    server_config['request.error_response'] = handle_error

    # update server config
    cherrypy.config.update(server_config)

    # this will let us access localhost:3005/Home or localhost:3005/Home/Index
    cherrypy.tree.mount(HomeController(), '/Home')

    # this will map localhost:3005/
    cherrypy.tree.mount(RootController(), '/', {
        '/': {
            'tools.staticdir.root': os.getcwd()
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static',

            # we don't need to initialize the database for static files served by CherryPy
            # 'tools.db.on': False
        }
    })


    # if you're using a separate WSGI server (e.g. Nginx + uWsgi) in prod, then let CherryPy know
    if SiteConfig.is_prod:
        cherrypy.server.unsubscribe()

    # failed attempt of Ctrl + C signal handler, will be deprecated
    if hasattr(cherrypy.engine, 'signal_handler'):
        cherrypy.engine.signal_handler.subscribe()

    # start the web server
    cherrypy.engine.start()

    # start logging
    logs.logall()

    # a little hint to kill the program
    print "Please use Ctrl + \\ to kill the program or use PID kill"

    # this return value is used by the WSGI server in prod
    return cherrypy.tree

# start the application, includes a basic error handle
try:
    application = start_server()
except Exception as ex:
    Logger.error('Error during run', ex)
