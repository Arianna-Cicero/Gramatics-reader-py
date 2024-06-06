import ply.lex as lex

tokens = [
    'PRINT',
    'NUMERO',
    'STRING',
    'LPAREN', 
    'RPAREN', 
    'PLUS',
    'MINUS',
    'NOME_DE_VAR',  
    'TIMES',
    'SEMICOLON',
    'EQUALS',
    'DIVIDE',
]

t_PRINT = r'print'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_STRING = r'\".*?\"|\'[^\']*\''
t_EQUALS = r'='
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_SEMICOLON = r';'

def t_NUMERO(t):
    r'\d+'  
    t.value = int(t.value)
    return t

def t_NOME_DE_VAR(t):
    r'[a-z_][a-zA-Z_0-9]*[\?!]?'
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

lexer.input("print (2+3)*4;")
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)