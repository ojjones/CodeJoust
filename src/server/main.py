import os.path
import cherrypy
from cherrypy.lib.static import serve_file
 
config = {
    '/': {
        'tools.staticdir.on' : True,
        'tools.staticdir.dir' : '/home/ojones/Programs/IsiCodeJoust/src/www',
        'tools.staticdir.index' : 'index.html',
        },
    '/setup': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Content-Type', 'text/plain')]
        }
     }

class Root():
    exposed = True

    def index(self,name):
        print name
        return serve_file(os.path.join(current_dir, name))
    index.exposed = True
 
    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return cherrypy.session['mystring']

    @cherrypy.tools.json_in()
    def POST(self, problem):
        print problem
        return 'foobahr'

    def PUT(self, another_string):
        cherrypy.session['mystring'] = another_string

    def DELETE(self):
        cherrypy.session.pop('mystring', None)

cherrypy.quickstart(Root(), '/', config=config)
