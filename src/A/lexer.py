import ply.lex as lex

# Tokens
tokens = [
    'PRINT',
    'NUMERO',
    'STRING',
    'LPAREN', 
    'RPAREN', 
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'ASSIGN',
    'ID',
    'SEMICOLON',
]

t_ignore = ' \t\n'

t_PRINT = r'print'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_SEMICOLON = r';'
t_STRING = r'\".*?\"|\'[^\']*\''

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_!/?]*'
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

