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

    def statement(self):
        syntax_tree = SyntaxTreeNode("Statement")
        newRoot = None

		#   If it is the main program		,
        if self.checkToken(self.tokenNames['ReservedProgram']):
            newRoot = SyntaxTreeNode("Program", [])
            self.match(self.tokenNames['ReservedProgram'])            
            self.match(self.tokenNames['ReservedMain'])
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
            
        #   Is attribuition
        elif self.checkToken(self.tokenNames['Identificator']):
            newRoot = SyntaxTreeNode("Identificator", [])
            newRoot.children.append(self.attribuition())
            self.match(self.tokenNames['SignalSemiComma'])

        #   while ( <condicao> ) do begin <sentencas> end
        elif self.checkToken(self.tokenNames['ReservedWhile']):
            newRoot = SyntaxTreeNode("ReservedWhile", [])
            self.match(self.tokenNames['ReservedWhile'])
            self.match(self.tokenNames['OpenPar'])
            newRoot.children.append(self.expression())
            self.match(self.tokenNames['ClosePar'])
            self.match(self.tokenNames['ReservedDoBegin'])
            newRoot.children.append(SyntaxTreeNode("ReservedDoBegin", []))
            while not self.checkToken(self.tokenNames['ReservedEnd']):
                newRoot.children.append(self.statement())
            self.match(self.tokenNames['ReservedEnd'])

        #   if ( <condicao> ) then begin <sentencas> end <pfalsa>
        elif self.checkToken(self.tokenNames['ReservedIf']):
            newRoot = SyntaxTreeNode("ReservedIf", [])
            self.match(self.tokenNames['ReservedIf'])
            self.match(self.tokenNames['OpenPar'])

            newRoot.children.append(SyntaxTreeNode("OpenPar", []))
            newRoot.children[0].children.append(self.expression())

            self.match(self.tokenNames['ClosePar'])

            newRoot.children.append(SyntaxTreeNode("ClosePar", []))

            self.match(self.tokenNames['ReservedThen'])
            self.match(self.tokenNames['ReservedBegin'])

            newRoot.children.append(SyntaxTreeNode("ReservedBegin", []))
            
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
            newRoot = SyntaxTreeNode("ReservedWrite", [])
            self.match(self.tokenNames['ReservedWrite'])
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
            self.match(self.tokenNames['SignalSemiComma'])

        #   <funcao> ::= function <id> <parametros> : <tipo_funcao> ; <corpo> ; <rotina>
        elif self.checkToken(self.tokenNames['DefFunction']):
            newRoot = SyntaxTreeNode("DefFunction", [])
            self.match(self.tokenNames['DefFunction'])
            self.match(self.tokenNames['Identificator'])
            self.match(self.tokenNames['OpenPar'])
            self.match(self.tokenNames['Identificator'])

            while self.checkToken(self.tokenNames['SignalComma']):
                self.match(self.tokenNames['SignalComma'])
                self.match(self.tokenNames['Identificator'])
            
            self.match(self.tokenNames['SignalTwoPoints'])
            self.primary()
            self.match(self.tokenNames['ClosePar'])

            self.match(self.tokenNames['SignalTwoPoints'])
            self.primary()
            
            self.match(self.tokenNames['SignalSemiComma'])

        #   reserved begin <sentencas> end
        elif self.checkToken(self.tokenNames['ReservedBegin']):
            newRoot = SyntaxTreeNode("ReservedBegin", [])
            self.match(self.tokenNames['ReservedBegin'])

            while not self.checkToken(self.tokenNames['ReservedEnd']):
                newRoot.children.append(self.statement())
            self.match(self.tokenNames['ReservedEnd'])
            pfalsaReturn = self.pfalsa()
            if pfalsaReturn != None:
                newRoot.children.append(pfalsaReturn)

        #<expressao_bag> ::= <opBag1>(<conteudo> , <conteudo>) | pos(<integer_num>) | <opBag2>(<conteudo>)
        #<conteudo> ::= {} | {[<integer_num>,<integer_num>]<conteudo_integer_cont>} | {[<real_num>,<integer_num>]<conteudo_real_cont>}
        #<conteudo_integer_cont> ::= ,[<integer_num>,<integer_num>]<conteudo_integer_cont>|<empty>
        #<conteudo_real_cont> ::= ,[<real_num>,<integer_num>]<conteudo_real_cont>|<empty>
        #<opBag1> ::= U | ∩
        #<opBag2> ::= elemento | quantidade
        elif self.checkToken(self.tokenNames['ReservedUnion']):
            newRoot = SyntaxTreeNode("ReservedUnion", [])
            self.match(self.tokenNames['ReservedUnion'])

            self.match(self.tokenNames['OpenPar'])
            newRoot.children.append(SyntaxTreeNode("OpenPar", []))

            newRoot.children[0].children.append(self.conteudo())

            self.match(self.tokenNames['SignalComma'])
            newRoot.children[0].children.append(SyntaxTreeNode('SignalComma', []))

            newRoot.children[0].children.append(self.conteudo())

            self.match(self.tokenNames['ClosePar'])
            newRoot.children.append(SyntaxTreeNode("ClosePar", []))
            self.match(self.tokenNames['SignalSemiComma'])
        elif self.checkToken(self.tokenNames['ReservedInterception']):
            newRoot = SyntaxTreeNode("ReservedInterception", [])
            self.match(self.tokenNames['ReservedInterception'])

            self.match(self.tokenNames['OpenPar'])
            newRoot.children.append(SyntaxTreeNode("OpenPar", []))

            newRoot.children[0].children.append(self.conteudo())

            self.match(self.tokenNames['SignalComma'])
            newRoot.children[0].children.append(SyntaxTreeNode('SignalComma', []))

            newRoot.children[0].children.append(self.conteudo())
            self.match(self.tokenNames['ClosePar'])
            newRoot.children.append(SyntaxTreeNode("ClosePar", []))
            self.match(self.tokenNames['SignalSemiComma'])
        elif self.checkToken(self.tokenNames['ReservedElemento']):
            self.match(self.tokenNames['ReservedElemento'])
            newRoot = SyntaxTreeNode("ReservedElemento", [])

            self.match(self.tokenNames['OpenPar'])
            newRoot.children.append(SyntaxTreeNode("OpenPar", []))

            self.match(self.tokenNames['OpenBrace'])
            newRoot.children.append(SyntaxTreeNode("OpenBrace", []))

            newRoot.children.append(self.isObject())

            self.match(self.tokenNames['CloseBrace'])
            newRoot.children.append(SyntaxTreeNode("CloseBrace", []))

        else:
            self.abort("Problema com " + self.tokenCurrent[1] + " (" + self.tokenCurrent[0] + ")")

        if newRoot:
            syntax_tree.children.append(newRoot)

        nlReturn = self.nl()
        if(nlReturn != None):
            syntax_tree.children.append(nlReturn)
        
        return syntax_tree
    
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
        elif(self.checkToken(self.tokenNames['DoubleConst'])):
            self.match(self.tokenNames['DoubleConst'])
            newRoot = SyntaxTreeNode("DoubleConst", [])
        else:
            self.abort("Problema com " + self.tokenCurrent[1] + " (" + self.tokenCurrent[0] + ")")
        
        return newRoot
    def nl(self):
        newRoot = None
        
        if(not self.checkToken(self.tokenNames['EndLine'])):
            if self.checkToken(self.tokenNames['ReservedEnd']):
                self.match(self.tokenNames['ReservedEnd'])
                newRoot = SyntaxTreeNode("ReservedEnd", [])
        else: 
            self.match(self.tokenNames['EndLine'])
            newRoot = SyntaxTreeNode("EndLine", [])
            while self.checkToken(self.tokenNames['EndLine']):
                self.match(self.tokenNames['EndLine'])

        return newRoot
        

    def pfalsa(self):
        newRoot = None

        if self.checkToken(self.tokenNames['ReservedElse']):
            self.match(self.tokenNames['ReservedElse'])
            newRoot = SyntaxTreeNode("ReservedElse", [])
            self.match(self.tokenNames['ReservedBegin'])
            newRoot.children.append(SyntaxTreeNode("ReservedBegin", []))
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
        
    def expression(self):
        syntax_tree = SyntaxTreeNode("Expression", [])
        self.equality()
        return syntax_tree
    # equality
    def equality(self):
        self.comparison()
        while self.checkToken(self.tokenNames['RelationEqual']) or  self.checkToken(self.tokenNames['RelationNotEqual']):
            self.nextToken()
            self.comparison()
    # comparison
    def comparison(self):
        self.term()
        while self.checkToken(self.tokenNames['RelationLower']) or self.checkToken(self.tokenNames['RelationLowerEqual']) or self.checkToken(self.tokenNames['RelationGreater']) or self.checkToken(self.tokenNames['RelationGreaterEqual']) or self.checkToken(self.tokenNames['RelationEqual']) or self.checkToken(self.tokenNames['RelationNotEqual']):
            self.nextToken()
            self.term()
    def term(self):
        self.factor()
        while self.checkToken(self.tokenNames['OperationSub']) or self.checkToken(self.tokenNames['OperationSum']):
            self.nextToken()
            self.factor()
    def factor(self):
        self.unary()
        while self.checkToken(self.tokenNames['OperationMult']) or self.checkToken(self.tokenNames['OperationDiv']):
            self.nextToken()
            self.unary()
    def unary(self):
        if self.checkToken(self.tokenNames['OperationSub']) or self.checkToken(self.tokenNames['OperationSum']):
            self.nextToken()
            self.unary()
        else:
            self.primary()

    def primary(self):
        newRoot = None
        if self.checkToken(self.tokenNames['TypeInteger']):
            self.match(self.tokenNames['TypeInteger'])
            newRoot = SyntaxTreeNode("TypeInteger", [])
        elif self.checkToken(self.tokenNames['TypeReal']):
            self.match(self.tokenNames['TypeReal'])
            newRoot = SyntaxTreeNode("TypeReal", [])
        elif self.checkToken(self.tokenNames['DoubleConst']):
            self.match(self.tokenNames['DoubleConst'])
            newRoot = SyntaxTreeNode("DoubleConst", [])
        elif self.checkToken(self.tokenNames['Identificator']):
            self.match(self.tokenNames['Identificator'])
            newRoot = SyntaxTreeNode("Identificator", [])
        elif self.checkToken(self.tokenNames['IntegerConst']):
            self.match(self.tokenNames['IntegerConst'])
            newRoot = SyntaxTreeNode("IntegerConst", [])
        elif self.checkToken(self.tokenNames['TypeBag']):
            self.match(self.tokenNames['TypeBag'])
            newRoot = SyntaxTreeNode("TypeBag", [])
        else:
            self.abort("Token inesperado, esperava por NUMERO ou IDENTIFICADOR, apareceu: " + self.tokenCurrent[0] + " (" + self.tokenCurrent[1] + ")")

        return newRoot