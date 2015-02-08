function Setup() {
    var timer$ = $("#timer")

    timer$.css({
        left: (window.innerWidth / 2) - 50
    })

    var t = Date.now()
    setInterval(function() {
        var diff = Date.now() - t; 
        diff /= 1000
        var minutes = parseInt(diff / 60)
        var seconds = parseInt(diff % 60)
        console.log(minutes, seconds)
        var string_time = ""
        if (minutes > 0) {
            string_time += minutes + ":"
        }
        string_time += seconds;

        timer$.text(string_time)
    }, 1000)

    var eplayer1 = ace.edit("editor-player1");
    eplayer1.setTheme("ace/theme/tomorrow_night_eighties");

    var eplayer2 = ace.edit("editor-player2");
    eplayer2.setTheme("ace/theme/tomorrow_night_eighties");

    var player1Score$ = $("#player1-score")
    var player2Score$ = $("#player2-score")


    //
    // Patch update
    //

    /*
    // Update Player 1 with delta changes
    s.on("patchPlayer1", function (e) {
    eplayer1.getSession().getDocument().applyDeltas([e.patch]);
    })

    // Update Player 2 with delta changes
    s.on("patchPlayer2", function (e) {
    eplayer2.getSession().getDocument().applyDeltas([e.patch]);
    })

    //
    // Score update
    //

    // Update Player 1 score
    s.on("scorePlayer1", function (e) {
    player1Score$.text(e.score)
    })

    // Update Player 2 score
    s.on("scorePlayer2", function (e) {
    player2Score$.text(e.score)
    })
    */
}
