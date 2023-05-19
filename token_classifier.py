#include <unordered_map>
from tokenTypes import Token

class TokenClassifier:
    tokenIdToStr = {}

    def __init__ (self):
        self.tokenIdToStr[Token.Identificator] = "Identificator"
        self.tokenIdToStr[Token.DefFunction] = "DefFunction"
        self.tokenIdToStr[Token.ReservedProgram] = "ReservedProgram"
        self.tokenIdToStr[Token.ReservedMain] = "ReservedMain"
        self.tokenIdToStr[Token.TypeVoid] = "TypeVoid"
        self.tokenIdToStr[Token.TypeInteger] = "TypeInteger"
        self.tokenIdToStr[Token.TypeReal] = "TypeReal"
        self.tokenIdToStr[Token.TypeBag] = "TypeBag"
        self.tokenIdToStr[Token.ReservedOf] = "ResevedOf"
        self.tokenIdToStr[Token.OpenBrace] = "OpenBrace"
        self.tokenIdToStr[Token.CloseBrace] = "CloseBrace"
        self.tokenIdToStr[Token.OpenBracket] = "OpenBracket"
        self.tokenIdToStr[Token.CloseBracket] = "CloseBracket"
        self.tokenIdToStr[Token.OpenPar] = "OpenPar"
        self.tokenIdToStr[Token.ClosePar] = "ClosePar"
        self.tokenIdToStr[Token.EndLine] = "EndLine"
        self.tokenIdToStr[Token.ReservedEnd] = "ReservedEnd"
        self.tokenIdToStr[Token.ReservedIf] = "ReservedIf"
        self.tokenIdToStr[Token.ReservedElse] = "ReservedElse"
        self.tokenIdToStr[Token.ReservedBegin] = "ReservedBegin"
        self.tokenIdToStr[Token.ReservedThen] = "ReservedThen"
        self.tokenIdToStr[Token.ReservedElseBegin] = "ReservedElseBegin"
        self.tokenIdToStr[Token.ReservedFor] = "ReservedFor"
        self.tokenIdToStr[Token.ReservedWhile] = "ReservedWhile"
        self.tokenIdToStr[Token.ReservedWrite] = "ReservedWrite"
        self.tokenIdToStr[Token.ReservedRead] = "ReservedRead"
        self.tokenIdToStr[Token.SignalComma] = "SignalComma"
        self.tokenIdToStr[Token.OperationSum] = "OperationSum"
        self.tokenIdToStr[Token.OperationSub] = "OperationSub"
        self.tokenIdToStr[Token.OperationMult] = "OperationMult"
        self.tokenIdToStr[Token.OperationDiv] = "OperationDiv"
        self.tokenIdToStr[Token.OperationIntegerDiv] = "OperationIntegerDiv"
        self.tokenIdToStr[Token.SignalAtribution] = "SignalAtribution"
        self.tokenIdToStr[Token.RelationEqual] = "RelationEqual"
        self.tokenIdToStr[Token.RelationNotEqual] = "RelationNotEqual"
        self.tokenIdToStr[Token.RelationGreater] = "RelationGreater"
        self.tokenIdToStr[Token.RelationLower] = "RelationLower"
        self.tokenIdToStr[Token.RelationGreaterEqual] = "RelationGreaterEqual"
        self.tokenIdToStr[Token.RelationLowerEqual] = "RelationLowerEqual"
        self.tokenIdToStr[Token.DoubleConst] = "DoubleConst"
        self.tokenIdToStr[Token.IntegerConst] = "IntegerConst"
        self.tokenIdToStr[Token.SignalDot] = "SignalDot"
        self.tokenIdToStr[Token.Unknown] = "Unknown"
        self.tokenIdToStr[Token.SignalSemiComma] = "SignalSemiComma"
        self.tokenIdToStr[Token.SignalTwoPoints] = "SignalTwoPoints"
        self.tokenIdToStr[Token.LogicAnd] = "LogicAnd"
        self.tokenIdToStr[Token.LogicOr] = "LogicOr"
        self.tokenIdToStr[Token.LogicNot] = "LogicNot"
        self.tokenIdToStr[Token.ReservedDoBegin] = "ReservedDoBegin"
	
    def getToken(self, token):
        return self.tokenIdToStr[token]

    def classify(self, token):
        reserved_words = {
            "real": Token.TypeReal,
            "integer": Token.TypeInteger,
            "bag": Token.TypeBag,
			"of": Token.ReservedOf,
            "main": Token.ReservedMain,
            "program": Token.ReservedProgram,
            "function": Token.DefFunction,
            "if": Token.ReservedIf,
            "else": Token.ReservedElse,
            "write": Token.ReservedWrite,
            "read": Token.ReservedRead,
            "for": Token.ReservedFor,
            "while": Token.ReservedWhile,
            "and": Token.LogicAnd,
            "or": Token.LogicOr,
            "not": Token.LogicNot,
            "::=": Token.SignalAtribution,
            "then": Token.ReservedThen,
            "begin": Token.ReservedBegin,
            "end": Token.ReservedEnd,
            "do": Token.ReservedDoBegin,
            "+": Token.OperationSum,
			"-": Token.OperationSub,
			"/": Token.OperationDiv,
            "//": Token.OperationIntegerDiv,
			"*": Token.OperationMult,
            "(": Token.OpenPar,
            ")": Token.ClosePar,
            ";": Token.SignalSemiComma,
            ":": Token.SignalTwoPoints,
            ",": Token.SignalComma,
            ".": Token.SignalDot,
            "=": Token.RelationEqual,
            "<>": Token.RelationNotEqual,
            ">": Token.RelationGreater,
            "<": Token.RelationLower,
            ">=": Token.RelationGreaterEqual,
            "<=": Token.RelationLowerEqual,
            "{": Token.OpenBrace,
            "}": Token.CloseBrace,
            "[": Token.OpenBracket,
            "]": Token.CloseBracket,
            "\n": Token.EndLine,
        }

        tokenType = ''
        try:
            tokenType = reserved_words[token]
        except:
            tokenType = token
        if token.isdigit():
            token = int(token)
        if type(token) == int:
            return Token.IntegerConst
        elif type(token) == float:
            return Token.RealConst
        
        if token == tokenType:
            return Token.Identificator if not token[0].isdigit() and not self.haveSpecialCharacterAtFirstPositin(token[0]) else 'Caracter Inicial Inválido'
            
        return tokenType

    def haveSpecialCharacterAtFirstPositin(self, token):
        return token[0] == '_' or token[0] == '$' or token[0] == '@' or token[0] == '#' or token[0] == '&' or token[0] == '%' or token[0] == '!' or token[0] == '?' or token[0] == '~' or token[0] == '`' or token[0] == '^' or token[0] == '*' or token[0] == '-' or token[0] == '+' or token[0] == '=' or token[0] == '<' or token[0] == '>' or token[0] == '/' or token[0] == '\\' or token[0] == '|' or token[0] == ':' or token[0] == ';' or token[0] == ',' or token[0] == '.' or token[0] == '}' or token[0] == '{' or token[0] == ']' or token[0] == '[' or token[0] == ')' or token[0] == '(' or token[0] == '"' or token[0] == "'"