import os.path
import cherrypy
import json
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
        'tools.response_headers.headers': [('Content-Type', 'application/json')]
        }
     }

class Root():
    exposed = True
    game_id = 0
    current_games = {}

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return cherrypy.session['mystring']

    @cherrypy.tools.json_in()
    def POST(self, vpath):
        if vpath == 'setup':
            tmpGameId = self.game_id
            self.game_id += 1
            problem = cherrypy.request.json
            self.current_games[tmpGameId] = {'Problem':problem['problem']}
            print self.current_games
            return json.dumps({'game_id':tmpGameId})

        return vpath

    def PUT(self, another_string):
        cherrypy.session['mystring'] = another_string

    def DELETE(self):
        cherrypy.session.pop('mystring', None)

cherrypy.quickstart(Root(), '/', config=config)
