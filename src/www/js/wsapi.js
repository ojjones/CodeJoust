
(function(window) {

	wsapi = {};

	wsapi.TEAM_INIT_REQ_ID = 0;
	wsapi.TEAM_INIT_RES_ID = 1;
	wsapi.TEAM_CODE_PUSH_ID = 2;
	wsapi.SCORE_EDITOR_UPDATE_ID = 3;
	wsapi.SCORE_INIT_ID = 4;
	wsapi.START_ID = 5;
	wsapi.STOP_ID = 6;
	wsapi.WINNER_ID = 7;

	wsapi.INIT_REQ = function(gameid, teamid) {
		return {
			type: wsapi.TEAM_INIT_REQ_ID,
			game_id: gameid,
			team_id: teamid
		};
	};

	wsapi.SCORE_INIT = function(gameid, teamid) {
		return {
			type: wsapi.SCORE_INIT_ID,
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
