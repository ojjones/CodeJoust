# vim: set tabstop=4 softtabstop=4 shiftwidth=4 expandtab
"""
Web Socket test code
"""
import json

import websocket

import httplib
import unittest
from spec import *

class WebSocketTest(unittest.TestCase):

    def setUp(self):
        self.conn = httplib.HTTPConnection("localhost:8000")

    def tearDown(self):
        self.conn.close()

    def createGame(self):
        self.conn.request("POST", "/api/newgame")
        response = self.conn.getresponse()
        result = response.read()
        result = json.loads(result)
        return result[GAME_ID]

    def playerJoin(self, gameid, playerid):
        body = { GAME_ID : gameid,
                 PLAYER_ID : playerid }
        body = json.dumps(body)
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        self.conn.request("POST", "/api/playerjoin", body, headers)

        response = self.conn.getresponse()
        result = response.read()
        result = json.loads(result)
        self.assertEqual(result[GAME_ID],gameid)
        self.assertEqual(result[PLAYER_ID],playerid)

    def scoreJoin(self, gameid):
        body = { GAME_ID : gameid }
        body = json.dumps(body)
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        self.conn.request("POST", "/api/scorejoin", body, headers)

        response = self.conn.getresponse()
        result = response.read()
        result = json.loads(result)
        self.assertEqual(result[GAME_ID],gameid)

    def initPlayerSocket(self, gameid, playerid):
        self.player_ws = websocket.create_connection("ws://localhost:8000/player/socket")
        msg = {
            "type": INIT_REQ,
            "data": {GAME_ID : gameid,
                     PLAYER_ID : playerid}
        }
        msg = json.dumps(msg)
        self.player_ws.send(msg)

        result = self.player_ws.recv()
        result = json.loads(result)
        self.assertEqual(result["data"][GAME_STATE],STOPPED)

    def playerSendDelta(self, gameid, playerid, delta):
        self.player_ws
        msg = {
            "type": DELTA_UPDATE,
            "data": {PLAYER_ID : playerid,
                     DELTA : delta}
        }
        msg = json.dumps(msg)
        self.player_ws.send(msg)

    def initScoreSocket(self, gameid):
        self.score_ws = websocket.create_connection("ws://localhost:8000/score/socket")
        msg = {
            "type": INIT_REQ,
            "data": {GAME_ID : gameid}
        }
        msg = json.dumps(msg)
        self.score_ws.send(msg)

        result = self.score_ws.recv()
        result = json.loads(result)
        self.assertEqual(result["data"][GAME_STATE],STOPPED)

    def scoreRecvDelta(self):
        result = self.score_ws.recv()
        result = json.loads(result)

        self.assertEqual(result["type"],DELTA_UPDATE)

        return result["data"]

    def testDeltaUpdate(self):
        gameid = self.createGame()
        playerid = "TestTeam"
        self.playerJoin(gameid, playerid)
        self.scoreJoin(gameid)

        self.initPlayerSocket(gameid, playerid)
        self.initScoreSocket(gameid)

        delta = "Test Delta"
        self.playerSendDelta(gameid, playerid, delta)
        result = self.scoreRecvDelta()
        self.assertEqual(result[PLAYER_ID],playerid)
        self.assertEqual(result[DELTA],delta)

if __name__ == "__main__":
    unittest.main()
