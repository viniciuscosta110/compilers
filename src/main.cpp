#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <map>
#include <vector>
#include <algorithm>

#include "token.cpp"
#include "token_classifier.cpp"

using namespace std;

vector<string> identifyWords(string program) {
    vector<string> words;
    string word;
    bool inVariable = false;
    int size = program.size() - 1;

    for (int i = size; i >= 0; i--) {
        char c = program[i];
        if (c == ' ' || c == '\t' || c == '\n' || c == ';' || c == ',' || c == '(' || c == ')') {
            if (inVariable && !word.empty()) {
                words.push_back(word);
                word.clear();
                inVariable = false;
            }
            if (c != ' ' && c != '\t' && c != '\n') {
                string specialChar(1, c);
                words.push_back(specialChar);
            }
        } else if (c == ':' && i > 0 && program[i - 1] == ':') {
            if (!word.empty()) {
                words.push_back(word);
                word.clear();
            }
            words.push_back("::=");
            i--;
        } else {
            word = c + word;
            inVariable = true;
        }
    }

    if (inVariable && !word.empty()) {
        words.push_back(word);
    }
    
    return words;
}

int main (int argc, char *argv[]) {
    TokenClassifier classifier = TokenClassifier();
    string codigo;

    cout << argv[1] << endl;

    ifstream input_file(argv[1]);
    if (!input_file) {
        cerr << "Error: Could not open input file " << argv[1] << endl;
        return 1;
    }

    string program((istreambuf_iterator<char>(input_file)), istreambuf_iterator<char>());
    input_file.close();

    vector<string> words = identifyWords(program);
    for (string word : words) {
        Token token = classifier.classify(word);
        cout << '(' << classifier.getToken(token) << ", " << word << ')' << endl;
    }
}