
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftPLUSMINUSleftTIMESDIVIDErightUMINUSASSIGN DIVIDE ID LPAREN MINUS NUMERO PLUS PRINT RPAREN SEMICOLON STRING TIMESS : comando\n         | atribuicaocomandos : comandos comando\n                | comandoatribuicao : ID ASSIGN expressaoexpressao : expressao PLUS expressao\n                 | expressao MINUS expressao\n                 | expressao TIMES expressao\n                 | expressao DIVIDE expressaoexpressao : MINUS expressao %prec UMINUSexpressao : LPAREN expressao RPARENexpressao : NUMEROexpressao : STRINGcomando : PRINT LPAREN expressao RPAREN SEMICOLONexpressao : ID'
    
_lr_action_items = {'PRINT':([0,],[4,]),'ID':([0,6,7,8,10,17,18,19,20,],[5,13,13,13,13,13,13,13,13,]),'$end':([1,2,3,11,12,13,14,21,22,23,24,25,26,27,],[0,-1,-2,-12,-13,-15,-5,-10,-11,-14,-6,-7,-8,-9,]),'LPAREN':([4,6,7,8,10,17,18,19,20,],[6,8,8,8,8,8,8,8,8,]),'ASSIGN':([5,],[7,]),'MINUS':([6,7,8,9,10,11,12,13,14,15,17,18,19,20,21,22,24,25,26,27,],[10,10,10,18,10,-12,-13,-15,18,18,10,10,10,10,-10,-11,-6,-7,-8,-9,]),'NUMERO':([6,7,8,10,17,18,19,20,],[11,11,11,11,11,11,11,11,]),'STRING':([6,7,8,10,17,18,19,20,],[12,12,12,12,12,12,12,12,]),'RPAREN':([9,11,12,13,15,21,22,24,25,26,27,],[16,-12,-13,-15,22,-10,-11,-6,-7,-8,-9,]),'PLUS':([9,11,12,13,14,15,21,22,24,25,26,27,],[17,-12,-13,-15,17,17,-10,-11,-6,-7,-8,-9,]),'TIMES':([9,11,12,13,14,15,21,22,24,25,26,27,],[19,-12,-13,-15,19,19,-10,-11,19,19,-8,-9,]),'DIVIDE':([9,11,12,13,14,15,21,22,24,25,26,27,],[20,-12,-13,-15,20,20,-10,-11,20,20,-8,-9,]),'SEMICOLON':([16,],[23,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'S':([0,],[1,]),'comando':([0,],[2,]),'atribuicao':([0,],[3,]),'expressao':([6,7,8,10,17,18,19,20,],[9,14,15,21,24,25,26,27,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> S","S'",1,None,None,None),
  ('S -> comando','S',1,'p_inicio','parser_A.py',15),
  ('S -> atribuicao','S',1,'p_inicio','parser_A.py',16),
  ('comandos -> comandos comando','comandos',2,'p_comandos','parser_A.py',20),
  ('comandos -> comando','comandos',1,'p_comandos','parser_A.py',21),
  ('atribuicao -> ID ASSIGN expressao','atribuicao',3,'p_atribuicao','parser_A.py',33),
  ('expressao -> expressao PLUS expressao','expressao',3,'p_expressao_aritmetica','parser_A.py',38),
  ('expressao -> expressao MINUS expressao','expressao',3,'p_expressao_aritmetica','parser_A.py',39),
  ('expressao -> expressao TIMES expressao','expressao',3,'p_expressao_aritmetica','parser_A.py',40),
  ('expressao -> expressao DIVIDE expressao','expressao',3,'p_expressao_aritmetica','parser_A.py',41),
  ('expressao -> MINUS expressao','expressao',2,'p_expressao_uminus','parser_A.py',52),
  ('expressao -> LPAREN expressao RPAREN','expressao',3,'p_expressao_parentheses','parser_A.py',56),
  ('expressao -> NUMERO','expressao',1,'p_expressao_numero','parser_A.py',60),
  ('expressao -> STRING','expressao',1,'p_expressao_string','parser_A.py',64),
  ('comando -> PRINT LPAREN expressao RPAREN SEMICOLON','comando',5,'p_comando_print','parser_A.py',68),
  ('expressao -> ID','expressao',1,'p_expressao_id','parser_A.py',72),
]
