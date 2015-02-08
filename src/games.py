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


class Player(object):
    INITIALIZED = 0
    CONNECTED = 1
    DISCONNECTED = 2

    def __init__(self, playerid):
        self.__playerid = playerid
        self.__ws = None

    @property
    def playerid(self):
        return self.__playerid

    @property
    def connected(self):
        return self.__ws is not None

    def register_websocket(self, ws):
        self.__ws = ws

    def unregister_websocket(self):
        self.__ws = None

class Game(object):

    #GAME STATE
    STOP = 0
    START = 1
    PAUSE = 2
    GAME_OVER = 3

    def __init__(self, gameid):
        self.__gameid = gameid
        self.__created = time.time()
        self.__current_problem = None
	self.__game_state = self.STOP

        # init players
        self.__players = {}

    def __repr__(self):
        output = "GameID: %s\nCreated: %s\nPlayer 1: %s\nPlayer 2: %s" % \
                (self.gameid, self.created_str, repr(self.player1), repr(self.player2))
        return output

    def create_player(self, playerid):
        self.__players[playerid] = Player(playerid)

    @property
    def gameid(self):
        return self.__gameid

    @property
    def created(self):
        return self.__created

    @property
    def current_problem(self):
        return self.__current_problem

    @property
    def created_str(self):
        return time.ctime(self.created)

    def set_current_problem(self, problem):
        self.__current_problem = problem

    def get_player(self, playerid, throw=True):
        try:
            player = None
            player = self.__player[playerid]
        except:
            if throw:
                raise Exception("Invalid player ID")
        return player

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
