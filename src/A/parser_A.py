import ply.yacc as yacc
from lexer import tokens
# from lexer import tokens

variaveis : dict = {}

# Regras de precedência
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# Regras do parser
def p_inicio(p):
    '''S : comando
         | atribuicao'''
    p[0] = p[1]

def p_comandos(p):
    '''comandos : comandos comando
                | comando'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_atribuicao(p):
    'atribuicao : ID ASSIGN expressao'
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

def p_comando_print(p):
    'comando : PRINT LPAREN expressao RPAREN SEMICOLON'
    p[0] = ('print', p[3])

def p_expressao_id(p):
    'expressao : ID'
    try:
        p[0] = variaveis[p[1]]
    except LookupError:
        print(f"Erro: Variável '{p[1]}' não definida!")
        p[0] = 0

def p_error(p):
    if p:
        print("Erro sintático na posição: ", p.lexpos , "ao analisar:", p.value)
    else:
        print("Erro sintático!")

parser = yacc.yacc()

input_terminal = """
    tmp_01 = 2*3+4;
    a1_ = 12345 - (5191 * 15);
    idade_valida? = 1;
    mult_3! = a1_ * 3;
"""

instructions = input_terminal.split(";")
instructions = instructions[:-1]

for instruction in instructions:
    result = parser.parse(instruction)
    print(result)