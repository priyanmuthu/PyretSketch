#!/usr/bin/python
import sys
import subprocess, platform
import os
from string import Template
from translator import ptest2sk, get_test_cases, getFuncSignature
from utils import UtilMethods
from synthesizer import synthesize_list_to_int, synthesize_list_to_list, synthesize_int_to_list

def test_pyret(py_filename: str):
    # py_filename = 'b6_hint_sol.arr'
    # py_filename = os.path.abspath(py_filename)
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    out_dir = os.path.abspath('./out')
    os.chdir(out_dir)

    command = ['pyret', py_filename]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    process.wait()
    
    os.chdir(cur_dir)
    out_str = out.decode()
    err_str = err.decode()
    
    if process.returncode != 0:
        return process.returncode, err_str + '\n' + out_str

    return process.returncode, out_str

def run(instr_filename: str, stu_filename: str):
    generate_hint(instr_filename, stu_filename)

def generate_hint(instr_filename: str, stu_filename: str):
    
    instr_filename = os.path.abspath(instr_filename)
    stu_filename = os.path.abspath(stu_filename)
    test_cases = get_test_cases(instr_filename)
    test_function_name = getFuncSignature(instr_filename)
    test_function_name = test_function_name[0]
    translated_code, funcSignature = ptest2sk(stu_filename)

    # generate sketch
    funcname, return_type, input_type = funcSignature

    return_code = None
    result_str = None

    if input_type == 'List' :
        if return_type == 'List' :
            # list_list_template
            return_code, result_str = synthesize_list_to_list(translated_code, stu_filename)
            pass
        elif return_type == 'Integer':
            # list_int_template
            return_code, result_str = synthesize_list_to_int(translated_code, stu_filename)
    elif input_type == 'Integer':
        if return_type == 'List':
            # int_list_template
            return_code, result_str = synthesize_int_to_list(translated_code, stu_filename)
            pass
        elif return_type == 'Integer':
            print('Unspported now')

    # Putting it in out directory
    if not os.path.exists('out'):
        os.makedirs('out')
    solution_file = './out/' + os.path.basename(stu_filename).split('.', 1)[0] + '_sol.arr'
    test_file = './out/' + os.path.basename(stu_filename).split('.', 1)[0] + '_test.arr'

    result_str = process_result(result_str)
    if not result_str:
        return
    
    clear_terminal()

    UtilMethods.write_text_to_file(solution_file, result_str)

    test_str = add_test_cases(result_str, test_cases, test_function_name)
    UtilMethods.write_text_to_file(test_file, test_str)
    
    # testing the pyret code generated
    return_code, test_output = test_pyret(os.path.basename(test_file))

    if return_code == 0:
        print('No hints available')
    
    print('The test cases are not complete.')
    # print(test_output)
    error_cases = get_failed_test_cases(test_output, stu_filename, test_str.splitlines())

    if error_cases:
        print('Check the following inputs:')

    for cases in error_cases:
        print(cases)

    print('\n\n')
    return

def get_failed_test_cases(error_str: str, stu_filename: str, code_lines: list):
    error_lines = error_str.splitlines()
    error_lines = [l for l in error_lines if ('failed because' in l)]
    error_cases = []
    for lines in error_lines:
        lno = int(lines.split(',')[0].split('line ')[-1])
        error_cases.append(code_lines[lno - 1].strip())

    return error_cases

def process_result(result_str: str):
    relevant_lines = result_str.splitlines()[6:]
    relevant_lines = relevant_lines[:len(relevant_lines)-2]
    return '\n'.join(relevant_lines)

def add_test_cases(result_str: str, test_cases: str, test_function_name: str):

    test_cases_lines = test_cases.strip().splitlines()
    test_cases_lines = ['\t' + l for l in test_cases_lines]
    test_cases_lines.insert(0, 'where:')
    test_cases = '\n'.join(test_cases_lines)
    result_str = result_str.replace('sketch_method', test_function_name)
    relevant_lines = result_str.splitlines()
    last_line = relevant_lines[-1]
    relevant_lines[-1:] = [test_cases, last_line]
    return '\n'.join(relevant_lines)

def clear_terminal():
    print("\033c", end="")

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        run(sys.argv[1], sys.argv[2])
    else:
        # run("input.arr")
        print('error: not enough arguments')