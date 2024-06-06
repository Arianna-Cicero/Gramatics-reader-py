import ply.yacc as yacc
from lexer import tokens

variaveis : dict = {}

def p_program(p):
    'program : comandos'
    p[0] = p[1]

def p_comandos(p):
    '''comandos : comandos comando
                | comando'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_comando(p):
    '''comando : decl_var SEMICOLON
               | expressao SEMICOLON'''
    p[0] = p[1]

def p_decl_var(p):
    'decl_var : NOME_DE_VAR EQUALS expressao'
    variaveis[p[1]] = p[3]
    p[0] = ('assign', p[1], p[3])


def p_expressao_aritmetica(p):
    '''expressao : expressao PLUS expressao
                 | expressao MINUS expressao
                 | expressao TIMES expressao
                 | expressao DIVIDE expressao'''
    if len(p) == 4:
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] // p[3]


def p_expressao_string(p):
    'expressao : STRING'
    p[0] = p[1]

def p_expressao_nome_de_var(p):
    'expressao: NOME_DE_VAR'
    p[0] = variaveis.get(p[1], 0)

def p_error(p):
    if p:
        print("Syntax error at position:", p.lexpos)
    else:
        print("Syntax error!")

parser = yacc.yacc()

input_terminal = """
    tmp_01 = 2*3+4 ;
    a1_ = 12345 - (5191 * 15) ;
    idade_valida? = 1;
    mult_3! = a1_ * 3 ;
"""

instructions = input_terminal.split(";")
instructions = instructions[:-1]

for instruction in instructions:
    result = parser.parse(f"program: {instruction}")
    print(result)

for var, value in variaveis.items():
    print(f"{var} = {value}")

