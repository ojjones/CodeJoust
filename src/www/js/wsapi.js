
(function(window) {

	wsapi = {};

	wsapi.INIT_REQ_ID = 0;
	wsapi.INIT_RES_ID = 1;
	wsapi.TEAM_CODE_PUSH_ID = 2;
	wsapi.EDITOR_UPDATE = 3;
	wsapi.SCORE_INIT = 4;
	wsapi.START = 5;
	wsapi.STOP = 6;
	wsapi.WINNER = 7;

	wsapi.INIT_REQ = function(gameid, teamid) {
		return {
			type: wsapi.INIT_REQ_ID,
			game_id: gameid,
			team_id: teamid
		};
	};

	wsapi.INIT_SCORE = function(gameid, teamid) {
		return {
			type: wsapi.SCORE_INIT,
			game_id: gameid,
		};
	};

	wsapi.TEAM_CODE_PUSH = function(gameid, teamid, code) {
		return {
			type: wsapi.TEAM_CODE_PUSH_ID,
			game_id: gameid,
			team_id: teamid,
			code: code
		};
	};

	window.wsapi = wsapi;

})(window);
