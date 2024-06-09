import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'ID', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'ASSIGN', 'SEMICOLON', 'LPAREN', 'RPAREN',
    'ESCREVER', 'CONCAT', 'IF', 'ELIF', 'ELSE', 'COLON',
    'WHILE', 'DEF', 'RETURN', 'END',
    'GT', 'LT', 'GE', 'LE', 'EQ', 'NE', 'COMMA'
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
t_COMMA = r','
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
    return t

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
    'statement_def : DEF ID LPAREN params RPAREN COLON statement_list RETURN expression SEMICOLON END'
    functions[p[2]] = (p[4], p[7], p[9])
    p[0] = None

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
    p[0] = None

def p_error(p):
    print("Syntax error at '%s'" % p.value)

parser = yacc.yacc()

def evaluate_expression(expr, local_vars=None):
    if local_vars is None:
        local_vars = variables
    
    if isinstance(expr, tuple):
        if expr[0] == 'call':
            func_name = expr[1]
            args = expr[2]
            if func_name in functions:
                params, body, ret_expr = functions[func_name]
                if len(params) != len(args):
                    print(f"Argument mismatch in call to '{func_name}'")
                    return None
                local_scope = dict(local_vars)
                for param, arg in zip(params, args):
                    local_scope[param] = evaluate_expression(arg, local_vars)
                execute_block(body, local_scope)
                return evaluate_expression(ret_expr, local_scope)
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
            elif op == '>':
                return left > right
            elif op == '<':
                return left < right
            elif op == '>=':
                return left >= right
            elif op == '<=':
                return left <= right
            elif op == '==':
                return left == right
            elif op == '!=':
                return left != right
            elif op == '<>':
                return str(left) + str(right)
        elif expr[0] == 'var':
            return local_vars.get(expr[1], 0)
        elif expr[0] == 'concat':
            return str(evaluate_expression(expr[1], local_vars)) + str(evaluate_expression(expr[2], local_vars))
    else:
        return expr

def execute_block(block, local_vars=None):
    if local_vars is None:
        local_vars = variables

    result = None
    for statement in block:
        result = execute_statement(statement, local_vars)
        if result is not None and result[0] == 'return':
            return result[1]
    return result

def execute_statement(statement, local_vars=None):
    if local_vars is None:
        local_vars = variables

    if statement[0] == 'assign':
        local_vars[statement[1]] = evaluate_expression(statement[2], local_vars)
    elif statement[0] == 'ESCREVER':
        print(evaluate_expression(statement[1], local_vars))
    elif statement[0] == 'if':
        cond, true_block, elif_blocks, else_block = statement[1], statement[2], statement[3], statement[4]
        if evaluate_expression(cond, local_vars):
            return execute_block(true_block, local_vars)
        for elif_cond, elif_block in elif_blocks:
            if evaluate_expression(elif_cond, local_vars):
                return execute_block(elif_block, local_vars)
        return execute_block(else_block, local_vars)
    elif statement[0] == 'while':
        while evaluate_expression(statement[1], local_vars):
            result = execute_block(statement[2], local_vars)
            if result is not None and result[0] == 'return':
                return result
    elif statement[0] == 'return':
        return ('return', evaluate_expression(statement[1], local_vars))


# program2 = '''
# a = 1;
# b = 5;
# IF a > b : 
#     ESCREVER('a is greater than b');
# ELIF a < b :
#     ESCREVER('a is less than b');
# ELSE :
#     ESCREVER('a is equal to b');
# '''

# program3 = '''
# x = 5;
# WHILE x > 0 :
#     ESCREVER(x);
#     x = x - 1;
# '''


# for i, program in enumerate([program2, program3 ], start=1):
#     print(f"\nExecuting program {i}:\n")
#     parser.parse(program)


def read_program(filename):
    with open(filename, 'r') as file:
        return file.read()

def main():
    filename = input("Enter the name of the file with the FCA extension: ")
    program = read_program('testes/'+filename)
    parser.parse(program)


if __name__ == "__main__":
    main()