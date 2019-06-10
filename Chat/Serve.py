import cherrypy

# Serving the main page
class Web_Page(object):

    # All redirects are back to index HTML
    @cherrypy.expose
    def default(self, *args, **kwargs):
        return Web_Page.index(self)
    # Serves the client the index HTML
    @cherrypy.expose
    def index(self):
        return open('./Bundled/index.html')