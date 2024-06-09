import ply.lex as lex
import ply.yacc as yacc

# Token list
tokens = (
    'ID', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'ASSIGN', 'SEMICOLON', 'LPAREN', 'RPAREN',
    'ESCREVER', 'CONCAT', 'IF', 'ELIF', 'ELSE', 'COLON',
    'WHILE', 'DEF', 'RETURN', 'END',
    'GT', 'LT', 'GE', 'LE', 'EQ', 'NE',
)

# Token regex
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
    t.value = t.value[1:-1]  # Remove quotes
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
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement statement_list
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + '\n' + p[2]
    else:
        p[0] = p[1]

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
    if p[1] not in variables:
        variables[p[1]] = True
        p[0] = f'int {p[1]} = {p[3]};'
    else:
        p[0] = f'{p[1]} = {p[3]};'

def p_statement_escrever(p):
    'statement_escrever : ESCREVER LPAREN expression RPAREN SEMICOLON'
    p[0] = f'printf("%s\\n", {p[3]});'

def p_statement_if(p):
    '''statement_if : IF expression COLON statement_list elif_blocks else_block'''
    code = f'if ({p[2]}) {{\n{p[4]}\n}}'
    for elif_cond, elif_block in p[5]:
        code += f'else if ({elif_cond}) {{\n{elif_block}\n}}'
    if p[6]:
        code += f'else {{\n{p[6]}\n}}'
    p[0] = code

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
    if p[1]:
        p[0] = p[3]
    else:
        p[0] = ''

def p_statement_while(p):
    'statement_while : WHILE expression COLON statement_list'
    p[0] = f'while ({p[2]}) {{\n{p[4]}\n}}'

def p_statement_def(p):
    'statement_def : DEF ID LPAREN RPAREN COLON statement_list RETURN expression SEMICOLON END'
    function_name = p[2]
    function_body = p[6]
    return_expr = p[8]
    p[0] = f'int {function_name}() {{\n{function_body}\nreturn {return_expr};\n}}'

def p_statement_return(p):
    'statement_return : RETURN expression SEMICOLON'
    p[0] = f'return {p[2]};'

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = f'({p[1]} {p[2]} {p[3]})'

def p_expression_comp(p):
    '''expression : expression GT expression
                  | expression LT expression
                  | expression GE expression
                  | expression LE expression
                  | expression EQ expression
                  | expression NE expression'''
    p[0] = f'({p[1]} {p[2]} {p[3]})'

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = str(p[1])

def p_expression_string(p):
    'expression : STRING'
    p[0] = f'"{p[1]}"'

def p_expression_var(p):
    'expression : ID'
    p[0] = p[1]

def p_expression_concat(p):
    'expression : expression CONCAT expression'
    p[0] = f'strcat({p[1]}, {p[3]})'

def p_expression_call(p):
    'expression : ID LPAREN RPAREN'
    p[0] = f"{p[1]}()"

def p_empty(p):
    'empty :'
    p[0] = ''

def p_error(p):
    print("Syntax error at '%s'" % p.value)

parser = yacc.yacc()

code = '''
idade = 18;
ESCREVER(idade);
ESCREVER('A tua idade: ' <> idade);
ESCREVER(365+2);
curso = 'ESI';
ESCREVER('OLA, ' <> curso);
DEF add():
x = 2;
y = 3;
RETURN x + y;
END
'''

c_code = parser.parse(code)

with open("output.c", "w") as f:
    if c_code:
        f.write(c_code)
    else:
        print("Failed to generate valid C code.")