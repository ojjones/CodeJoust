
(function(window) {

	wsapi = {};

	wsapi.INIT_REQ_ID = 0;
	wsapi.INIT_RES_ID = 1;

	wsapi.INIT_REQ = function(gameid, teamid) {
		return {
			type: wsapi.INIT_REQ_ID,
			game_id: gameid,
			team_id: teamid
		};
	};

	window.wsapi = wsapi;

})(window);
