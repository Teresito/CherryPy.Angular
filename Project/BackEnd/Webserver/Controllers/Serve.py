import cherrypy

# Serving the main page
class Web_Page(object):

    @cherrypy.expose
    def default(self, *args, **kwargs):
        return Web_Page.index(self)

    @cherrypy.expose
    def index(self):
        return open('./bundled/index.html')