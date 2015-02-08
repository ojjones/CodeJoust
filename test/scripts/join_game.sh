#!/bin/sh
curl -H "Content-type: application/json" -d "{\"playerid\": \"${1}\", \"gameid\": $2}" http://localhost:8000/api/joingame
