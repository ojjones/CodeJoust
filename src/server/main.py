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

TEAM_INIT_REQ = 0;
TEAM_INIT_RES = 1;
TEAM_CODE_UPDATE = 2;
SCORE_SCREEN_UPDATE = 3;
SCORE_INIT = 4;
START_ID = 5;
STOP_ID = 6;
WINNER_ID = 7;
DRINK_ID = 8;

class teamHandler(WebSocket):
    def received_message(self, m):

        m = json.loads(str(m))

        game_id = m['game_id']
        team_id = m['team_id']
        ty = m['type']

        if ty == TEAM_INIT_REQ:
            description, template = problem.get_problem(current_games[game_id]['problem'])
            if  "code_session" in current_games[game_id]['teams'][team_id]:
                code = current_games[game_id]['teams'][team_id]["code_session"]
            else:
                code = template;
            tmp = {'type':TEAM_INIT_RES,
                   'game_id':game_id,
                   'problem_id':current_games[game_id]['problem'],
                   'problem_text': description,
                   'code_session': code
                  }
            response = json.dumps(tmp)
            self.send(response)
            current_games[game_id]['teams'][team_id]['team_session'] = self

        if ty == TEAM_CODE_UPDATE:
            code = m['code']
            current_games[game_id]['teams'][team_id]["code_session"] = code
            tmp = {'type':SCORE_SCREEN_UPDATE,
                   'team_id':team_id,
                   'code':code
                  }
            if "scoresession" in current_games[game_id]:
                print code
                msg = json.dumps(tmp)
                current_games[game_id]['scoresession'].send(msg)


    def closed(self, code, reason="A client left the room without a proper explanation."):
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))

class scoreHandler(WebSocket):

    def received_message(self, m):

        m = json.loads(str(m))

        game_id = m['game_id']
        ty = m['type']

        if ty == SCORE_INIT:
            current_games[game_id]['scoresession'] = self
            if "code_session" in current_games[game_id]["teams"][0]:
                tmp = {'type':SCORE_SCREEN_UPDATE,
                       'team_id':0,
                       'code':current_games[game_id]['teams'][0]["code_session"]
                      }
                msg = json.dumps(tmp)
                self.send(msg)
            if "code_session" in current_games[game_id]["teams"][1]:
                tmp = {'type':SCORE_SCREEN_UPDATE,
                       'team_id':1,
                       'code':current_games[game_id]['teams'][1]["code_session"]
                       }
                msg = json.dumps(tmp)
                self.send(msg)

        cherrypy.engine.publish('websocket-broadcast', m)

    def closed(self, code, reason="A client left the room without a proper explanation."):
        for i in current_games:
            if current_games[i]['scoresession'] == self:
                del current_games[i]['scoresession']

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
        },
    '/team': {
        'tools.websocket.on': True,
        'tools.websocket.handler_cls': teamHandler
        },
    '/score': {
        'tools.websocket.on': True,
        'tools.websocket.handler_cls': scoreHandler
        },
    '/start': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        'tools.json_in.on': True,
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Content-Type', 'application/json')]
        },
    '/stop': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        'tools.json_in.on': True,
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Content-Type', 'application/json')]
        },
    '/drink': {
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
            print problems
            return json.dumps(problems)

        return "Nothing here for you"

    @cherrypy.tools.json_in()
    def POST(self, vpath):
        if vpath == 'setup':
            tmpGameId = self.game_id
            self.game_id += 1
            _problem = cherrypy.request.json
            current_games[tmpGameId] = {'problem':_problem['problem']}
            current_games[tmpGameId]['teams'] = []
            current_games[tmpGameId]['teams'].append({})
            current_games[tmpGameId]['teams'].append({})
            print current_games
            return json.dumps({'game_id':tmpGameId})

        if vpath == 'compile':
            args = cherrypy.request.json
            team = args['team']
            game_id = args['game_id']
            contents = args['code']
            text_file = open(str(game_id) + "." + str(team) + ".c", "w")
            text_file.write(contents)
            text_file.close()

            return json.dumps(validate.validate(str(game_id) + "." + str(team) + ".c", problem.CJoustProblem(current_games[game_id]["problem"])))

        if vpath == "join":
            args = cherrypy.request.json
            game_id = int(args['game_id'])

            if game_id not in current_games:
                return json.dumps("Error: game_id " + game_id + "not found")

            if 'enabled' not in current_games[game_id]['teams'][0]:
                team = 0
                current_games[game_id]['teams'][0]['enabled'] = 1
            elif 'enabled' not in current_games[game_id]['teams'][1]:
                team = 1
                current_games[game_id]['teams'][1]['enabled'] = 1
            else:
                team = -1

            return_val = {}
            return_val['team'] = team
            return_val['game_id'] = game_id
            return_val['problem'] = current_games[game_id]["problem"]

            return json.dumps(return_val)

        if vpath == 'start':
            args = cherrypy.request.json
            game_id = int(args['game_id'])

            tmp = {'type':START_ID}
            msg = json.dumps(tmp)
            if 'team_session' in current_games[game_id]['teams'][0]:
                current_games[game_id]['teams'][0]['team_session'].send(msg)
            if 'team_session' in current_games[game_id]['teams'][1]:
                current_games[game_id]['teams'][1]['team_session'].send(msg)
            
        if vpath == 'stop':
            args = cherrypy.request.json
            game_id = int(args['game_id'])

            tmp = {'type':STOP_ID}
            msg = json.dumps(tmp)
            if 'team_session' in current_games[game_id]['teams'][0]:
                current_games[game_id]['teams'][0]['team_session'].send(msg)
            if 'team_session' in current_games[game_id]['teams'][1]:
                current_games[game_id]['teams'][1]['team_session'].send(msg)

        return vpath

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080
    })

    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.quickstart(Root(), '/', config=config)
