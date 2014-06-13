import os

def list_problems():
    problems = {}
    path = "../problems/"
    dirs = os.listdir(path)
    for fol in dirs:
        with open(path+fol+'/description', 'r') as f:
            problems[fol] = "\n".join(f.readlines())
    return problems

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
