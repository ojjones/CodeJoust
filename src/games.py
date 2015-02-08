# vim: set tabstop=4 softtabstop=4 shiftwidth=4 expandtab
"""
Game Session Management
"""
import time

NEXT_GAMEID = 1
GAMES = {}


class GameNotFoundError(Exception):
    """
    Error raised when a game does not exist
    """
    def __init__(self, gameid):
        super(GameNotFoundError, self).__init__("Game '%s' not found." % gameid)
        self.__gameid = gameid

    @property
    def gameid(self):
        return self.__gameid

class WebSocketProxy(object):

    def __init__(self):
        self.__ws = None

    @property
    def connected(self):
        return self.__ws is not None

    def register_websocket(self, ws):
        self.__ws = ws

    def unregister_websocket(self):
        self.__ws = None

    def send(self, msg):
        if self.connected:
            self.__ws.send(msg)

class Player(WebSocketProxy):

    def __init__(self, playerid):
        super(Player, self).__init__()
        self.__playerid = playerid

    @property
    def playerid(self):
        return self.__playerid

class ScoreScreen(WebSocketProxy):

    def __init__(self, playerid):
        super(ScoreScreen, self).__init__()

class Game(WebSocketProxy):

    #GAME STATE
    STOP = "STOP"
    START = "START"
    PAUSE = "PAUSE"
    GAME_OVER = "GAME_OVER"

    def __init__(self, gameid):
        self.__gameid = gameid
        self.__created = time.time()
        self.__current_problem = None
        self.__game_state = self.STOP

        # init players
        self.__players = {}

        # init scorescreen
        self.__scorescreen = None

    def __repr__(self):
        output = "GameID: %s" % (self.gameid)
        return output

    @property
    def gameid(self):
        return self.__gameid

    @property
    def created(self):
        return self.__created

    @property
    def created_str(self):
        return time.ctime(self.created)

    @property
    def current_problem(self):
        return self.__current_problem

    def create_player(self, playerid):
        self.__players[playerid] = Player(playerid)

    @property
    def score_screen(self):
        return self.__scorescreen

    def create_score_screen(self):
        self.__score = ScoreScreen()

    def broadcast(self, msg):
        self.send(msg)
        for player in self.list_players():
            player.send(msg)

    def set_current_problem(self, problem):
        self.__current_problem = problem

    def get_player(self, playerid, throw=True):
        try:
            player = None
            player = self.__players[playerid]
        except:
            if throw:
                raise Exception("Invalid player ID")
        return player

    def list_players(self):
        return [player for player in self.__players.itervalues()]

def new_game():
    global NEXT_GAMEID
    gameid = str(NEXT_GAMEID)
    NEXT_GAMEID += 1
    GAMES[gameid] = Game(gameid)
    return GAMES[gameid]

def get_game(gameid, throw=True):
    gameid = str(gameid)
    if gameid in GAMES:
        return GAMES[gameid]
    if throw:
        raise GameNotFoundError(gameid)
    return None
