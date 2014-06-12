
(function(window) {

	wsapi = {};

	wsapi.INIT_REQ_ID = 0;
	wsapi.INIT_RES_ID = 1;

	wsapi.INIT_REQ = function(gameid) {
		return {
			type: wsapi.INIT_REQ_ID,
			game_id: gameid
		};
	};

	window.wsapi = wsapi;

})(window);
