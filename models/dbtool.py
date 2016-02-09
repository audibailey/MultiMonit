import os
import cherrypy
from cherrypy.process import wspbus, plugins
from site_config import SiteConfig


# from models.DbHelper import DbHelper

class DbTool(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, 'on_start_resource',
                               self.bind_session,
                               priority=51)

    def _setup(self):
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach('on_end_resource',
                                      self.close,
                                      priority=80)

    def bind_session(self):
        # this is where I initialize a database connection with a connection string stored
        # in my site configuration. I then store a reference to the database object in the
        # request.
        # cherrypy.request.dbh = DbHelper(SiteConfig.conn_string)
        pass

    def close(self):
        cherrypy.request.dbh.close()
