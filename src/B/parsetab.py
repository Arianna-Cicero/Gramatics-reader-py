
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "CARACTER_ACENTUADO CARACTER_ESPECIAL CARACTER_NAO_IMPRIMIVEL ESCREVER IDENTIFICADOR INTERPOLACAO LPAREN MINUS NUMERO PLUS RPAREN STRINGinstrucao : ESCREVER LPAREN valor RPAREN \n                 | atribuicaoatribuicao : IDENTIFICADOR '=' valorvalor : STRING\n             | expressaoexpressao : expressao PLUS expressao\n                 | expressao MINUS expressao\n                 | LPAREN expressao RPAREN\n                 | NUMERO\n                 | IDENTIFICADOR\n                 | INTERPOLACAO\n                 | CARACTER_ESPECIAL\n                 | CARACTER_ACENTUADO\n                 | CARACTER_NAO_IMPRIMIVEL"
    
_lr_action_items = {'ESCREVER':([0,],[2,]),'IDENTIFICADOR':([0,5,6,7,20,21,],[4,12,12,12,12,12,]),'$end':([1,3,9,10,11,12,13,14,15,16,17,19,22,23,24,],[0,-2,-4,-5,-9,-10,-11,-12,-13,-14,-3,-1,-8,-6,-7,]),'LPAREN':([2,5,6,7,20,21,],[5,7,7,7,7,7,]),'=':([4,],[6,]),'STRING':([5,6,],[9,9,]),'NUMERO':([5,6,7,20,21,],[11,11,11,11,11,]),'INTERPOLACAO':([5,6,7,20,21,],[13,13,13,13,13,]),'CARACTER_ESPECIAL':([5,6,7,20,21,],[14,14,14,14,14,]),'CARACTER_ACENTUADO':([5,6,7,20,21,],[15,15,15,15,15,]),'CARACTER_NAO_IMPRIMIVEL':([5,6,7,20,21,],[16,16,16,16,16,]),'RPAREN':([8,9,10,11,12,13,14,15,16,18,22,23,24,],[19,-4,-5,-9,-10,-11,-12,-13,-14,22,-8,-6,-7,]),'PLUS':([10,11,12,13,14,15,16,18,22,23,24,],[20,-9,-10,-11,-12,-13,-14,20,-8,20,20,]),'MINUS':([10,11,12,13,14,15,16,18,22,23,24,],[21,-9,-10,-11,-12,-13,-14,21,-8,21,21,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'instrucao':([0,],[1,]),'atribuicao':([0,],[3,]),'valor':([5,6,],[8,17,]),'expressao':([5,6,7,20,21,],[10,10,18,23,24,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> instrucao","S'",1,None,None,None),
  ('instrucao -> ESCREVER LPAREN valor RPAREN','instrucao',4,'p_instrucao','parser_B.py',8),
  ('instrucao -> atribuicao','instrucao',1,'p_instrucao','parser_B.py',9),
  ('atribuicao -> IDENTIFICADOR = valor','atribuicao',3,'p_atribuicao','parser_B.py',14),
  ('valor -> STRING','valor',1,'p_valor','parser_B.py',18),
  ('valor -> expressao','valor',1,'p_valor','parser_B.py',19),
  ('expressao -> expressao PLUS expressao','expressao',3,'p_expressao','parser_B.py',23),
  ('expressao -> expressao MINUS expressao','expressao',3,'p_expressao','parser_B.py',24),
  ('expressao -> LPAREN expressao RPAREN','expressao',3,'p_expressao','parser_B.py',25),
  ('expressao -> NUMERO','expressao',1,'p_expressao','parser_B.py',26),
  ('expressao -> IDENTIFICADOR','expressao',1,'p_expressao','parser_B.py',27),
  ('expressao -> INTERPOLACAO','expressao',1,'p_expressao','parser_B.py',28),
  ('expressao -> CARACTER_ESPECIAL','expressao',1,'p_expressao','parser_B.py',29),
  ('expressao -> CARACTER_ACENTUADO','expressao',1,'p_expressao','parser_B.py',30),
  ('expressao -> CARACTER_NAO_IMPRIMIVEL','expressao',1,'p_expressao','parser_B.py',31),
]
