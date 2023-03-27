#include <unordered_map>

class TokenClassifier {
private:
    std::string tokenIdToStr[Token::qntTokens];

    void initTokens() {
		tokenIdToStr[Token::Identificator] = "Identificator";
		tokenIdToStr[Token::DefFunction] = "DefFunction";
		tokenIdToStr[Token::ReservedProgram] = "ReservedProgram";
        tokenIdToStr[Token::ReservedMain] = "ReservedMain";
		tokenIdToStr[Token::TypeVoid] = "TypeVoid";
		tokenIdToStr[Token::TypeInteger] = "TypeInteger";
		tokenIdToStr[Token::TypeReal] = "TypeReal";
		tokenIdToStr[Token::TypeBag] = "TypeBag";
		tokenIdToStr[Token::ReservedOf] = "ResevedOf";
		tokenIdToStr[Token::OpenBrace] = "OpenBrace";
		tokenIdToStr[Token::CloseBrace] = "CloseBrace";
		tokenIdToStr[Token::OpenBracket] = "OpenBracket";
		tokenIdToStr[Token::CloseBracket] = "CloseBracket";
		tokenIdToStr[Token::OpenPar] = "OpenPar";
		tokenIdToStr[Token::ClosePar] = "ClosePar";
		tokenIdToStr[Token::EndLine] = "EndLine";
        tokenIdToStr[Token::ReservedEnd] = "ReservedEnd";
		tokenIdToStr[Token::ReservedIf] = "ReservedIf";
        tokenIdToStr[Token::ReservedElse] = "ReservedElse";
        tokenIdToStr[Token::ReservedBegin] = "ReservedBegin";
        tokenIdToStr[Token::ReservedThen] = "ReservedThen";
		tokenIdToStr[Token::ReservedElseBegin] = "ReservedElseBegin";
		tokenIdToStr[Token::ReservedFor] = "ReservedFor";
		tokenIdToStr[Token::ReservedWhile] = "ReservedWhile";
		tokenIdToStr[Token::ReservedWrite] = "ReservedWrite";
		tokenIdToStr[Token::ReservedRead] = "ReservedRead";
		tokenIdToStr[Token::SignalComma] = "SignalComma";
		tokenIdToStr[Token::OperationSum] = "OperationAdd";
		tokenIdToStr[Token::OperationSub] = "OperationSub";
		tokenIdToStr[Token::OperationMult] = "OperationMult";
		tokenIdToStr[Token::OperationDiv] = "OperationDiv";
		tokenIdToStr[Token::OperationIntegerDiv] = "OperationIntegerDiv";
		tokenIdToStr[Token::SignalAtribution] = "SignalAtribution";
		tokenIdToStr[Token::RelationEqual] = "RelationEqual";
		tokenIdToStr[Token::RelationNotEqual] = "RelationNotEqual";
		tokenIdToStr[Token::RelationGreater] = "RelationGreater";
		tokenIdToStr[Token::RelationLower] = "RelationLower";
		tokenIdToStr[Token::RelationGreaterEqual] = "RelationGreaterEqual";
		tokenIdToStr[Token::RelationLowerEqual] = "RelationLowerEqual";
		tokenIdToStr[Token::DoubleConst] = "RealConst";
		tokenIdToStr[Token::IntConst] = "IntegerConst";
		tokenIdToStr[Token::SignalDot] = "SignalDot";
        tokenIdToStr[Token::Unknown] = "Unknown";
        tokenIdToStr[Token::SignalSemiComma] = "SignalSemiComma";
        tokenIdToStr[Token::SignalTwoPoints] = "SignalTwoPoints";
        tokenIdToStr[Token::LogicAnd] = "LogicAnd";
        tokenIdToStr[Token::LogicOr] = "LogicOr";
        tokenIdToStr[Token::LogicNot] = "LogicNot";
    }
public:
	TokenClassifier() {
		this->initTokens();
	}
	std::string getToken(Token token) {
        return this->tokenIdToStr[token];
    }
	Token classify(std::string token) {
    	std::unordered_map<std::string, Token> reserved_words = {
            {"real", Token::TypeReal},
            {"integer", Token::TypeInteger},
            {"bag", Token::TypeBag},
			{"of", Token::ReservedOf},
            {"main", Token::ReservedMain},
            {"program", Token::ReservedProgram},
            {"function", Token::DefFunction},
            {"if", Token::ReservedIf},
            {"else", Token::ReservedElse},
            {"write", Token::ReservedWrite},
            {"read", Token::ReservedRead},
            {"for", Token::ReservedFor},
            {"while", Token::ReservedWhile},
            {"and", Token::LogicAnd},
            {"or", Token::LogicOr},
            {"not", Token::LogicNot},
            {"::=", Token::SignalAtribution},
            {"then", Token::ReservedThen},
            {"begin", Token::ReservedBegin},
            {"end", Token::ReservedEnd},
            {"+", Token::OperationSum},
			{"-", Token::OperationSub},
			{"/", Token::OperationDiv},
            {"//", Token::OperationIntegerDiv},
			{"*", Token::OperationMult},
            {"(", Token::OpenPar},
            {")", Token::ClosePar},
            {";", Token::SignalSemiComma},
            {":", Token::SignalTwoPoints},
            {",", Token::SignalComma},
            {".", Token::SignalDot},
            {"=", Token::RelationEqual},
            {"<>", Token::RelationNotEqual},
            {">", Token::RelationGreater},
            {"<", Token::RelationLower},
            {">=", Token::RelationGreaterEqual},
            {"<=", Token::RelationLowerEqual},
            {"{", Token::OpenBrace},
            {"}", Token::CloseBrace},
            {"[", Token::OpenBracket},
            {"]", Token::CloseBracket},
        };

        Token tokenType = reserved_words[token];
        // check if token is a number
        if(token.find_first_not_of("0123456789") == std::string::npos) {
            return Token::IntConst;
        }

        if(!tokenType) {
            return Token::Identificator;
        }
        return tokenType;
    }
};