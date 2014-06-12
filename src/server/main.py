import os.path
import cherrypy
from cherrypy.lib.static import serve_file
 
current_dir = os.path.abspath('../www')

config = {
    '/': {
        'tools.staticdir.on' : True,
        'tools.staticdir.dir' : current_dir,
        'tools.staticdir.index' : 'index.html',
        },
    '/setup': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        'tools.json_in.on': True,
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Content-Type', 'text/plain')]
        }
     }

class Root():
    exposed = True

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return cherrypy.session['mystring']

    @cherrypy.tools.json_in()
    def POST(self, problem):
        test = cherrypy.request.json
        print test
        return test

    def PUT(self, another_string):
        cherrypy.session['mystring'] = another_string

    def DELETE(self):
        cherrypy.session.pop('mystring', None)

cherrypy.quickstart(Root(), '/', config=config)
