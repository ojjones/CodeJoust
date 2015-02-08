function Setup() {
    var editor = ace.edit("editor-actual");
    editor.setTheme("ace/theme/tomorrow_night_eighties");

    var goofModeTimer;


    /*
    var editor2 = ace.edit("editor-mock");
    editor2.setTheme("ace/theme/twilight");
    */

    //////////
    btnCompile$ = $('#btn-compile')
    ulErrors$ = $('#error-list')
    //////////

    // Send the code to the server to compile
    function Compile() {
        console.log("hello")
        $.ajax({
            url: "/compile",
            data: {},
            type: "POST",
            success: function (res) {
            }
        })
    }

    function ShowErrors(list) {
        ulErrors$.empty()
        $.each(list, function(i, o) {
            var error = $('<li>' + o.text + '</li>')
            ulErrors$.append(error)
        })
        $('#errorModal').modal('show') 
    }


    //ShowErrors([{text: "hello"}, {text: "world"}]);

    //
    // Setup Compile bindings
    //
    btnCompile$.on('click', Compile) 
    $(document).keydown(function(event) {
        if((event.ctrlKey || event.metaKey) && event.which == 66) {
            event.preventDefault();
            Compile()
            return false;
        };
    });

    function DisableSyntaxValidation() {
        editor.session.setOption("useWorker", false);
    }

    function EnableSyntaxValidation() {
        editor.session.setOption("useWorker", true);
    }

    window.dsv = DisableSyntaxValidation;
    window.esv = EnableSyntaxValidation;

    ////

    function DisableSyntaxColor() {
        editor.getSession().setMode("");
    }

    function EnableSyntaxColor() {
        editor.getSession().setMode("ace/mode/c_cpp");
    }

    window.dsc = DisableSyntaxColor;
    window.esc = EnableSyntaxColor;

    ////

    function DisableCodeCompletion() {
        editor.setBehavioursEnabled(false)
    }

    function EnableCodeCompletion() {
        editor.setBehavioursEnabled(true)
    }

    window.dcc = DisableCodeCompletion;
    window.ecc = EnableCodeCompletion;

    /////
    
    function DisableGutter() {
        editor.renderer.setShowGutter(false);
    }

    function EnableGutter() {
        editor.renderer.setShowGutter(true);
    }

    window.dg = DisableGutter;
    window.eg = EnableGutter;

    /////
    
    function DisableGoofyMode() {
        clearInterval(goofModeTimer)
        editor.getSession().setMode("ace/mode/c_cpp");
    }

    function EnableGoofyMode() {
        var modes =["python", "perl", "java", "php", "ruby"]
        var i = 0;

        goofModeTimer = setInterval(function() {
            editor.getSession().setMode("ace/mode/" + modes[i%modes.length] );
            i++
        }, 1000);
    }

    //eg();
   // esc();
    //ecc();


/*

    var s = new Socket("");
    editor.getSession().on("change", function (e) {
        s.emit('patchPlayer' + $.cookie('player'), {
            patch: e.data
        })
    })
    */

}

function Init() {
    var gameId = $.cookie('gameId')
    var playerId = $.cookie('playerId')


    var locationHash = window.location.hash

    if (locationHash) {
        locationHash = locationHash.substring(1)

        if (gameId && gameId != locationHash) {
            // Two games
            // Find which one to play
        } else {
            //
        }
    } else {
        // No location hash set
        if (gameId == undefined) {
            // No game detected
        } else {
            // Game cookie set
        }
    }

    /*
    $.cookie('gameId', 'a game')
    $.cookie('playerId', 'a player')
    */

}

Init();
