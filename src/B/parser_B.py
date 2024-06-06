import ply.yacc as yacc

# Importa tokens do lexer
from lexer import tokens

# Parser rules
def p_instrucao(p):
    '''instrucao : ESCREVER LPAREN valor RPAREN 
                 | atribuicao'''
                #  | INTERPOLACAO
    p[0] = p[1]
 
def p_atribuicao(p):
    '''atribuicao : IDENTIFICADOR '=' valor'''
    p[0] = p[3]

def p_valor(p):
    '''valor : STRING
             | expressao'''
    p[0] = p[1]

def p_expressao(p):
    '''expressao : expressao PLUS expressao
                 | expressao MINUS expressao
                 | LPAREN expressao RPAREN
                 | NUMERO
                 | IDENTIFICADOR
                 | INTERPOLACAO
                 | CARACTER_ESPECIAL
                 | CARACTER_ACENTUADO
                 | CARACTER_NAO_IMPRIMIVEL'''
    if len(p) == 4:
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
    else:
        p[0] = p[1]

def p_error(p):
    if p:
        print("Erro de sintaxe na posição: ", p.lexpos)
    else:
        print("Erro de sintaxe!")

parser = yacc.yacc()

input_terminal = """
    ESCREVER("Olá Mundo");
    ESCREVER(365 * 2);
    curso = "ESI";
    ESCREVER("Olá, " <> curso);
    {− exemplo interpolação de strings
    Olá, EST IPCA!−}
    escola ="EST";
    inst = "IPCA";
    ESCREVER ("Olá, #{escola} #{inst}!");
"""

instructions = input_terminal.split(";")
instructions = instructions[:-1]

for instruction in instructions:
    result = parser.parse(instruction)
    print(result)