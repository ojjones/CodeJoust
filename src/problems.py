"""
Problems manager
"""
import os

import tornado.web

import controllers

PROBLEMSPATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "problems")

class ProblemNotFoundError(Exception):
    """
    Error raised when a problem does not exist
    """
    def __init__(self, name):
        super(ProblemNotFoundError, self).__init__("Problem '%s' not found." % name)
        self.__name = name

    @property
    def name(self):
        return self.__name

class Problem(object):

    def __init__(self, name):
        self.__name = name
        self.__description = None

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return os.path.join(PROBLEMSPATH, self.name)

    @property
    def description(self):
        if self.__description is None:
            with open(os.path.join(self.path, "description")) as file:
                self.__description = file.read()
        return self.__description

    def valid(self):
        required_files = ["description", "input", "output"]
        if not os.path.isdir(self.path):
            return False
        for file in required_files:
            if not os.path.isfile(os.path.join(self.path, file)):
                return False
        return True

def list_problems():
    problems = []
    for entry in os.listdir(PROBLEMSPATH):
        try:
            problems.append(get_problem(entry))
        except:
            pass
    return problems

def get_problem(name, throw=True):
    problem = Problem(name)
    if problem.valid():
        return problem
    elif throw:
        raise ProblemNotFoundError(name)
    return None


class ProblemHandler(controllers.BaseApiHandler):

    def get(self, name=None):
        try:
            if name is not None:
                problem = get_problem(name)
                self.write_json({"name": problem.name,
                            "description": problem.description})
            else:
                self.write_json([{"name": problem.name,
                                  "description": problem.description} for
                                 problem in list_problems()])
        except ProblemNotFoundError as err:
            raise tornado.web.HTTPError(404, err.message)

class JoustProblem:
    def __init__(self, problem_name):
        # XXXJDR make this cleaner, secure, etc...
        self.reference_input = "../problems/%s/sample_input" % problem_name
        self.reference_output = "../problems/%s/sample_output" % problem_name
    def make_compile_cmd(self, filename):
        return
    def make_binary_name(self, filename):
        return

class CJoustProblem(JoustProblem):
    def make_binary_name(self, filename):
        return "%s.out" % filename
    def make_compile_cmd(self, filename):
        return "gcc %s -o %s" % (filename, self.make_binary_name(filename))
