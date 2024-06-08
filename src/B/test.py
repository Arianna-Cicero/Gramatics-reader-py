import ply.lex as lex
import ply.yacc as yacc

# Tokens
tokens = [
    'ESCREVER',
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

t_ESCREVER = r'ESCREVER'
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

variaveis = {}

# Regras de precedência
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# Regras do parser
def p_inicio(p):
    '''S : comandos'''
    p[0] = p[1]

def p_comandos(p):
    '''comandos : comandos comando
                | comando'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_comando(p):
    '''comando : atribuicao
               | escrever'''
    p[0] = p[1]

def p_atribuicao(p):
    'atribuicao : ID ASSIGN expressao SEMICOLON'
    variaveis[p[1]] = p[3]
    p[0] = p[3]

def p_expressao_aritmetica(p):
    '''expressao : expressao PLUS expressao
                 | expressao MINUS expressao
                 | expressao TIMES expressao
                 | expressao DIVIDE expressao'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_expressao_uminus(p):
    'expressao : MINUS expressao %prec UMINUS'
    p[0] = -p[2]

def p_expressao_parentheses(p):
    'expressao : LPAREN expressao RPAREN'
    p[0] = p[2]

def p_expressao_numero(p):
    'expressao : NUMERO'
    p[0] = p[1]

def p_expressao_string(p):
    'expressao : STRING'
    p[0] = p[1]

def p_expressao_id(p):
    'expressao : ID'
    try:
        p[0] = variaveis[p[1]]
    except LookupError:
        print(f"Erro: Variável '{p[1]}' não definida!")
        p[0] = 0

def p_escrever(p):
    'escrever : ESCREVER LPAREN expressao RPAREN SEMICOLON'
    print(p[3])
    p[0] = p[3]

def p_error(p):
    if p:
        print("Erro sintático na posição: ", p.lexpos, "ao analisar:", p.value)
    else:
        print("Erro sintático!")

parser = yacc.yacc()

input_terminal = """
    tmp_01 = 2*3+4;
    a1_ = 12345 - (5191 * 15);
    idade_valida? = 1;
    mult_3! = a1_ * 3;
    ESCREVER("Olá Mundo");
    ESCREVER(365 + 2);
    curso = "ESI";
    ESCREVER("Olá, " + curso);
"""

instructions = input_terminal.split(";")
instructions = instructions[:-1]

for instruction in instructions:
    result = parser.parse(instruction + ";")
    print(result)
