# vim: set tabstop=4 softtabstop=4 shiftwidth=4 expandtab
import os

import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options, parse_command_line
import tornado.web
from tornado.web import url

import controllers
import problems

STATICPATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static")
TEMPLATEPATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates")

define("port", default=8000, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")

def make_app():
    return tornado.web.Application(
        [
            url("/", controllers.DefaultHandler),
            url("/api/newgame", controllers.NewGameHandler, name="newgame"),
            url("/api/joingame", controllers.JoinGameHandler, name="joingame"),
            url(r"/overlord/g([0-9]+)", controllers.OverlordHandler, name="overlord"),
            url("/overlord/socket", controllers.OverlordSocketHandler, name="overlord_socket"),
            url(r"/player/g([0-9]+)p(.+)", controllers.PlayerHandler, name="player"),
            url("/player/socket", controllers.PlayerSocketHandler, name="player_socket"),
            url(r"/api/problem/(.+)", controllers.ProblemHandler, name="api_problem"),
            url("/api/problems", controllers.ProblemHandler, name="api_problems"),
            url("/api/compile", controllers.CompileHandler, name="compile"),
            url(r"/score/g([0-9]+)", controllers.ScoreJoinGameHandler, name="score"),
            url("/score/socket", controllers.ScoreSocketHandler, name="score_socket"),
        ],
        debug=options.debug,
        static_path=STATICPATH,
        template_path=TEMPLATEPATH
        )

def main():
    parse_command_line()
    print "Starting application on port %s" % options.port
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(options.port)
    server.start(1)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
