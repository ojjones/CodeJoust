import os
import cherrypy
import json
from cherrypy.lib.static import serve_file

import random
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage
 
current_dir = os.path.abspath('../www')

class ChatWebSocketHandler(WebSocket):
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
    '/ws': {
        'tools.websocket.on': True,
        'tools.websocket.handler_cls': ChatWebSocketHandler
        }
     }

class Root():
    exposed = True
    game_id = 0
    current_games = {}

    @cherrypy.expose
    def ws(self):
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
            self.current_games[tmpGameId] = {'Problem':problem['problem']}
            print self.current_games
            return json.dumps({'game_id':tmpGameId})

        return vpath

    def PUT(self, another_string):
        cherrypy.session['mystring'] = another_string

    def DELETE(self):
        cherrypy.session.pop('mystring', None)

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 9000
    })

    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.quickstart(Root(), '/', config=config)
