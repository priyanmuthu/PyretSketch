#!/usr/bin/python
import sys
import subprocess
import os
from string import Template
from translator import ptest2sk
from utils import UtilMethods
from synthesizer import synthesize_list_to_int, synthesize_list_to_list, synthesize_int_to_list

def run(filename: str):
    
    filename = os.path.abspath(filename)

    translated_code, funcSignature = ptest2sk(filename)
    
    # print(translated_code)
    # return

    # generate sketch
    funcname, return_type, input_type = funcSignature

    return_code = None
    result_str = None

    if input_type == 'List' :
        if return_type == 'List' :
            # list_list_template
            return_code, result_str = synthesize_list_to_list(translated_code, filename)
            pass
        elif return_type == 'Integer':
            # list_int_template
            return_code, result_str = synthesize_list_to_int(translated_code, filename)
    elif input_type == 'Integer':
        if return_type == 'List':
            # int_list_template
            return_code, result_str = synthesize_int_to_list(translated_code, filename)
            pass
        elif return_type == 'Integer':
            print('Unspported now')

    # Putting it in out directory
    if not os.path.exists('out'):
        os.makedirs('out')
    solution_file = './out/' + os.path.basename(filename).split('.', 1)[0] + '_sol.arr'

    print(solution_file)
    result_str = process_result(result_str)
    if result_str:
        UtilMethods.write_text_to_file(solution_file, result_str)
    
    return

def process_result(result_str: str):
    relevant_lines = result_str.splitlines()[6:]
    relevant_lines = relevant_lines[:len(relevant_lines)-2]
    return '\n'.join(relevant_lines)

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        run(sys.argv[1])
    else:
        run("input.arr")