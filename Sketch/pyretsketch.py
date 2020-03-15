#!/usr/bin/python
import sys
import subprocess
import os
from string import Template

whitespaces = [' ', '\t', '\n']
symbols = ['+', '*', '/', '[', ']', '(', ')', ',', ':']
def preprocess(filename):
    f = open(filename, 'r')
    while True:
        line = f.readline()
        if line == '':
            print("'where:' not found")
            return -1
        line = line.strip()
        if line == "where:":
            break
    # print("'where:' found")
    fout = open(filename.split('.', 1)[0] + '.tmp', 'w')
    flag = 0 #0: normal 1: whitespace detected, discard following contiguous whitespaces
    while True:
        line = f.readline()
        if line == '':
            break
        line = line.strip()
        if line == 'end':
            break
        if line == '':
            continue
        i = 0
        while i < len(line):
            if line[i] == '#':
                # comment
                break
            elif line[i] in whitespaces:
                if flag == 0:
                    flag = 1
                    fout.write(' ')
                else:
                    i += 1
                    continue
            elif line[i] == '"':
                # preserve all characters between quotation marks
                fout.write('"')
                i += 1
                while i < len(line):
                    fout.write(line[i])
                    if line[i] == '"':
                        break
                    i += 1
            else:
                # default, write as it is
                flag = 0
                fout.write(line[i])
            i += 1
        fout.write('\n')
    f.close()
    fout.close()
    return 1


# this function reads a preprocessed Pyret file
# and returns a list of lists of tokens, every sublist representing tokens in a line
def tokenize(filename):
    f = open(filename, 'r')
    result = []
    while True:
        line = f.readline()
        if line == '':
            break
        line = line.strip()
        tokensThisLine = []
        i = 0
        flag = 0
        token = "" # buffer
        while i < len(line):
            if line[i] == '"':
                # consider a string as a token
                token += line[i]
                i += 1
                while i < len(line):
                    token += line[i]
                    if line[i] == '"':
                        break
                    i += 1
            elif line[i] in symbols:
                # the appearance of a symbol forces the chars before it to become a token
                if token != "":
                    tokensThisLine.append(token)
                tokensThisLine.append(line[i])
                token = ""
            elif line[i] in whitespaces:
                # whitespaces separate the tokens, so the chars before it becomes a token
                if token != "":
                    tokensThisLine.append(token)
                    token = ""
                else:
                    pass
            else:
                token += line[i]
            i += 1
        if token != "":
            tokensThisLine.append(token)
        result.append(tokensThisLine)
    return result

# this function takes the result of function 'tokenize' as input
# translates Pyret tokens to Sketch tokens
# returns a list of Sketch tokens
# as well as Pyret function signature containing name, return type and param type
def translate(lexresult):
    sketchTokens = [] # a list that will contain the tokens of Sketch assertions
    lists = [] # each element is a Python list, representing a Sketch list;
    # for each element, every element of the element is a Python list representing tokens of a Sketch list element
    currentListNo = -1
    originalFuncnameCandidates = {}
    paramTypeCandidates = {'Integer':0, 'List':0}
    isListProgram = False
    for tokensThisLine in lexresult:
        # sketch code is always like 'assert () == ();\n'
        sketchTokens.append('assert');
        sketchTokens.append('(');
        functionCallMayExist = False
        nextTokenIsArg = False
        i = 0
        while i < len(tokensThisLine):
            if nextTokenIsArg and tokensThisLine[i] != '(':
                if tokensThisLine[i] == '[' or tokensThisLine[i] == 'empty':
                    paramTypeCandidates['List'] += 1
                else:
                    paramTypeCandidates['Integer'] += 1
                nextTokenIsArg = False
            if tokensThisLine[i] == '[':
                if len(tokensThisLine) > i + 2 and tokensThisLine[i+1] == 'list' and tokensThisLine[i+2] == ':':
                    # a Pyret list begins
                    if functionCallMayExist == False:
                        isListProgram = True # If there is no function call token preceeding '[list:' token, the function is a list function. (a stupid AI... 
                    i += 3
                    thislist = []
                    listbeginning = 1
                    currentListNo += 1
                    while i < len(tokensThisLine) and tokensThisLine[i] != ']':
                        if listbeginning == 1:
                            thislist.append([])
                            listbeginning = 0
                        if tokensThisLine[i] == ',':
                            thislist.append([])
                        else:
                            thislist[-1].append(tokensThisLine[i])
                        i += 1
                    lists.append(thislist)
                    # replace concrete lists with Sketch variable names
                    sketchTokens.append('__l' + str(currentListNo))
                else:
                    print("error: '[' is not followed by 'list:'")
                    return ""
            elif tokensThisLine[i] == 'is':
                sketchTokens.append(')')
                sketchTokens.append('==')
                sketchTokens.append('(')
                functionCallMayExist = False
            else:
                sketchTokens.append(tokensThisLine[i])
                if tokensThisLine[i][0].isalpha() and i + 1 < len(tokensThisLine) and tokensThisLine[i+1] == '(':
                    # print(tokensThisLine[i])
                    functionCallMayExist = True
                    nextTokenIsArg = True
                    if tokensThisLine[i] not in originalFuncnameCandidates:
                        originalFuncnameCandidates[tokensThisLine[i]] = 1
                    else:
                        originalFuncnameCandidates[tokensThisLine[i]] += 1
                    
            i += 1
        sketchTokens.append(')')
        sketchTokens.append(';')
    
    # print(originalFuncnameCandidates)
    # Find the candidate who appears most often and infer it to be the original function name
    # (a stupid AI...
    max_count = 0
    originalFuncname = ''
    for name in originalFuncnameCandidates:
        if originalFuncnameCandidates[name] > max_count:
            originalFuncname = name
            max_count = originalFuncnameCandidates[name]
            

    max_count = 0
    paramType = ''
    for ty in paramTypeCandidates:
        if paramTypeCandidates[ty] > max_count:
            paramType = ty
            max_count = paramTypeCandidates[ty]
    
    for i in range(len(sketchTokens)):
        if sketchTokens[i] == originalFuncname:   
            # sketchTokens[i] = 'list_method' if isListProgram else 'int_method'
            sketchTokens[i] = 'sketch_method'

    listTokens = []
    # for empty list
    listTokens.append('List<int> emlist = empty()')
    listTokens.append(';')
    print(lists)
    print('------------------------------------')
    for i in range(len(lists)):
        # now we define the list variables in Sketch
        listTokens.append('List<int>'); # currently only supports lists of ints
        listTokens.append('__l' + str(i));
        listTokens.append('=');
        rhsTokens = ['emlist']
        for element in reversed(lists[i]):
            rhsTokens = ['add', '('] + rhsTokens + [','] + element + [')']
        listTokens += rhsTokens + [';']
    
    # the result is the concatination of var defs and assertions
    return listTokens + sketchTokens, [originalFuncname, 'List' if isListProgram else 'Integer', paramType]

# this function takes sketch tokens as input
# returns the text of the Sketch harness function body
def sktokens2skcode(sketchTokens):
    result = ""
    for token in sketchTokens:
        if token == ';':
            result += ';\n'
        else:
            result += token + ' '
    return result

def text_from_file(file_path: str):
    f = open(file_path, 'r')
    file_text = f.read()
    f.close()
    return file_text

def write_text_to_file(file_path: str, text: str):
    file = open(file_path, 'w')
    file.write(text)
    file.close()

def ptest2sk(filename, funcname = ''):
    # Just packing of calling preprocessing, tokenizing and translating
    # Because Sketch doesn't support function names containing '-'
    # we need to change the Pyret function name
    # currently the Pyret function name is automatically inferred, so the param 'funcname' is not used. 
    # returns a list of Sketch tokens
    # as well as Pyret function signature containing name, return type and param type
    preprocess(filename)
    lexresult = tokenize(filename.split('.', 1)[0] + '.tmp')
    # print(lexresult)
    transresult, funcSignature = translate(lexresult)
    return transresult, funcSignature
    
def getFuncSignature(filename, funcname = ''):
    # Just packing of calling preprocessing, tokenizing and translating
    # Because Sketch doesn't support function names containing '-'
    # we need to change the Pyret function name
    # currently the Pyret function name is automatically inferred, so the param 'funcname' is not used. 
    # returns a list of Sketch tokens
    # as well as Pyret function signature containing name, return type and param type
    preprocess(filename)
    lexresult = tokenize(filename.split('.', 1)[0] + '.tmp')
    # print(lexresult)
    transresult, funcSignature = translate(lexresult)
    return funcSignature

def run(filename: str):
    
    list_int_template_path = 'list_int_template.sk'
    list_list_template_path = 'list_list_template.sk'


    transresult, funcSignature = ptest2sk(filename)
    translated_code = sktokens2skcode(transresult)
    
    print(translated_code)
    return

    # generate sketch
    funcname, return_type, input_type = funcSignature
    if input_type == 'List' :
        if return_type == 'List' :
            # list_list_template
            pass
        elif return_type == 'Integer':
            # list_int_template
            sketch_template = Template(text_from_file(list_int_template_path))
            sketch_string = sketch_template.substitute(assert_statements=translated_code)
    
    if (sketch_string) is None or (sketch_string == ''):
        return
    
    sk_file_name = filename.split('.', 1)[0] + '.sk'

    write_text_to_file(sk_file_name, sketch_string)

    cur_dir_path = os.path.dirname(os.path.realpath(__file__))
    sketch_dir_path = os.path.abspath('./sketch-1.7.5/sketch-frontend/')
    sk_file_path = os.path.abspath(sk_file_name)
    # print(sk_file_path)
    # print(cur_dir_path)
    # print(sketch_dir_path)

    os.chdir(sketch_dir_path)

    command = ['./sketch', '--fe-custom-codegen', 'customcodegen.jar', '--bnd-inline-amnt', '7', sk_file_path]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    process.wait()
    if process.returncode != 0:
        print(process.returncode)
        print('-------------------\n\n\n\n')
        print(err)
        raise Exception('Error: ', process.returncode)

    os.chdir(cur_dir_path)
    
    write_text_to_file('sol.arr', out.decode())


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        run(sys.argv[1])
    else:
        run("input.arr")