# import ply.yacc as yacc
# from lexer import tokens

# variaveis = {}

# # Definindo a gramática
# def p_program(p):
#     'program : statement_list'
#     p[0] = ('program', p[1])

# def p_statement_list(p):
#     '''statement_list : statement_list statement
#                       | statement'''
#     if len(p) == 3:
#         p[0] = p[1] + [p[2]]
#     else:
#         p[0] = [p[1]]

# def p_statement(p):
#     '''statement : escrever_statement
#                  | assignment_statement
#                  | comentario_statement'''
#     p[0] = p[1]

# def p_escrever_statement(p):
#     'escrever_statement : ESCREVER "(" expression RPAREN'
#     p[0] = (p[3])

# def p_assignment_statement(p):
#     'assignment_statement : IDENTIFICADOR ATRIBUICAO expression'
#     p[0] = ('assign', p[1], p[3])

# def p_comentario_statement(p):
#     'comentario_statement : LBRACE expression RBRACE'
#     p[0] = ('comentario', p[2])

# def p_expression_binop(p):
#     '''expression : expression PLUS expression
#                   | expression MINUS expression
#                   | expression MULTIPLICACAO expression
#                   | expression DIVISAO expression'''
#     if p[2] == '+':
#         p[0] = ('+', p[1], p[3])
#     elif p[2] == '-':
#         p[0] = ('-', p[1], p[3])
#     elif p[2] == '*':
#         p[0] = ('*', p[1], p[3])
#     elif p[2] == '/':
#         p[0] = ('/', p[1], p[3])

# def p_expression_group(p):
#     'expression : LPAREN expression RPAREN'
#     p[0] = p[2]

# def p_expression_num(p):
#     'expression : NUMERO'
#     p[0] = p[1]

# def p_expression_string(p):
#     'expression : STRING'
#     p[0] = p[1]

# def p_expression_id(p):
#     'expression : IDENTIFICADOR'
#     p[0] = p[1]

# def p_expression_interpolation(p):
#     'expression : INTERPOLACAO expression INTERPOLACAO'
#     p[0] = ('interpolacao', p[2])


# def p_expression_special_char(p):
#     'expression : CARACTER_ESPECIAL'
#     p[0] = p[1]

# def p_expression_accented_char(p):
#     'expression : CARACTER_ACENTUADO'
#     p[0] = p[1]

    

# def p_error(p):
#     if p:
#         print("Erro sintático na posição:", p.lexpos, "ao analisar:", p.value)
#     else:
#         print("Erro sintático!")

# parser = yacc.yacc()

# input_terminal = """
#     ESCREVER("Olá Mundo");
#     ESCREVER(365 + 2);
#     curso = "ESI";
#     ESCREVER("Olá, " + curso);
#     {- exemplo interpolação de strings
#     Olá, EST IPCA!-}
#     escola = "EST";
#     inst = "IPCA";
#     ESCREVER("Olá, #{escola} #{inst}!");
# """

# # input_terminal = """
# #     ESCREVER ( "Olá Mundo" );
# # """


# instructions = input_terminal.split(";")
# instructions = instructions[:-1]

# for instruction in instructions:
#     result = parser.parse(instruction)
#     print(result)