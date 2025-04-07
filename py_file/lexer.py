import sys
from enum import IntEnum

class CharClass(IntEnum):
    LETTER = 0
    DIGIT = 1
    UNKNOWN = 99
    EOF = -1

class Token(IntEnum):
    INT_LIT = 10
    IDENT = 11
    ADD_OP = 21
    SUB_OP = 22
    MULT_OP = 23
    DIV_OP = 24
    LEFT_PAREN = 25
    RIGHT_PAREN = 26
    EOF = -1

class Lexer:
    def __init__(self, filename):
        self.in_fp = open(filename, 'r')
        self.lexeme = []
        self.lex_len = 0
        self.next_char = ''
        self.char_class = CharClass.EOF
        self.next_token = Token.EOF
        self._get_char()

    def _get_char(self):
        self.next_char = self.in_fp.read(1)
        if not self.next_char:
            self.char_class = CharClass.EOF
        elif self.next_char.isalpha():
            self.char_class = CharClass.LETTER
        elif self.next_char.isdigit():
            self.char_class = CharClass.DIGIT
        else:
            self.char_class = CharClass.UNKNOWN

    def _add_char(self):
        if self.lex_len < 98:
            self.lexeme.append(self.next_char)
            self.lex_len += 1
        else:
            print("Error - lexeme too long")

    def _lookup(self, ch):
        token_map = {
            '(': Token.LEFT_PAREN,
            ')': Token.RIGHT_PAREN,
            '+': Token.ADD_OP,
            '-': Token.SUB_OP,
            '*': Token.MULT_OP,
            '/': Token.DIV_OP
        }
        self.next_token = token_map.get(ch, Token.EOF)
        return self.next_token

    def get_token(self):
        self.lexeme = []
        self.lex_len = 0

        while self.next_char.isspace():
            self._get_char()

        if self.char_class == CharClass.LETTER:
            while self.char_class in (CharClass.LETTER, CharClass.DIGIT):
                self._add_char()
                self._get_char()
            self.next_token = Token.IDENT
        elif self.char_class == CharClass.DIGIT:
            while self.char_class == CharClass.DIGIT:
                self._add_char()
                self._get_char()
            self.next_token = Token.INT_LIT
        elif self.char_class == CharClass.UNKNOWN:
            self._lookup(self.next_char)
            self._add_char()
            self._get_char()
        elif self.char_class == CharClass.EOF:
            self.next_token = Token.EOF

        lexeme_str = ''.join(self.lexeme)
        print(f"Next token is: {self.next_token.name}, Next lexeme is {lexeme_str}")
        return self.next_token

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lexer.py <input_file>")
        sys.exit(1)

    lexer = Lexer(sys.argv[1])
    while lexer.get_token() != Token.EOF:
        pass
# we write in the terminal ( python lexer.py input.txt )
# the code lexical analyzer the statment in the text file and identify the token