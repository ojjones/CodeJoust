# vim: set tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#!/usr/bin/python
"""
Library for compiling and validating small code snippets against a known output
"""
import os
import difflib
import subprocess

# TODO: Use alternate working directory for output
# TODO: Not really safe for production
# TODO: Swap to pretty html table output (needs .css style)
# TODO: Make actual module, put problem class some place else
# TODO: Make some classes and shit, python loves classes

class JoustProblem:
    def __init__(self, problem):
        # XXXJDR make this cleaner, secure, etc...
        self.reference_input = problem.input_file_path
        self.reference_output = problem.output_file_path
    def make_compile_cmd(self, filename):
        return
    def make_binary_name(self, filename):
        return

class CJoustProblem(JoustProblem):
    def make_binary_name(self, filename):
        return "%s.out" % filename
    def make_compile_cmd(self, filename):
        return "gcc %s -o %s" % (filename, self.make_binary_name(filename))

def _pretty_output(output):
    return output.rstrip('\n').split('\n')

def _pretty_file(filename):
    return [line.rstrip('\n') for line in open(filename, 'r')]

def _compile_code(cur_problem, filename):
    # JDR: Use a gcc python plugin?
    
    # XXX don't use shell=True in production...
    compiler_process = subprocess.Popen(cur_problem.make_compile_cmd(filename),
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
    full_output = compiler_process.communicate()

    success = (compiler_process.returncode == 0)

    # stderr
    compiler_output = _pretty_output(full_output[1])
    # XXX full of shit like \x80 ??
    
    return (success, compiler_output)

def _validate_output(cur_problem, filename):
    binary = cur_problem.make_binary_name(filename)
    problem_process = subprocess.Popen("./"+binary, shell=True,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
    full_output = problem_process.communicate(open(cur_problem.reference_input, 'r').read())
    problem_output = _pretty_output(full_output[0])
    valid_output = _pretty_file(cur_problem.reference_output)

    # XXX temp ugly output
    raw_diff_output = difflib.unified_diff(problem_output, valid_output)

    full_diff_output=""
    for line in raw_diff_output:
        full_diff_output += line + "\n"

    success = (len(full_diff_output) == 0)

    os.remove(binary)

    return success, full_diff_output

    # XXX future pretty output
#    full_diff_output =  difflib.HtmlDiff().make_table(problem_output, valid_output)
    # XXX Need style like this in parent page:
    '''
    <style type="text/css">
        table.diff {font-family:Courier; border:medium;}
        .diff_header {background-color:#e0e0e0}
        td.diff_header {text-align:right}
        .diff_next {background-color:#c0c0c0}
        .diff_add {background-color:#aaffaa}
        .diff_chg {background-color:#ffff77}
        .diff_sub {background-color:#ffaaaa}
    </style>
    '''
    

def validate(filename, cur_problem): 
    compile_success = False
    validate_success = False
    compiler_output = None
    validation_output = None
    
    # Step 1: Compile
    (compile_success, compiler_output) = _compile_code(cur_problem, filename)

    # Step 2: Validate
    if compile_success:
        (validate_success, validation_output) = _validate_output(cur_problem, filename)
    
    return (compile_success, compiler_output, validate_success, validation_output)

if __name__ == '__main__':
    fake_problem = CJoustProblem("samples/sample_input.txt", "samples/sample_output.txt")
    for sample in ["samples/sample1.c", "samples/sample2.c", "samples/sample3.c"]:
        print "File: %s" % sample
        (compile_success, compiler_output, validate_success, validation_output) = validate(sample, fake_problem)

        print "Compilation success: %s" % compile_success
        print "Compilation output:"
        print compiler_output
        print "Validation success: %s" % validate_success
        print "Diff output:"
        print validation_output
    
