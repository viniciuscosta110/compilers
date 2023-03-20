#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <map>

#include "token.cpp"
#include "token_classifier.cpp"

int main (int argc, char *argv[]) {
    TokenClassifier classifier = TokenClassifier();
    std::cout << classifier.getToken(Token::OperationMult) << std::endl;
}