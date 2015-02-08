
### Types

    <STATE> = <string [STOPPED, STARTED, PAUSED, GAMEOVER]>

    <PROBLEM> = {
        name: <string>
        description: <string>
    }


#### WS: /socket/game

    init_req: {
        gameid: <string>,
        playerid: <string>
    }

    init_res: {
        state: <STATE>,
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

    code_update_event: {
        delta: <string>,
    }

#### WS: /socket/overload

    init_req: {
        gameid: <string>
    }

    init_res: {
        state: <STATE>,
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

    set_state = <STATE>

#### HTTP: /api/compile

    req: {
        gameid: <string>,
        playerid: <string>,
        code: <string> // base64?
    }

    res: none
