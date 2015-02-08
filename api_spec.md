
### Types

    <GAME_STATE> = <string [STOPPED, STARTED, PAUSED, GAMEOVER]>

    <PROBLEM> = {
        name: <string>
        description: <string>
    }


#### WS: /socket/player

    init_req: {
        gameid: <string>,
        playerid: <string>
    }

    init_res: {
        state: <GAME_STATE>,
        union {
            STOPPED: { },
            STARTED: {
                problem: <PROBLEM>,
                code: <string>
            },
            PAUSED: {},
            GAMEOVER: {
                message: <string>,
                winner: <bool>
            }
        }
    }

    delta_update: {
        delta: <string>,
    }

#### WS: /socket/overload

    init_req: {
        gameid: <string>
    }

    init_res: {
        state: <GAME_STATE>,
        union {
            STOPPED: { },
            STARTED: {
                problem: <PROBLEM>,
                code: <string>
            },
            PAUSED: {},
            GAMEOVER: {
                message: <string>,
                winner: <bool>
            }
        }
    }

    set_state = <GAME_STATE>

#### HTTP: /api/compile

    req: {
        gameid: <string>,
        playerid: <string>,
        code: <string> // base64?
    }

    res: none
