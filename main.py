# get the samples from ./samples/ex1.vit and compile it

import sys
from tokenTypes import Token
from token_classifier import TokenClassifier
from parser import Parser

def main():
    data = ''
    with open('./samples/ex1.vit', 'r') as f:
        data = f.read()

    dataLength = len(data)
    words = []
    word = ''
    
    for i in range(dataLength+1):
        if i == dataLength:
            words.append(word)
            break
        c = data[i]
        if c == ' ' or c == '\n' or c == '\t':
            if word == ' ':
                word = ''
                continue
            if len(word) > 0:
                words.append(word)
                word = ''
                continue
            if c == '\n' or c == '\t':
                words.append(c)
                word = ''
                continue
        elif c == '(' or c == ')' or c == '[' or c == ']' or c == '{' or c == '}' or c == ',' or c == ';':
            if len(word) > 0:
                words.append(word)
                word = ''
                words.append(c)
                continue
            else:
                words.append(c)
                continue
        
        word = word + c
    
    tokenClass = TokenClassifier()
    tokens = Token()
    tokenTable = []

    for word in words:
        if(word == ''):
            continue
        if(word[0] == ' '):
            word = word[1:]
        token = tokenClass.classify(word)
        word = word if word != '\n' else '\\n'

        tokenTable.append((tokenClass.getToken(token), word))

    # print all tokens in Token class
    tokenNames = Token.__dict__
    tokenNames = {key: tokenNames[key] for key in tokenNames if not key.startswith('__')}

    #formatting tokenNames[key] from (1,) to just 1
    for key in tokenNames:
        if not key.startswith('__'):
            if type(tokenNames[key]) == tuple:
                tokenNames[key] = tokenNames[key][0]
    
    #print token table
    #for token in tokenTable:
    #    print(token)
    #print('\n\n')
    #use Parser
    parser = Parser(tokenTable)
    parser.parse()

    # print all nodes in the Abstract Syntax Tree (AST)
    #print(parser.syntaxTree[0])

    # If there is no error in the syntax, these lines will be printed
    print("Seu programa não tem erros sintáticos.")
    print("\033[92mPASSOU\033[0m")
    
if __name__ == '__main__':
    main()