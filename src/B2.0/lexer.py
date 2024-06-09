import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'ID',
    'NUMBER',
    'STRING',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'ASSIGN',
    'SEMICOLON',
    'ESCREVER',
    'CONCAT',
    'LPAREN',
    'RPAREN',
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_SEMICOLON = r';'
t_ESCREVER = r'ESCREVER'
t_CONCAT = r'<>'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_ID(t):
    r'[a-z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\'[^\']*\''
    t.value = t.value[1:-1]  
    return t

t_ignore = ' \t\n'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

variables = {}

def p_program(p):
    '''program : statement
               | program statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement_assign(p):
    'statement : ID ASSIGN expression SEMICOLON'
    variables[p[1]] = p[3]

def p_statement_escrever(p):
    'statement : ESCREVER LPAREN expression RPAREN SEMICOLON'
    print(evaluate_expression(p[3]))

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression CONCAT expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_string(p):
    'expression : STRING'
    p[0] = p[1]

def p_expression_id(p):
    'expression : ID'
    try:
        p[0] = variables[p[1]]
    except LookupError:
        print(f"Undefined name '{p[1]}'")
        p[0] = 0

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

def evaluate_expression(expr):
    if isinstance(expr, tuple):
        op, left, right = expr
        left = evaluate_expression(left)
        right = evaluate_expression(right)
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '<>':
            return str(left) + str(right)
    else:
        return expr

code = '''
idade = 18;
ESCREVER(idade);
ESCREVER('A tua idade: ' <> idade);
ESCREVER(365 + 5);
curso = 'ESI';
ESCREVER('OLA, ' <> curso);
'''

lexer.input(code)
parser.parse(code)
