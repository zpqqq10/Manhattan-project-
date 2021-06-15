
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND CHAR COLUMN COMMA CREATE DELETE DROP END EXIT FROM INDEX INSERT INTO KEY LFPARENTH ON OP PRIMARY RGPARENTH SELECT STAR TABLE TYPE UNIQUE VALUES WHEREexpressions : expression\n                    | expressions expression\n                    | exp_exitexpression :  exp_select\n                    | exp_create_table\n                    | exp_create_index\n                    | exp_insert\n                    | exp_drop_table\n                    | exp_drop_index\n                    | exp_delete exp_exit : EXITexp_drop_table : DROP TABLE COLUMN ENDexp_drop_index : DROP INDEX COLUMN ENDexp_delete : DELETE  FROM COLUMN END\n                    | DELETE  FROM COLUMN WHERE exp_condition ENDexp_select : SELECT columns FROM COLUMN END\n                    | SELECT STAR FROM COLUMN END\n                    | SELECT STAR FROM COLUMN WHERE exp_condition END\n                    | SELECT columns FROM COLUMN WHERE exp_condition ENDexp_create_table : CREATE TABLE COLUMN LFPARENTH exp_attributes COMMA PRIMARY KEY LFPARENTH COLUMN RGPARENTH RGPARENTH ENDexp_create_index : CREATE INDEX COLUMN ON COLUMN LFPARENTH COLUMN RGPARENTH ENDexp_attributes : exp_attribute\n                      | exp_attributes COMMA exp_attributeexp_attribute : COLUMN TYPE \n                     | COLUMN CHAR LFPARENTH COLUMN RGPARENTH\n                     | COLUMN TYPE UNIQUE\n                     | COLUMN CHAR LFPARENTH COLUMN RGPARENTH UNIQUEexp_insert : INSERT INTO COLUMN exp_insert_endexp_condition : COLUMN OP COLUMN\n                     | COLUMN OP COLUMN AND exp_conditionexp_insert_end : VALUES LFPARENTH columns RGPARENTH END\n                      | LFPARENTH columns RGPARENTH VALUES LFPARENTH columns RGPARENTH ENDcolumns : COLUMN\n               | COLUMN COMMA columns'
    
_lr_action_items = {'EXIT':([0,],[11,]),'SELECT':([0,1,2,3,4,5,6,7,8,9,10,11,17,41,44,45,46,48,50,69,70,71,83,88,95,97,],[12,12,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-2,-28,-12,-13,-14,-16,-17,-15,-19,-18,-31,-21,-32,-20,]),'CREATE':([0,1,2,3,4,5,6,7,8,9,10,11,17,41,44,45,46,48,50,69,70,71,83,88,95,97,],[13,13,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-2,-28,-12,-13,-14,-16,-17,-15,-19,-18,-31,-21,-32,-20,]),'INSERT':([0,1,2,3,4,5,6,7,8,9,10,11,17,41,44,45,46,48,50,69,70,71,83,88,95,97,],[14,14,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-2,-28,-12,-13,-14,-16,-17,-15,-19,-18,-31,-21,-32,-20,]),'DROP':([0,1,2,3,4,5,6,7,8,9,10,11,17,41,44,45,46,48,50,69,70,71,83,88,95,97,],[15,15,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-2,-28,-12,-13,-14,-16,-17,-15,-19,-18,-31,-21,-32,-20,]),'DELETE':([0,1,2,3,4,5,6,7,8,9,10,11,17,41,44,45,46,48,50,69,70,71,83,88,95,97,],[16,16,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-2,-28,-12,-13,-14,-16,-17,-15,-19,-18,-31,-21,-32,-20,]),'$end':([1,2,3,4,5,6,7,8,9,10,11,17,41,44,45,46,48,50,69,70,71,83,88,95,97,],[0,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-2,-28,-12,-13,-14,-16,-17,-15,-19,-18,-31,-21,-32,-20,]),'STAR':([12,],[20,]),'COLUMN':([12,21,22,23,24,25,26,27,28,29,39,40,43,47,49,51,56,64,65,68,73,84,85,87,],[19,30,31,32,33,34,35,36,19,38,52,55,19,58,58,58,19,52,76,79,80,19,58,92,]),'TABLE':([13,15,],[21,24,]),'INDEX':([13,15,],[22,25,]),'INTO':([14,],[23,]),'FROM':([16,18,19,20,37,],[26,27,-33,29,-34,]),'RGPARENTH':([19,37,57,66,76,80,89,92,94,],[-33,-34,67,77,82,86,93,94,96,]),'COMMA':([19,53,54,62,72,75,86,91,],[28,64,-22,-24,-26,-23,-25,-27,]),'LFPARENTH':([30,32,42,55,63,78,81,],[39,43,56,65,73,84,87,]),'ON':([31,],[40,]),'VALUES':([32,67,],[42,78,]),'END':([33,34,35,36,38,59,60,61,77,79,82,90,93,96,],[44,45,46,48,50,69,70,71,83,-29,88,-30,95,97,]),'WHERE':([35,36,38,],[47,49,51,]),'TYPE':([52,],[62,]),'CHAR':([52,],[63,]),'OP':([58,],[68,]),'UNIQUE':([62,86,],[72,91,]),'PRIMARY':([64,],[74,]),'KEY':([74,],[81,]),'AND':([79,],[85,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expressions':([0,],[1,]),'expression':([0,1,],[2,17,]),'exp_exit':([0,],[3,]),'exp_select':([0,1,],[4,4,]),'exp_create_table':([0,1,],[5,5,]),'exp_create_index':([0,1,],[6,6,]),'exp_insert':([0,1,],[7,7,]),'exp_drop_table':([0,1,],[8,8,]),'exp_drop_index':([0,1,],[9,9,]),'exp_delete':([0,1,],[10,10,]),'columns':([12,28,43,56,84,],[18,37,57,66,89,]),'exp_insert_end':([32,],[41,]),'exp_attributes':([39,],[53,]),'exp_attribute':([39,64,],[54,75,]),'exp_condition':([47,49,51,85,],[59,60,61,90,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expressions","S'",1,None,None,None),
  ('expressions -> expression','expressions',1,'p_statement_expr','interpreter.py',323),
  ('expressions -> expressions expression','expressions',2,'p_statement_expr','interpreter.py',324),
  ('expressions -> exp_exit','expressions',1,'p_statement_expr','interpreter.py',325),
  ('expression -> exp_select','expression',1,'p_expression_start','interpreter.py',332),
  ('expression -> exp_create_table','expression',1,'p_expression_start','interpreter.py',333),
  ('expression -> exp_create_index','expression',1,'p_expression_start','interpreter.py',334),
  ('expression -> exp_insert','expression',1,'p_expression_start','interpreter.py',335),
  ('expression -> exp_drop_table','expression',1,'p_expression_start','interpreter.py',336),
  ('expression -> exp_drop_index','expression',1,'p_expression_start','interpreter.py',337),
  ('expression -> exp_delete','expression',1,'p_expression_start','interpreter.py',338),
  ('exp_exit -> EXIT','exp_exit',1,'p_expression_exit','interpreter.py',340),
  ('exp_drop_table -> DROP TABLE COLUMN END','exp_drop_table',4,'p_expression_drop_table','interpreter.py',345),
  ('exp_drop_index -> DROP INDEX COLUMN END','exp_drop_index',4,'p_expression_drop_index','interpreter.py',352),
  ('exp_delete -> DELETE FROM COLUMN END','exp_delete',4,'p_expression_delete','interpreter.py',359),
  ('exp_delete -> DELETE FROM COLUMN WHERE exp_condition END','exp_delete',6,'p_expression_delete','interpreter.py',360),
  ('exp_select -> SELECT columns FROM COLUMN END','exp_select',5,'p_expression_select','interpreter.py',370),
  ('exp_select -> SELECT STAR FROM COLUMN END','exp_select',5,'p_expression_select','interpreter.py',371),
  ('exp_select -> SELECT STAR FROM COLUMN WHERE exp_condition END','exp_select',7,'p_expression_select','interpreter.py',372),
  ('exp_select -> SELECT columns FROM COLUMN WHERE exp_condition END','exp_select',7,'p_expression_select','interpreter.py',373),
  ('exp_create_table -> CREATE TABLE COLUMN LFPARENTH exp_attributes COMMA PRIMARY KEY LFPARENTH COLUMN RGPARENTH RGPARENTH END','exp_create_table',13,'p_expression_create_table','interpreter.py',385),
  ('exp_create_index -> CREATE INDEX COLUMN ON COLUMN LFPARENTH COLUMN RGPARENTH END','exp_create_index',9,'p_expression_create_index','interpreter.py',396),
  ('exp_attributes -> exp_attribute','exp_attributes',1,'p_expression_attributes','interpreter.py',414),
  ('exp_attributes -> exp_attributes COMMA exp_attribute','exp_attributes',3,'p_expression_attributes','interpreter.py',415),
  ('exp_attribute -> COLUMN TYPE','exp_attribute',2,'p_expression_attribute','interpreter.py',417),
  ('exp_attribute -> COLUMN CHAR LFPARENTH COLUMN RGPARENTH','exp_attribute',5,'p_expression_attribute','interpreter.py',418),
  ('exp_attribute -> COLUMN TYPE UNIQUE','exp_attribute',3,'p_expression_attribute','interpreter.py',419),
  ('exp_attribute -> COLUMN CHAR LFPARENTH COLUMN RGPARENTH UNIQUE','exp_attribute',6,'p_expression_attribute','interpreter.py',420),
  ('exp_insert -> INSERT INTO COLUMN exp_insert_end','exp_insert',4,'p_expression_insert','interpreter.py',432),
  ('exp_condition -> COLUMN OP COLUMN','exp_condition',3,'p_expression_condition','interpreter.py',446),
  ('exp_condition -> COLUMN OP COLUMN AND exp_condition','exp_condition',5,'p_expression_condition','interpreter.py',447),
  ('exp_insert_end -> VALUES LFPARENTH columns RGPARENTH END','exp_insert_end',5,'p_expresssion_insert_end','interpreter.py',453),
  ('exp_insert_end -> LFPARENTH columns RGPARENTH VALUES LFPARENTH columns RGPARENTH END','exp_insert_end',8,'p_expresssion_insert_end','interpreter.py',454),
  ('columns -> COLUMN','columns',1,'p_expression_columns','interpreter.py',460),
  ('columns -> COLUMN COMMA columns','columns',3,'p_expression_columns','interpreter.py',461),
]
