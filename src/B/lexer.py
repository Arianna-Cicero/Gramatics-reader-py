import ply.lex as lex

# Definindo os tokens
tokens = [
    'ESCREVER',
    'STRING',
    'LPAREN', 
    'RPAREN', 
    'PLUS',
    'MINUS',  
    'IDENTIFICADOR',
    'NUMERO',
    'INTERPOLACAO',
    'CARACTER_ESPECIAL',
    'CARACTER_ACENTUADO',
    'CARACTER_NAO_IMPRIMIVEL',
    # 'ATRIBUICAO',
]

t_ignore = ' \t\n'

t_ESCREVER = r'ESCREVER'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
# t_ATRIBUICAO = r'='

def t_STRING(t):
    r'\".*?\"|\'[^\']*\''
    t.value = t.value[1:-1]  # Remover as aspas
    return t

def t_NUMERO(t):
    r'\d+'  # Usa uma raw string aqui
    t.value = int(t.value)
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_INTERPOLACAO(t):
    r'\{.*?\}'
    t.value = t.value[1:-1].strip()  # Remover as chaves e espaços em branco
    return t

def t_CARACTER_ESPECIAL(t):
    r'[!@#$%^&*\(\)\[\]\{\}\|\\;:\'\"<>,.?/~`]'
    return t

def t_CARACTER_ACENTUADO(t):
    r'[áàãâéèẽêíìĩîóòõôúùũûÁÀÃÂÉÈẼÊÍÌĨÎÓÒÕÔÚÙŨÛ]'
    return t

def t_CARACTER_NAO_IMPRIMIVEL(t):
    r'[^\x20-\x7E]'
    return t

def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()