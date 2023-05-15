# get the samples from ./samples/ex1.vit and compile it bottom-up and right-left

import sys
from token import Token
from token_classifier import TokenClassifier

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
    token = Token()
    tokenTable = []
    for word in words:
        token = tokenClass.classify(word)
        word = word if word != '\n' else '\\n'

        tokenTable.append((tokenClass.getToken(token), word))

        print(f'({tokenClass.getToken(token)}, {word})')

if __name__ == '__main__':
    main()