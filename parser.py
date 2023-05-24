import sys
from tokenTypes import Token as tokenTypes

class SyntaxTreeNode:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children if children is not None else []

    def __str__(self, level=0):
        result = "  " * level + self.label + "\n"
        for child in self.children:
            result += child.__str__(level + 1)
        return result

class Parser:
    def __init__(self, lexerTable):
        self.tokenNames = tokenTypes.__dict__
        self.tokenNames = {key: self.tokenNames[key] for key in self.tokenNames if not key.startswith('__')}

        for key in self.tokenNames:
            if not key.startswith('__'):
                # formatting self.tokenNames[key] from (1,) to just 1

                if type(self.tokenNames[key]) == tuple:
                    self.tokenNames[key] = self.tokenNames[key][0]

        self.lexerTable = lexerTable
        self.tokenCurrent = lexerTable[0]
        self.proximoToken = lexerTable[1]
        self.posCurrent = 0
        self.syntaxTree = []
        self.tokenList = []

    #Retorna true se o Token **Current** casa com tipo de Token esperado
    def checkToken(self, tipo):
        tokenCurrentId = self.tokenNames[self.tokenCurrent[0]]
        return tipo == tokenCurrentId

    #Retorna true se o próximo Token **(peek)** casa com tipo de Token esperado
    def checkPeek(self, tipo):
        return tipo == self.proximoToken[0]

    #Tenta fazer o casamento do Token Current. Se conseguir, avança para o próximo Token. Do contrário, gera mensagem de erro.
    def match(self, tipo):

        getNameFromTipo = [key for key, value in self.tokenNames.items() if value == tipo]
        expected = getNameFromTipo[0]
        if not self.checkToken(tipo):
            self.abort("Esperava por token do tipo " + expected + ", mas apareceu " + self.tokenCurrent[0])
        else:
            self.tokenList.append(self.tokenCurrent)
            self.nextToken()

    # Avançando com os ponteiros dos tokens (Current e peek)
    def nextToken(self):
        if(self.posCurrent >= len(self.lexerTable)-2):
            return
        self.tokenCurrent = self.proximoToken
        self.posCurrent += 1
        self.proximoToken = self.lexerTable[self.posCurrent+1]

    def abort(self, msg):
        sys.exit("Erro sintático: "+msg)

    def parse(self):
        self.program()

    # program ::= statement
    def program(self):
        self.syntaxTree = SyntaxTreeNode("Program", [])
        self.syntaxTree.children.append(self.statement())
        while(self.posCurrent < len(self.lexerTable)-2):
            self.syntaxTree.children.append(self.statement())

    """
        <sentencas> ::= <comando> <mais_sentencas>
        <mais_sentencas> ::= ; <cont_sentencas>
        <cont_sentencas> ::= <sentencas> | <empty>
    """
    def statement(self):
        syntax_tree = SyntaxTreeNode("Statement")
        newRoot = None

		#   If it is the main program
        if self.checkToken(self.tokenNames['ReservedProgram']):
            newRoot = SyntaxTreeNode("Program", [])
            self.match(self.tokenNames['ReservedProgram'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))   
            self.match(self.tokenNames['ReservedMain'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['SignalSemiComma'])

            nlReturn = self.nl()
            if(nlReturn != None):
                newRoot.children.append(nlReturn)

        #   If it is declaring an integer
        elif self.checkToken(self.tokenNames['TypeInteger']):
            newRoot = SyntaxTreeNode("TypeInteger", [])
            self.match(self.tokenNames['TypeInteger'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))

            self.match(self.tokenNames['Identificator'])
            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))

            while self.checkToken(self.tokenNames['SignalComma']):
                self.match(self.tokenNames['SignalComma'])
                newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
                self.match(self.tokenNames['Identificator'])
                newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['SignalSemiComma'])

        #   if it is declaring a real
        elif self.checkToken(self.tokenNames['TypeReal']):
            newRoot = SyntaxTreeNode("TypeReal", [])
            self.match(self.tokenNames['TypeReal'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['Identificator'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))

            while self.checkToken(self.tokenNames['SignalComma']):
                self.match(self.tokenNames['SignalComma'])

                newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
                self.match(self.tokenNames['Identificator'])

                newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['SignalSemiComma'])
            
        #   Is attribuition
        elif self.checkToken(self.tokenNames['Identificator']):
            newRoot = SyntaxTreeNode(self.tokenCurrent[0], [])
            newRoot.children.append(self.attribuition())
            self.match(self.tokenNames['SignalSemiComma'])

        #   while ( <condicao> ) do begin <sentencas> end
        elif self.checkToken(self.tokenNames['ReservedWhile']):
            newRoot = SyntaxTreeNode(self.tokenCurrent[0], [])
            self.match(self.tokenNames['ReservedWhile'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['OpenPar'])

            newRoot.children.append(self.expression())
            
            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['ClosePar'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['ReservedDoBegin'])

            while not self.checkToken(self.tokenNames['ReservedEnd']):
                newRoot.children.append(self.statement())

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['ReservedEnd'])

        #   if ( <condicao> ) then begin <sentencas> end <pfalsa>
        elif self.checkToken(self.tokenNames['ReservedIf']):
            newRoot = SyntaxTreeNode(self.tokenCurrent[0], [])
            self.match(self.tokenNames['ReservedIf'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['OpenPar'])

            newRoot.children[0].children.append(self.expression())

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['ClosePar'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['ReservedThen'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['ReservedBegin'])
            
            while not self.checkToken(self.tokenNames['ReservedEnd']):
                newRoot.children.append(self.statement())

            self.match(self.tokenNames['ReservedEnd'])
            newRoot.children.append(SyntaxTreeNode("ReservedEnd", []))
            
            pfalsaReturn = self.pfalsa()

            if pfalsaReturn != None:
                newRoot.children.append(pfalsaReturn)

        #   write ( <var_write> ) 
        #   <var_write> ::= <id> <mais_var_write>
        #   <mais_var_write> ::= , <var_write> | <empty>
        elif self.checkToken(self.tokenNames['ReservedWrite']):
            newRoot = SyntaxTreeNode(self.tokenCurrent[0], [])
            self.match(self.tokenNames['ReservedWrite'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['OpenPar'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['Identificator'])
            
            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))

            while self.checkToken(self.tokenNames['SignalComma']):
                self.match(self.tokenNames['SignalComma'])

                newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
                self.match(self.tokenNames['Identificator'])

                newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))

            self.match(self.tokenNames['ClosePar'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['SignalSemiComma'])

        #   <funcao> ::= function <id> <parametros> : <tipo_funcao> ; <corpo> ; <rotina>
        elif self.checkToken(self.tokenNames['DefFunction']):
            newRoot = SyntaxTreeNode(self.tokenCurrent[0], [])
            self.match(self.tokenNames['DefFunction'])
            
            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['Identificator'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['OpenPar'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['Identificator'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            while self.checkToken(self.tokenNames['SignalComma']):
                self.match(self.tokenNames['SignalComma'])

                newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
                self.match(self.tokenNames['Identificator'])

                newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            
            self.match(self.tokenNames['SignalTwoPoints'])
            
            newRoot.children.append(self.primary())

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['ClosePar'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['SignalTwoPoints'])

            newRoot.children.append(self.primary())
            
            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['SignalSemiComma'])

            newRoot.children.append(self.statement())

        #   reserved begin <sentencas> end
        elif self.checkToken(self.tokenNames['ReservedBegin']):
            newRoot = SyntaxTreeNode(self.tokenCurrent[0], [])
            self.match(self.tokenNames['ReservedBegin'])

            while not self.checkToken(self.tokenNames['ReservedEnd']):
                newRoot.children.append(self.statement())

            self.match(self.tokenNames['ReservedEnd'])
            pfalsaReturn = self.pfalsa()

            if pfalsaReturn != None:
                newRoot.children.append(pfalsaReturn)

        #<expressao_bag> ::= <opBag1>(<conteudo> , <conteudo>) | pos(<integer_num>) | <opBag2>(<conteudo>)
        #<opBag1> ::= U | ∩
        #<opBag2> ::= elemento | quantidade
        elif self.checkToken(self.tokenNames['ReservedUnion']):
            newRoot = SyntaxTreeNode(self.tokenCurrent[0], [])
            self.match(self.tokenNames['ReservedUnion'])

            self.match(self.tokenNames['OpenPar'])
            newRoot.children.append(SyntaxTreeNode("OpenPar", []))

            newRoot.children[0].children.append(self.conteudo())

            self.match(self.tokenNames['SignalComma'])
            newRoot.children[0].children.append(SyntaxTreeNode('SignalComma', []))

            newRoot.children[0].children.append(self.conteudo())

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['ClosePar'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['SignalSemiComma'])

        elif self.checkToken(self.tokenNames['ReservedInterception']):
            newRoot = SyntaxTreeNode(self.tokenCurrent[0], [])
            self.match(self.tokenNames['ReservedInterception'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['OpenPar'])

            newRoot.children[0].children.append(self.conteudo())

            newRoot.children[0].children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['SignalComma'])

            newRoot.children[0].children.append(self.conteudo())

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['ClosePar'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['SignalSemiComma'])

        elif self.checkToken(self.tokenNames['ReservedElemento']):
            newRoot = SyntaxTreeNode(self.tokenCurrent[0], [])
            self.match(self.tokenNames['ReservedElemento'])

            self.match(self.tokenNames['OpenPar'])
            newRoot.children.append(SyntaxTreeNode("OpenPar", []))

            self.match(self.tokenNames['OpenBrace'])
            newRoot.children.append(SyntaxTreeNode("OpenBrace", []))

            newRoot.children.append(self.isObject())

            self.match(self.tokenNames['CloseBrace'])
            newRoot.children.append(SyntaxTreeNode("CloseBrace", []))

        else:
            if(self.checkToken(self.tokenNames['EndLine'])):
                self.match(self.tokenNames['EndLine'])
                newRoot = SyntaxTreeNode("EndLine", [])
                return newRoot

            self.abort("Problema com " + self.tokenCurrent[1] + " (" + self.tokenCurrent[0] + ")")

        if newRoot:
            syntax_tree.children.append(newRoot)

        nlReturn = self.nl()
        if(nlReturn != None):
            syntax_tree.children.append(nlReturn)
        
        return syntax_tree
    
    """ 
        <conteudo> ::= {} | {[<integer_num>,<integer_num>]<conteudo_integer_cont>} | {[<real_num>,<integer_num>]<conteudo_real_cont>}
        <conteudo_integer_cont> ::= ,[<integer_num>,<integer_num>]<conteudo_integer_cont>|<empty>
        <conteudo_real_cont> ::= ,[<real_num>,<integer_num>]<conteudo_real_cont>|<empty>
    """
    def conteudo(self):
        newRoot = None

        if(self.checkToken(self.tokenNames['OpenBrace'])):
            self.match(self.tokenNames['OpenBrace'])
            newRoot = SyntaxTreeNode("OpenBrace", [])

            if( self.checkToken(self.tokenNames['CloseBrace'])):
                self.match(self.tokenNames['CloseBrace'])
                newRoot.children.append(SyntaxTreeNode("CloseBrace", []))

            elif(self.checkToken(self.tokenNames['OpenBracket'])):
                self.match(self.tokenNames['OpenBracket'])
                newRoot.children.append(SyntaxTreeNode("OpenBracket", []))

                newRoot.children[0].children.append(self.isNumberOrReal())

                self.match(self.tokenNames['SignalComma'])
                newRoot.children.append(SyntaxTreeNode('SignalComma', []))

                self.match(self.tokenNames['IntegerConst'])
                newRoot.children[0].children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
        elif(self.checkToken(self.tokenNames['ReservedPos'])):
            self.match(self.tokenNames['ReservedPos'])
            newRoot = SyntaxTreeNode("ReservedPos", [])

            self.match(self.tokenNames['OpenPar'])
            newRoot.children.append(SyntaxTreeNode("OpenPar", []))

            newRoot.children[0].children.append(self.isNumberOrReal())

            self.match(self.tokenNames['ClosePar'])
            newRoot.children.append(SyntaxTreeNode("ClosePar", []))
        elif(self.checkToken(self.tokenNames['ReservedElemento'])):
            self.match(self.tokenNames['ReservedElemento'])
            newRoot = SyntaxTreeNode("ReservedElemento", [])

            self.match(self.tokenNames['OpenPar'])
            newRoot.children.append(SyntaxTreeNode("OpenPar", []))

            self.match(self.tokenNames['OpenBrace'])
            newRoot.children[0].children.append(SyntaxTreeNode("OpenBrace", []))

            newRoot.children[0].children[0].children.append(self.isObject())

            self.match(self.tokenNames['CloseBrace'])
            newRoot.children[0].children.append(SyntaxTreeNode("CloseBrace", []))

            while self.checkToken(self.tokenNames['SignalComma']):
                self.match(self.tokenNames['SignalComma'])
                newRoot.children[0].children.append(SyntaxTreeNode('SignalComma', []))
                self.match(self.tokenNames['OpenBrace'])
                newRoot.children[0].children.append(SyntaxTreeNode("OpenBrace", []))
                newRoot.children[0].children[-1].children.append(self.isObject())

                self.match(self.tokenNames['CloseBrace'])
                newRoot.children[0].children.append(SyntaxTreeNode("CloseBrace", []))

            self.match(self.tokenNames['ClosePar'])
            newRoot.children.append(SyntaxTreeNode("ClosePar", []))

        elif(self.checkToken(self.tokenNames['ReservedQuantidade'])):
            self.match(self.tokenNames['ReservedElemento'])
            newRoot = SyntaxTreeNode("ReservedElemento", [])

            self.match(self.tokenNames['OpenPar'])
            newRoot.children.append(SyntaxTreeNode("OpenPar", []))

            self.match(self.tokenNames['OpenBrace'])
            newRoot.children.append(self.isObject())

            self.match(self.tokenNames['CloseBrace'])
            while self.checkToken(self.tokenNames['SignalComma']):
                self.match(self.tokenNames['SignalComma'])
                newRoot.children.append(SyntaxTreeNode('SignalComma', []))
                self.match(self.tokenNames['OpenBrace'])
                newRoot.children.append(self.isObject())
                self.match(self.tokenNames['CloseBrace'])

            self.match(self.tokenNames['ClosePar'])
            newRoot.children.append(SyntaxTreeNode("ClosePar", []))

        else:
            self.abort("Problema com " + self.tokenCurrent[1] + " (" + self.tokenCurrent[0] + ")")

        return newRoot
    def isObject(self):
        newRoot = SyntaxTreeNode("OpenBracket", [])
        self.match(self.tokenNames['OpenBracket'])
        
        newRoot.children.append(self.isNumberOrReal())

        while not self.checkToken(self.tokenNames['CloseBracket']):
            self.match(self.tokenNames['SignalComma'])
            newRoot.children.append(SyntaxTreeNode('SignalComma', []))
            newRoot.children.append(self.isNumberOrReal())
        self.match(self.tokenNames['CloseBracket'])

        if(self.checkToken(self.tokenNames['SignalComma'])):
            self.match(self.tokenNames['SignalComma'])
            newRoot.children.append(SyntaxTreeNode('SignalComma', []))
            newRoot.children.append(self.isObject())
        newRoot.children.append(SyntaxTreeNode("CloseBracket", []))

        return newRoot


    def isNumberOrReal(self):
        newRoot = None

        if(self.checkToken(self.tokenNames['IntegerConst'])):
            self.match(self.tokenNames['IntegerConst'])
            newRoot = SyntaxTreeNode("IntegerConst", [])
        elif(self.checkToken(self.tokenNames['RealConst'])):
            self.match(self.tokenNames['RealConst'])
            newRoot = SyntaxTreeNode("RealConst", [])
        else:
            self.abort("Problema com " + self.tokenCurrent[1] + " (" + self.tokenCurrent[0] + ")")
        
        return newRoot


    def nl(self):
        newRoot = None
        
        if(not self.checkToken(self.tokenNames['EndLine'])):
            if self.checkToken(self.tokenNames['ReservedEnd']):
                newRoot = SyntaxTreeNode(self.tokenCurrent[0], [])
                self.match(self.tokenNames['ReservedEnd'])
        else:
            newRoot = SyntaxTreeNode(self.tokenCurrent[0], [])
            self.match(self.tokenNames['EndLine'])

            while self.checkToken(self.tokenNames['EndLine']):
                self.match(self.tokenNames['EndLine'])

        return newRoot
        
    #<pfalsa> ::= else begin <sentencas> end | <empty>
    def pfalsa(self):
        newRoot = None

        if self.checkToken(self.tokenNames['ReservedElse']):
            newRoot = SyntaxTreeNode(self.tokenCurrent[0], [])
            self.match(self.tokenNames['ReservedElse'])

            newRoot.children.append(SyntaxTreeNode(self.tokenCurrent[0], []))
            self.match(self.tokenNames['ReservedBegin'])
            while not self.checkToken(self.tokenNames['ReservedEnd']):
                newRoot.children.append(self.statement())
            newRoot.children.append(SyntaxTreeNode("ReservedEnd", []))

        return newRoot
            
    # expression ::== equality
    def attribuition(self):
        newRoot = SyntaxTreeNode("Attribuition", [])
        newRoot.children.append(self.primary())

        self.match(self.tokenNames['SignalAtribution'])
        newRoot.children.append(self.expression())
        return newRoot
    
    # <expressao> ::= <expressao_num> | <expressao_bag>
    def expression(self):
        newRoot = SyntaxTreeNode("Expression", [])
        self.equality()
        return newRoot

    # equality
    def equality(self):
        self.comparison()
        while self.checkToken(self.tokenNames['RelationEqual']) or  self.checkToken(self.tokenNames['RelationNotEqual']):
            self.nextToken()
            self.comparison()

    # <relacao> ::= = | > | < | >= | <= | <>
    def comparison(self):
        self.term()
        while self.checkToken(self.tokenNames['RelationLower']) or self.checkToken(self.tokenNames['RelationLowerEqual']) or self.checkToken(self.tokenNames['RelationGreater']) or self.checkToken(self.tokenNames['RelationGreaterEqual']) or self.checkToken(self.tokenNames['RelationEqual']) or self.checkToken(self.tokenNames['RelationNotEqual']):
            self.nextToken()
            self.term()

    # <operador> ::= + | - | * | / | //
    def term(self):
        self.factor()
        while self.checkToken(self.tokenNames['OperationSub']) or self.checkToken(self.tokenNames['OperationSum']):
            self.nextToken()
            self.factor()
    def factor(self):
        self.signedElement()
        while self.checkToken(self.tokenNames['OperationMult']) or self.checkToken(self.tokenNames['OperationDiv']):
            self.nextToken()
            self.signedElement()
    
    # <integer_num> ::= +<num> | -<num> | <num> | 0
    # <real_num> ::= +<num>.<num> | - <num>.<num> | +0.<num> | -0.<num> | <num>.<num> | 0.<num>
    def signedElement(self):
        if self.checkToken(self.tokenNames['OperationSub']) or self.checkToken(self.tokenNames['OperationSum']):
            self.nextToken()
            self.signedElement()
        else:
            self.primary()

    def primary(self):
        newRoot = SyntaxTreeNode(self.tokenCurrent[0], [])
        
        if self.checkToken(self.tokenNames['TypeInteger']):
            self.match(self.tokenNames['TypeInteger'])
        elif self.checkToken(self.tokenNames['TypeReal']):
            self.match(self.tokenNames['TypeReal'])
        elif self.checkToken(self.tokenNames['RealConst']):
            self.match(self.tokenNames['RealConst'])
        elif self.checkToken(self.tokenNames['Identificator']):
            self.match(self.tokenNames['Identificator'])
        elif self.checkToken(self.tokenNames['IntegerConst']):
            self.match(self.tokenNames['IntegerConst'])
        elif self.checkToken(self.tokenNames['TypeBag']):
            self.match(self.tokenNames['TypeBag'])
        else:
            self.abort("Token inesperado, esperava por NUMERO ou IDENTIFICADOR, apareceu: " + self.tokenCurrent[0] + " (" + self.tokenCurrent[1] + ")")

        return newRoot