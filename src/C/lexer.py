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
    'COMMA',
    'DEF',
    'END',
    'RETURN'
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
t_COMMA = r','
t_DEF = r'DEF'
t_END = r'END'
t_RETURN = r'RETURN'

def t_ID(t):
    r'[a-z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\'[^\']*\''
    t.value = t.value[1:-1]  # remove quotes
    return t

t_ignore = ' \t\n'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

variables = {}
functions = {}

def p_program(p):
    '''program : statement
               | program statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement_assign(p):
    'statement : ID ASSIGN expression SEMICOLON'
    variables[p[1]] = evaluate_expression(p[3])

def p_statement_escrever(p):
    'statement : ESCREVER LPAREN expression RPAREN SEMICOLON'
    print(evaluate_expression(p[3]))

def p_statement_function(p):
    'statement : DEF ID LPAREN params RPAREN statements END'
    functions[p[2]] = (p[4], p[6])

def p_statement_return(p):
    'statement : RETURN expression SEMICOLON'
    p[0] = ('return', p[2])

def p_params(p):
    '''params : ID
              | params COMMA ID
              | empty'''
    if len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = []

def p_statements(p):
    '''statements : statement
                  | statements statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

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
    p[0] = ('var', p[1])

def p_expression_function_call(p):
    'expression : ID LPAREN arguments RPAREN'
    p[0] = ('call', p[1], p[3])

def p_arguments(p):
    '''arguments : expression
                 | arguments COMMA expression
                 | empty'''
    if len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = []

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

def evaluate_expression(expr, local_vars=None):
    if local_vars is None:
        local_vars = variables
    
    if isinstance(expr, tuple):
        if expr[0] == 'call':
            func_name = expr[1]
            args = expr[2]
            if func_name in functions:
                params, body = functions[func_name]
                if len(params) != len(args):
                    print(f"Argument mismatch in call to '{func_name}'")
                    return None
                local_scope = dict(local_vars)
                for param, arg in zip(params, args):
                    local_scope[param] = evaluate_expression(arg, local_vars)
                return evaluate_statements(body, local_scope)
            else:
                print(f"Undefined function '{func_name}'")
                return None
        elif len(expr) == 3:
            op, left, right = expr
            left = evaluate_expression(left, local_vars)
            right = evaluate_expression(right, local_vars)
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
        elif expr[0] == 'var':
            return local_vars.get(expr[1], 0)
    else:
        return expr

def evaluate_statements(statements, local_vars):
    result = None
    for statement in statements:
        if isinstance(statement, tuple) and statement[0] == 'return':
            result = evaluate_expression(statement[1], local_vars)
            break
        else:
            evaluate_statement(statement, local_vars)
    return result

def evaluate_statement(statement, local_vars):
    if isinstance(statement, tuple):
        if statement[0] == 'assign':
            local_vars[statement[1]] = evaluate_expression(statement[2], local_vars)
        elif statement[0] == 'escrever':
            print(evaluate_expression(statement[1], local_vars))
    else:
        evaluate_expression(statement, local_vars)

code = '''
DEF add(a, b)
    RETURN a + b;
END

idade = 18;
ESCREVER(idade);
ESCREVER('A tua idade: ' <> idade);
ESCREVER(365 + 2);
curso = 'ESI';
ESCREVER('OLA, ' <> curso);
x = 2;
y = 3;
ESCREVER('Parametros para a funcao: ' <> x <> ' e ' <> y);
resultado = add(x, y);
ESCREVER('Resultado da funcao: ' <> resultado);
'''

lexer.input(code)
parser.parse(code)
