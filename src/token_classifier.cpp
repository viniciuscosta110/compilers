class TokenClassifier {
private:
    std::string tokenIdToStr[Token::qntTokens];

    void initTokens() {
		tokenIdToStr[Token::Identificator] = "Identificator";
		tokenIdToStr[Token::DefFunction] = "DefFunction";
		tokenIdToStr[Token::ReservedProgram] = "ReservedProgram";
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
		tokenIdToStr[Token::ReservedIf] = "ReservedIf";
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
            {"real", Token::TypeDouble},
            {"integer", Token::TypeInteger},
            {"bag", Token::TypeBag},
			{"of", Token::ReservedOf},
            {"main", Token::ReservedMain},
            {"program", Token::ReservedProgram},
            {"if", Token::ReservedIf},
            {"else", Token::ReservedElse},
            {"write", Token::ReservedWrite},
            {"read", Token::ReservedRead},
            {"for", Token::ReservedFor},
            {"while", Token::ReservedWhile},
            {"and", Token::LogicAnd},
            {"or", Token::LogicOr},
            {"not", Token::LogicNot},
        };
        Token tokenType = reserved_words[token];
        if(!tokenType) {
            return Token::Identificator;
        }
        return tokenType;
    }
};