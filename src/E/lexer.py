import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'ID', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'ASSIGN', 'SEMICOLON', 'LPAREN', 'RPAREN',
    'ESCREVER', 'CONCAT', 'IF', 'ELIF', 'ELSE', 'COLON',
    'WHILE', 'DEF', 'RETURN', 'END',
    'GT', 'LT', 'GE', 'LE', 'EQ', 'NE',
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_CONCAT = r'<>'
t_COLON = r':'
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_EQ = r'=='
t_NE = r'!='

def t_ESCREVER(t):
    r'ESCREVER'
    return t

def t_IF(t):
    r'IF'
    return t

def t_ELIF(t):
    r'ELIF'
    return t

def t_ELSE(t):
    r'ELSE'
    return t

def t_WHILE(t):
    r'WHILE'
    return t

def t_DEF(t):
    r'DEF'
    return t

def t_RETURN(t):
    r'RETURN'
    return t

def t_END(t):
    r'END'
    return t

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

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

variables = {}
functions = {}

def p_program(p):
    '''program : statement_list'''
    execute_block(p[1])

def p_statement_list(p):
    '''statement_list : statement statement_list
                      | statement'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : statement_assign
                 | statement_escrever
                 | statement_if
                 | statement_while
                 | statement_def
                 | statement_return'''
    p[0] = p[1]

def p_statement_assign(p):
    'statement_assign : ID ASSIGN expression SEMICOLON'
    p[0] = ('assign', p[1], p[3])

def p_statement_escrever(p):
    'statement_escrever : ESCREVER LPAREN expression RPAREN SEMICOLON'
    p[0] = ('ESCREVER', p[3])

def p_statement_if(p):
    '''statement_if : IF expression COLON statement_list elif_blocks else_block'''
    p[0] = ('if', p[2], p[4], p[5], p[6])

def p_elif_blocks(p):
    '''elif_blocks : elif_block elif_blocks
                   | empty'''
    if p[1] is None:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]

def p_elif_block(p):
    '''elif_block : ELIF expression COLON statement_list'''
    p[0] = (p[2], p[4])

def p_else_block(p):
    '''else_block : ELSE COLON statement_list
                  | empty'''
    p[0] = p[3] if len(p) > 2 else []

def p_statement_while(p):
    'statement_while : WHILE expression COLON statement_list'
    p[0] = ('while', p[2], p[4])

def p_statement_def(p):
    'statement_def : DEF ID LPAREN RPAREN COLON statement_list RETURN expression SEMICOLON END'
    print(f"Defining function {p[2]} with body {p[6]} and return {p[8]}")
    functions[p[2]] = (p[6], p[8])
    p[0] = None

def p_statement_return(p):
    'statement_return : RETURN expression SEMICOLON'
    p[0] = ('return', p[2])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_comp(p):
    '''expression : expression GT expression
                  | expression LT expression
                  | expression GE expression
                  | expression LE expression
                  | expression EQ expression
                  | expression NE expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_string(p):
    'expression : STRING'
    p[0] = p[1]

def p_expression_var(p):
    'expression : ID'
    p[0] = ('var', p[1])

def p_expression_concat(p):
    'expression : expression CONCAT expression'
    p[0] = ('concat', p[1], p[3])

def p_expression_call(p):
    'expression : ID LPAREN RPAREN'
    p[0] = ('call', p[1])

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    print("Syntax error at '%s'" % p.value)

parser = yacc.yacc()

def evaluate_expression(expr):
    if isinstance(expr, tuple):
        if expr[0] in ('+', '-', '*', '/', '>', '<', '>=', '<=', '==', '!='):
            op, left, right = expr
            left_val = evaluate_expression(left)
            right_val = evaluate_expression(right)
            if isinstance(left_val, str) or isinstance(right_val, str):
                # Convert non-strings to strings for comparison if necessary
                left_val = str(left_val)
                right_val = str(right_val)
            if op == '+':
                return left_val + right_val
            elif op == '-':
                return left_val - right_val
            elif op == '*':
                return left_val * right_val
            elif op == '/':
                return left_val / right_val
            elif op == '>':
                return left_val > right_val
            elif op == '<':
                return left_val < right_val
            elif op == '>=':
                return left_val >= right_val
            elif op == '<=':
                return left_val <= right_val
            elif op == '==':
                return left_val == right_val
            elif op == '!=':
                return left_val != right_val
        elif expr[0] == 'var':
            return variables.get(expr[1], f"Undefined name '{expr[1]}'")
        elif expr[0] == 'concat':
            return str(evaluate_expression(expr[1])) + str(evaluate_expression(expr[2]))
        elif expr[0] == 'call':
            if expr[1] in functions:
                func_body, ret_expr = functions[expr[1]]
                print(f"Calling function {expr[1]} with body {func_body} and return {ret_expr}")
                execute_block(func_body)
                return evaluate_expression(ret_expr)
            else:
                return f"Undefined function '{expr[1]}'"
    else:
        return expr

def execute_block(block):
    result = None
    for statement in block:
        result = execute_statement(statement)
        if result is not None and result[0] == 'return':
            return result[1]
    return result

def execute_statement(statement):
    if statement[0] == 'assign':
        variables[statement[1]] = evaluate_expression(statement[2])
    elif statement[0] == 'ESCREVER':
        print(evaluate_expression(statement[1]))
    elif statement[0] == 'if':
        condition = evaluate_expression(statement[1])
        if condition:
            return execute_block(statement[2])
        else:
            for elif_cond, elif_block in statement[3]:
                if evaluate_expression(elif_cond):
                    return execute_block(elif_block)
            return execute_block(statement[4])
    elif statement[0] == 'while':
        condition = evaluate_expression(statement[1])
        while condition:
            execute_block(statement[2])
            condition = evaluate_expression(statement[1])
    elif statement[0] == 'return':
        return ('return', evaluate_expression(statement[1]))

# ESCREVER(idade);
# ESCREVER('A tua idade: ' <> idade);
# ESCREVER(365+2);
# curso = 'ESI';
# ESCREVER('OLA, ' <> curso);
# DEF add():
#     x = 2;
#     y = 3;
#     RETURN x + y;
# END
# resultado = add();
# ESCREVER('Resultado: ' <> resultado);
code = '''
idade = 17;
IF idade > 17:
    ESCREVER('Maior de idade');
ELSE:
    ESCREVER('Menor de idade');
WHILE idade < 21:
    idade = idade + 1;
    ESCREVER(idade);
'''

parser.parse(code)
