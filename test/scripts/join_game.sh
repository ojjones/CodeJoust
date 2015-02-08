#!/bin/sh
curl -H "Content-type: application/json" -d '{"playerid": "testplayer", "gameid": 1}' http://localhost:8000/api/joingame
