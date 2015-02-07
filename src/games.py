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
        return int(self.__playerid)

    @property
    def connected(self):
        return self.__ws is not None

    def register_websocket(self, ws):
        self.__ws = ws

    def unregister_websocket(self):
        self.__ws = None


class Game(object):

    def __init__(self, gameid):
        self.__gameid = gameid
        self.__created = time.time()

        # init players
        self.__player1 = Player(1)
        self.__player2 = Player(2)

    def __repr__(self):
        output = "GameID: %s\nCreated: %s\nPlayer 1: %s\nPlayer 2: %s" % \
                (self.gameid, self.created_str, repr(self.player1), repr(self.player2))
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
    def player1(self):
        return self.__player1

    @property
    def player2(self):
        return self.__player2

    def get_player(self, playerid, throw=True):
        playerid = int(playerid)
        if playerid is 1:
            return self.player1
        elif playerid is 2:
            return self.player2
        if throw:
            raise Exception("Invalid player ID")
        return None

def new_game():
    global NEXT_GAMEID
    gameid = str(NEXT_GAMEID)
    NEXT_GAMEID += 1
    GAMES[gameid] = Game(gameid)
    return GAMES[gameid]

def get_game(gameid, throw=True):
    if gameid in GAMES:
        return GAMES[gameid]
    if throw:
        raise GameNotFoundError(gameid)
    return None