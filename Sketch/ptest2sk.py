#!/usr/bin/python
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
def translate(lexresult):
    sketchTokens = [] # a list that will contain the tokens of Sketch assertions
    lists = [] # each element is a Python list, representing a Sketch list;
    # for each element, every element of the element is a Python list representing tokens of a Sketch list element
    currentListNo = -1
    for tokensThisLine in lexresult:
        # sketch code is always like 'assert () == ();\n'
        sketchTokens.append('assert');
        sketchTokens.append('(');
        i = 0
        while i < len(tokensThisLine):
            if tokensThisLine[i] == '[':
                if len(tokensThisLine) > i + 2 and tokensThisLine[i+1] == 'list' and tokensThisLine[i+2] == ':':
                    # a Pyret list begins
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
            else:
                sketchTokens.append(tokensThisLine[i])
            i += 1
        sketchTokens.append(')')
        sketchTokens.append(';')
    
    # print(lists)
    listTokens = []
    for i in range(len(lists)):
        # now we define the list variables in Sketch
        listTokens.append('List<int>'); # currently only supports lists of ints
        listTokens.append('__l' + str(i));
        listTokens.append('=');
        rhsTokens = ['empty', '(', ')']
        for element in lists[i]:
            rhsTokens = ['add', '('] + rhsTokens + [','] + element + [')']
        listTokens += rhsTokens + [';']
    
    # the result is the concatination of var defs and assertions
    return listTokens + sketchTokens

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


def ptest2sk(filename, funcname):
    # Because Sketch doesn't support function names containing '-'
    # we need to change the Pyret function name
    # currently this feature is not implemented, so the param 'funcname' is not used. 
    preprocess(filename)
    lexresult = tokenize(filename.split('.', 1)[0] + '.tmp')
    # print(lexresult)
    transresult = translate(lexresult)
    # print(transresult)
    print(sktokens2skcode(transresult))

if __name__ == '__main__':
    ptest2sk("input.arr", "my-len")
