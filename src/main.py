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
            url(r"/", controllers.DefaultHandler),
            url(r"/newgame", controllers.NewGameHandler, name="newgame"),
            url(r"/joingame", controllers.JoinGameHandler, name="joingame"),
            url(r"/overlord/g([0-9]+)", controllers.OverlordHandler, name="overlord"),
            url(r"/overlord/socket", controllers.OverlordSocketHandler, name="overlord_socket"),
            url(r"/game/g([0-9]+)p(1|2)", controllers.GameHandler, name="game"),
            url(r"/game/socket", controllers.GameSocketHandler, name="game_socket"),
            url(r"/api/problem/(.+)", problems.ProblemHandler, name="api_problem"),
            url("/api/problems", problems.ProblemHandler, name="api_problems")
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
