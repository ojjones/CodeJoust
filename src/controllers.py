# vim: set tabstop=4 softtabstop=4 shiftwidth=4 expandtab
"""
Tornado request handlers
"""
import json
import logging
import traceback

import tornado.web
import tornado.websocket

import games
import validate
import spec

class BaseWebSocketHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, application, request, **kwargs):
        super(BaseWebSocketHandler, self).__init__(application, request, **kwargs)
        self.__gameid = None
        self.__handlers = {}

    @property
    def initialized(self):
        return self.__gameid is not None

    @property
    def game(self):
        return games.get_game(self.__gameid)

    @property
    def handlers(self):
        return self.__handlers

    def set_gameid(self, gameid):
        if self.initialized:
            raise Exception("Socket already initialized")
        self.__gameid = gameid

    def has_handler(self, type):
        return type in self.__handlers

    def add_handler(self, type, handler):
        self.__handlers[type] = handler

    def get_handler(self, type):
        return self.__handlers.get(type)

    def send(self, data):
        self.write_message(self.encode(data))

    def encode(self, data):
        return json.dumps(data)

    def decode(self, data):
        return json.loads(data)

    def on_message(self, message):
        try:
            message = self.decode(message)
        except:
            # ignore invalid messages
            return

        try:
            handler = self.get_handler(message["type"])
            if handler:
                handler(message["data"])
            else:
                raise Exception("Invalid message type received")
        except Exception as err:
            logging.error(err, exc_info=True)
            resp = {
                    "type": "error",
                    "data": {
                        "message": err.message
                        }
                    }
            self.send(resp)
            if self.application.settings.get("serve_traceback", False):
                resp = {
                        "type": "traceback",
                        "data": {
                            "message": traceback.format_exc()
                            }
                        }
                self.send(resp)

class BaseApiHandler(tornado.web.RequestHandler):

    def prepare(self):
        if "Content-type" in self.request.headers and \
            self.request.headers["Content-type"].startswith("application/json") and \
            len(self.request.body) > 0:
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None

    def write_json(self, data):
        self.set_header('Content-type', 'application/json')
        self.write(json.dumps(data))

class DefaultHandler(BaseApiHandler):

    def get(self):
        self.render("default.html")

class NewGameHandler(BaseApiHandler):

    def post(self):
        game = games.new_game()
        self.write_json({"gameid": game.gameid})

class JoinGameHandler(BaseApiHandler):

    def post(self):
        try:
            playerid = self.json_args["playerid"]
            gameid = self.json_args["gameid"]

            game = games.get_game(gameid)
            game.create_player(playerid)

            response = { "gameid" : game.gameid,
                         "playerid" : playerid}
            self.write_json(response)

        except games.GameNotFoundError as err:
            raise tornado.web.HTTPError(404, err.message)

class OverlordHandler(BaseApiHandler):

    def get(self, gameid):
        try:
            game = games.get_game(gameid)
            self.write("<pre>" + repr(game) + "</pre>")
        except games.GameNotFoundError as err:
            raise tornado.web.HTTPError(404, err.message)

class OverlordSocketHandler(BaseWebSocketHandler):

    def __init__(self, application, request, **kwargs):
        super(OverlordSocketHandler, self).__init__(application, request, **kwargs)
        self.__playerid = None

        self.add_handler("init_req", handle_init_req)

class PlayerHandler(BaseApiHandler):

    def get(self, gameid, playerid):
        try:
            game = games.get_game(gameid)
            self.render("game.html", game=game,
                    player=game.get_player(playerid))
        except games.GameNotFoundError as err:
            raise tornado.web.HTTPError(404, err.message)

class PlayerSocketHandler(BaseWebSocketHandler):

    def __init__(self, application, request, **kwargs):
        super(PlayerSocketHandler, self).__init__(application, request, **kwargs)
        self.__playerid = None

        self.add_handler("init_req", self.handle_init_req)

    @property
    def player(self):
        return self.game.get_player(self.__playerid)

    def set_player(self, playerid):
        if self.initialized:
            raise Exception("Socket already initialized")
        self.__playerid = playerid

    def handle_init_req(self, data):
        # try to find the game first
        gameid = str(data["gameid"])
        playerid = str(data["playerid"])
        try:
            games.get_game(gameid).get_player(playerid)
        except Exception as err:
            raise Exception("Invalid init values: %s" % err.message)

        # setup socket state
        self.set_gameid(gameid)
        self.set_playerid(playerid)

        # register socket with player object
        #TODO check if another browser is already connected
        self.player.register_websocket(self)

        game = get_game(gameid)

        # response
        resp = {
            "type": "init_res",
            "data": {spec.GAME_STATE:game.__game_state}
        }
        self.send(resp)

        #TODO register handlers here



class CompileHandler(BaseApiHandler):

    def post(self):
        playerid = self.json_args["playerid"]
        gameid = self.json_args["gameid"]
        contents = self.json_args["code"]

        #TODO ensure game has been started
        game = games.get_game(gameid)

        file_name = str(gameid) + "." + str(playerid) + ".c"
        text_file = open(file_name, "w")
        text_file.write(contents)
        text_file.close()

        current_problem = game.current_problem

        self.write_json(validate.validate(file_name, validate.CJoustProblem(current_problem)))
        #TODO Send update to game manager and viewer screen
