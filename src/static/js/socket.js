
function Socket(url) {
    var sock = new WebSocket(url, "protocolOne");
    var eventList = {}

    sock.onmessage = function (msg) {
        var parsedMsg = {}
        try {
            parsedMsg = json.Parse(msg)
        } catch (e) {
            console.error("Could not parse message")
            return;
        }

        if (!parsedMsg.event || !parsedMsg.payload) {
            console.error("Not a valid message")
            return;
        }

        var cbList = eventList[msg.event]
        if (cbList == undefined) {
            console.error("No callback registered")
            return;
        }

        for (var i = 0; i < cbList; i++) {
           var cb = cbList[i]

           cb(parsedMsg.payload)
        }
    }

    this.on = function(ev, cb) {
        if(typeof cb != "function")
            return;

        if (eventList[ev] == undefined) {
            eventList[ev] = []
            eventList[ev].push(cb)
        }
    }

    this.emit = function(ev, payload) {
        sock.send(json.Stringify({
            event: ev,
            payload: payload
        })
    }
}
