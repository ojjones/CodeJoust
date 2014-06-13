import os
import cherrypy
import json
from cherrypy.lib.static import serve_file

import random
from ws4py.websocket import WebSocket
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool

from ws4py.messaging import TextMessage
import validate
import problem

current_dir = os.path.abspath('../www')
current_games = {}

class teamHandler(WebSocket):
    def received_message(self, m):

        m = json.loads(str(m))
        print 'Hello\n'
        print m

        game_id = m['game_id']
        team_id = m['team_id']
        ty = m['type']

        if ty == 0:
            current_games[game_id][team_id]['team_session'] = self
            tmp = {'type':1,
                   'game_id':game_id,
                   'problem_id':current_games[game_id]['problem'],
                   'problem_text':"Hello World",
                   'code_session':"int main(void)"
                  }
            response = json.dumps(tmp)
            self.send(response)

        if ty == 2:
            code = m['code']

    def closed(self, code, reason="A client left the room without a proper explanation."):
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))

class scoreHandler(WebSocket):

    def received_message(self, m):

        game_id = m['game_id']
        ty = m['type']

        if type == 0:
            current_games[game_id]['scoresession'] = self

        cherrypy.engine.publish('websocket-broadcast', m)

    def closed(self, code, reason="A client left the room without a proper explanation."):
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))

config = {
    '/': {
        'tools.staticdir.on' : True,
        'tools.staticdir.dir' : current_dir,
        'tools.staticdir.index' : 'index.html',
        },
    '/problems': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        'tools.json_in.on': True,
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Content-Type', 'application/json')]
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
    '/score': {
        'tools.websocket.on': True,
        'tools.websocket.handler_cls': scoreHandler
        },
    '/join': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        'tools.json_in.on': True,
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Content-Type', 'application/json')]
        },
    '/compile': {
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

    @cherrypy.expose
    def team(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))

    @cherrypy.expose
    def score(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, vpath): # hopefully this works
        if vpath == 'problems':
             problems = problem.list_problems()
             return json.dumps(problems)

        return "Nothing here for you"

    @cherrypy.tools.json_in()
    def POST(self, vpath):
        if vpath == 'setup':
            tmpGameId = self.game_id
            self.game_id += 1
            problem = cherrypy.request.json
            current_games[tmpGameId] = {'problem':problem['problem']}
            current_games[tmpGameId]['team'] = 0
            print current_games
            return json.dumps({'game_id':tmpGameId})

        if vpath == 'compile':
            args = cherrypy.request.json
            team = args['team']
            game_id = args['game_id']
            contents = args['code']
            text_file = open(game_id + "." + team + ".c", "w")
            text_file.write(contents)
            text_file.close()

            return validate(game_id + "." + team + ".c")

        if vpath == "join":
            args = cherrypy.request.json
            game_id = int(args['game_id'])

            if game_id not in current_games:
                return json.dumps("Error: game_id " + game_id + "not found")

            team = current_games[game_id]["team"]
            current_games[game_id]["team"] = current_games[game_id]["team"] + 1

            return_val = {}
            return_val['team'] = team
            return_val['game_id'] = game_id
            return_val['problem'] = current_games[game_id]["problem"]

            return json.dumps(return_val)

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
