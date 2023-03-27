#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <map>

#include "token.cpp"
#include "token_classifier.cpp"

using namespace std;

int main (int argc, char *argv[]) {
    TokenClassifier classifier = TokenClassifier();
    string codigo;
    
    while(cin >> codigo) {
        if(codigo != "") cout << '(' << classifier.getToken(classifier.classify(codigo)) << ", " << codigo << ')' << endl;
    }
}