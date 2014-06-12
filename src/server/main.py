import os
import cherrypy
import json
from cherrypy.lib.static import serve_file

import random
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage
 
current_dir = os.path.abspath('../www')
current_games = {}

class teamHandler(WebSocket):
    def received_message(self, m):

        m = json.loads(str(m))

        game_id = m['game_id']

        tmp = {'type':1,
               'game_id':game_id,
               'problem_id':current_games[game_id]['problem'],
               'problem_text':"Hello World",
               'code_session':"int main(void)"
              }
        response = json.dumps(tmp)
        self.send(response)

    def closed(self, code, reason="A client left the room without a proper explanation."):
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))

class screenHandler(WebSocket):
    def received_message(self, m):
        cherrypy.engine.publish('websocket-broadcast', m)

    def closed(self, code, reason="A client left the room without a proper explanation."):
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))

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
        },
    '/team': {
        'tools.websocket.on': True,
        'tools.websocket.handler_cls': teamHandler
        },
    '/screen': {
        'tools.websocket.on': True,
        'tools.websocket.handler_cls': screenHandler
        }
     }

class Root():
    exposed = True
    game_id = 0

    @cherrypy.expose
    def team(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))

    @cherrypy.expose
    def screen(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return cherrypy.session['mystring']

    @cherrypy.tools.json_in()
    def POST(self, vpath):
        if vpath == 'setup':
            tmpGameId = self.game_id
            self.game_id += 1
            problem = cherrypy.request.json
            current_games[tmpGameId] = {'problem':problem['problem']}
            print current_games
            return json.dumps({'game_id':tmpGameId})

        return vpath

    def PUT(self, another_string):
        cherrypy.session['mystring'] = another_string

    def DELETE(self):
        cherrypy.session.pop('mystring', None)

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080
    })

    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.quickstart(Root(), '/', config=config)
