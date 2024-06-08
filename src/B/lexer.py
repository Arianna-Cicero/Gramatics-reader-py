import ply.lex as lex
import ply.yacc as yacc

# Definindo os tokens
tokens = [
    'ESCREVER',
    'STRING',
    'LPAREN', 
    'RPAREN', 
    'PLUS',
    'MINUS',  
    # 'MULTIPLICACAO',
    # 'DIVISAO',
    # 'IDENTIFICADOR',
    'NUMERO',
    # 'ATRIBUICAO',
    # 'INTERPOLACAO',
    'CARACTER_ESPECIAL',
    'CARACTER_ACENTUADO',
    # 'LBRACE',
    # 'RBRACE',
]

t_ignore = ' \t\n'

t_ESCREVER = r'ESCREVER'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'[-–—]'
# t_STRING = r'\"([^\\"]|\\.)*\"|\'([^\\\']|\\.)*\''

# t_MULTIPLICACAO = r'\*'
# t_DIVISAO = r'/'
# t_ATRIBUICAO = r'='
# t_LBRACE = r'\{'
# t_RBRACE = r'\}'
# t_CARACTER_ESPECIAL = r'[!@#$%^&*()\[\]\{\}|\\;:\'\"<>,.?/~`]'

# def t_IDENTIFICADOR(t):
#     r'[a-zA-Z_][a-zA-Z_0-9]*'
#     return t

def t_STRING(t):
    r'\"([^\\"]|\\.)*\"|\'([^\\\']|\\.)*\''
    t.value = t.value[1:-1]  # Remover as aspas
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# def t_ATRIBUICAO(t):
#     r'='
#     return t

# def t_INTERPOLACAO(t):
#     r'\#\{[a-zA-Z_][a-zA-Z_0-9]*\}'
#     t.value = t.value[2:-1]  # Remover as chaves e o #
#     return t

def t_CARACTER_ESPECIAL(t):
    r'[!@#$%^&*\[\]\{\}|\\;:\'\"<>,.?/~`]'
    return t

def t_CARACTER_ACENTUADO(t):
    r'[áàãâéèẽêíìĩîóòõôúùũûÁÀÃÂÉÈẼÊÍÌĨÎÓÒÕÔÚÙŨÛçÇ]'
    return t

def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

variaveis : dict = {}

# Parser rules
def p_inicio(p):
    '''S : comando '''
        #  | atribuicao'''
    p[0] = p[1]

def p_comando(p):
    'comando : ESCREVER LPAREN expressao RPAREN'
    p[0] = p[3]

# def p_atribuicao(p):
#     'atribuicao : IDENTIFICADOR ATRIBUICAO expressao'
#     variaveis[p[1]] = p[3]

def p_expressao_aritmetica(p):
    '''expressao : expressao PLUS expressao
                 | expressao MINUS expressao'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]

def p_expressao_parentheses(p):
    'expressao : LPAREN expressao RPAREN'
    p[0] = p[2]

def p_expressao_numero(p):
    'expressao : NUMERO'
    p[0] = p[1]

def p_expressao_string(p):
    'expressao : STRING'
    p[0] = p[1]

def p_expressao_caracter_especial(p):
    'expressao : CARACTER_ESPECIAL'
    p[0] = p[1]

# New parser rule for CARACTER_ACENTUADO
def p_expressao_caracter_acentuado(p):
    'expressao : CARACTER_ACENTUADO'
    p[0] = p[1]

def p_error(p):
    if p:
        print("Erro sintático na posição:", p.lexpos, "ao analisar:", p.value)
    else:
        print("Erro sintático!")

parser = yacc.yacc()

input_terminal = """
    ESCREVER("Olá Mundo");
    ESCREVER(365 + 2);"""
    # curso = "ESI";
    # ESCREVER("Olá, " + curso); 
    # {- exemplo interpolação de strings
    # Olá, EST IPCA!-}
    # escola = "EST";
    # inst = "IPCA";
    # ESCREVER("Olá, #{escola} #{inst}!");
# """

instructions = input_terminal.split(";")
instructions = instructions[:-1]

for instruction in instructions:
    result = parser.parse(instruction)
    print(result)