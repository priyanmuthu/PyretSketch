import subprocess
import os
from string import Template
from utils import UtilMethods

LIST_INT_TEMPLATE_PATH_BASIC = 'list_int_template_basic.sk'
LIST_INT_TEMPLATE_PATH_ADV = 'list_int_template_adv.sk'
LIST_LIST_TEMPLATE_PATH_BASIC = 'list_list_template_basic.sk'
LIST_LIST_TEMPLATE_PATH_ADV = 'list_list_template_adv.sk'
INT_LIST_TEMPLATE_PATH_BASIC = 'int_list_template_basic.sk'
INT_LIST_TEMPLATE_PATH_ADV = 'int_list_template_adv.sk'

def synthesize_list_to_int(translated_code: str, benchmark_file: str):
    sk_file_name = get_sketch_from_template(LIST_INT_TEMPLATE_PATH_BASIC, translated_code, benchmark_file)
    return_code, result_str = synthesize_sketch(sk_file_name, -1)

    if return_code != 0:
        print('Basic sketch failed, trying with advanced grammar')
        sk_file_name = get_sketch_from_template(LIST_INT_TEMPLATE_PATH_ADV, translated_code, benchmark_file)
        return_code, result_str = synthesize_sketch(sk_file_name, 5)

    return return_code, result_str

def synthesize_list_to_list(translated_code: str, benchmark_file: str):
    sk_file_name = get_sketch_from_template(LIST_LIST_TEMPLATE_PATH_BASIC, translated_code, benchmark_file)
    return_code, result_str = synthesize_sketch(sk_file_name, -1)

    if return_code != 0:
        print('Basic sketch failed, trying with advanced grammar')
        sk_file_name = get_sketch_from_template(LIST_LIST_TEMPLATE_PATH_ADV, translated_code, benchmark_file)
        return_code, result_str = synthesize_sketch(sk_file_name, 5)

    return return_code, result_str

def synthesize_int_to_list(translated_code: str, benchmark_file: str):
    sk_file_name = get_sketch_from_template(INT_LIST_TEMPLATE_PATH_BASIC, translated_code, benchmark_file)
    return_code, result_str = synthesize_sketch(sk_file_name, -1)

    if return_code != 0:
        print('Basic sketch failed, trying with advanced grammar')
        sk_file_name = get_sketch_from_template(INT_LIST_TEMPLATE_PATH_ADV, translated_code, benchmark_file)
        return_code, result_str = synthesize_sketch(sk_file_name, 5)

    return return_code, result_str

def get_sketch_from_template(template_path: str, translated_code: str, benchmark_file: str):
    sketch_template = Template(UtilMethods.text_from_file(template_path))
    sketch_string = sketch_template.substitute(assert_statements=translated_code)

    # Putting it in out directory
    if not os.path.exists('out'):
        os.makedirs('out')
    sk_file_name = './out/' + os.path.basename(benchmark_file).split('.', 1)[0] + '.sk'
    sk_file_name = os.path.abspath(sk_file_name)
    print(sk_file_name)
    UtilMethods.write_text_to_file(sk_file_name, sketch_string)
    print('Sketch generated. Store in : ', sk_file_name)
    return sk_file_name

def synthesize_sketch(sketch_file_name: str, inline_limit: int):
    
    # store the current path to come back to it after synthesis
    cur_dir_path = os.path.dirname(os.path.realpath(__file__))

    # Path for sketch
    sketch_dir_path = os.path.abspath('./sketch-1.7.5/sketch-frontend/')
    sk_file_path = os.path.abspath(sketch_file_name)

    # changing to the skech directory
    os.chdir(sketch_dir_path)

    print('running sketch...')
    command = ['./sketch', '--fe-custom-codegen', 'customcodegen.jar', '--bnd-inline-amnt', str(inline_limit), sk_file_path]
    if inline_limit == -1:
        command = ['./sketch', '--fe-custom-codegen', 'customcodegen.jar', sk_file_path]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    process.wait()
    
    os.chdir(cur_dir_path)
    out_str = out.decode()
    
    print('Sketch completed with return code: ', process.returncode )
    print('========')
    if process.returncode == 0:
        print(out_str)

    return process.returncode, out_str