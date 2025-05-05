from sly import Lexer

class LexerError(Exception):
    pass

class MyLexer(Lexer):
    tokens = {
        NAME, NUMBER, STRING, IF, THEN, ELSE, END, WHILE, DO, DEF, PRINT, TRUE, FALSE,
        PLUS, MINUS, TIMES, DIVIDE, EQUAL, EQEQ, NOTEQ, LPAREN, RPAREN, COMMA
    }

    ignore = ' \t'   # ignore spaces and tabs

    # Operators and punctuation
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    EQEQ    = r'=='
    NOTEQ   = r'!='
    EQUAL   = r'='
    LPAREN  = r'\('
    RPAREN  = r'\)'
    COMMA   = r','

    # String literals (double quotes)
    @_(r'\"[^\"]*\"')
    def STRING(self, token):
        token.value = token.value[1:-1]  # remove surrounding quotes
        return token

    # Number literal (integer or float)
    @_(r'\d+\.\d+')
    def NUMBER(self, token):
        token.value = float(token.value)
        return token

    @_(r'\d+')
    def NUMBER(self, token):
        token.value = int(token.value)
        return token

    # Identifiers and keywords
    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def NAME(self, token):
        # Keywords
        if token.value == 'if':
            token.type = 'IF'
        elif token.value == 'then':
            token.type = 'THEN'
        elif token.value == 'else':
            token.type = 'ELSE'
        elif token.value == 'end':
            token.type = 'END'
        elif token.value == 'while':
            token.type = 'WHILE'
        elif token.value == 'do':
            token.type = 'DO'
        elif token.value == 'def':
            token.type = 'DEF'
        elif token.value == 'print':
            token.type = 'PRINT'
        elif token.value == 'true':
            token.type = 'TRUE'
            token.value = True
        elif token.value == 'false':
            token.type = 'FALSE'
            token.value = False
        else:
            token.type = 'NAME'
        return token

    # Single-line comments (// to end of line)
    @_(r'//.*')
    def COMMENT(self, t):
        pass

    # Newlines (for line counting, but otherwise ignored)
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # Illegal characters
    def error(self, token):
        raise LexerError(f"Illegal character {token.value[0]!r} at line {self.lineno}")
