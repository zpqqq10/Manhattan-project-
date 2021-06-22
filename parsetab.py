
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND CHAR COLUMN COMMA CREATE DELETE DROP END EQUAL EXECFILE EXIT FROM HELP INDEX INSERT INTO KEY LFPARENTH ON OP PRIMARY RGPARENTH SELECT SET SHOW STAR TABLE TYPE UNIQUE UPDATE VALUES WHEREexpressions : expression\n                    | expressions expression\n                    | exp_exitexpression :  exp_select\n                    | exp_create_table\n                    | exp_create_index\n                    | exp_insert\n                    | exp_drop_table\n                    | exp_drop_index\n                    | exp_delete\n                    | exp_execfile\n                    | exp_help\n                    | exp_show\n                    | exp_update exp_exit : EXIT END exp_update : UPDATE COLUMN SET exp_assign END\n                   | UPDATE COLUMN SET exp_assign WHERE exp_condition ENDexp_drop_table : DROP TABLE COLUMN ENDexp_assign : COLUMN EQUAL COLUMN\n                  | COLUMN EQUAL COLUMN COMMA exp_assignexp_drop_index : DROP INDEX COLUMN ENDexp_delete : DELETE  FROM COLUMN END\n                    | DELETE  FROM COLUMN WHERE exp_condition ENDexp_select : SELECT columns FROM COLUMN END\n                    | SELECT STAR FROM COLUMN END\n                    | SELECT STAR FROM COLUMN WHERE exp_condition END\n                    | SELECT columns FROM COLUMN WHERE exp_condition ENDexp_create_table : CREATE TABLE COLUMN LFPARENTH exp_attributes COMMA PRIMARY KEY LFPARENTH COLUMN RGPARENTH RGPARENTH ENDexp_create_index : CREATE INDEX COLUMN ON COLUMN LFPARENTH COLUMN RGPARENTH ENDexp_attributes : exp_attribute\n                      | exp_attributes COMMA exp_attributeexp_attribute : COLUMN TYPE \n                     | COLUMN CHAR LFPARENTH COLUMN RGPARENTH\n                     | COLUMN TYPE UNIQUE\n                     | COLUMN CHAR LFPARENTH COLUMN RGPARENTH UNIQUEexp_insert : INSERT INTO COLUMN exp_insert_endexp_condition : COLUMN OP COLUMN\n                     | COLUMN OP COLUMN AND exp_condition\n                     | COLUMN EQUAL COLUMN\n                     | COLUMN EQUAL COLUMN AND exp_conditionexp_insert_end : VALUES LFPARENTH columns RGPARENTH END\n                      | LFPARENTH columns RGPARENTH VALUES LFPARENTH columns RGPARENTH ENDcolumns : COLUMN\n               | COLUMN COMMA columns exp_show : SHOW END exp_execfile : EXECFILE COLUMN END exp_help : HELP END'
    
_lr_action_items = {'EXIT':([0,],[15,]),'SELECT':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,25,26,37,38,49,56,59,60,61,65,67,78,90,93,94,105,109,116,124,126,],[16,16,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-2,-15,-47,-45,-46,-36,-18,-21,-22,-24,-25,-16,-23,-27,-26,-17,-41,-29,-42,-28,]),'CREATE':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,25,26,37,38,49,56,59,60,61,65,67,78,90,93,94,105,109,116,124,126,],[17,17,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-2,-15,-47,-45,-46,-36,-18,-21,-22,-24,-25,-16,-23,-27,-26,-17,-41,-29,-42,-28,]),'INSERT':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,25,26,37,38,49,56,59,60,61,65,67,78,90,93,94,105,109,116,124,126,],[18,18,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-2,-15,-47,-45,-46,-36,-18,-21,-22,-24,-25,-16,-23,-27,-26,-17,-41,-29,-42,-28,]),'DROP':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,25,26,37,38,49,56,59,60,61,65,67,78,90,93,94,105,109,116,124,126,],[19,19,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-2,-15,-47,-45,-46,-36,-18,-21,-22,-24,-25,-16,-23,-27,-26,-17,-41,-29,-42,-28,]),'DELETE':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,25,26,37,38,49,56,59,60,61,65,67,78,90,93,94,105,109,116,124,126,],[20,20,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-2,-15,-47,-45,-46,-36,-18,-21,-22,-24,-25,-16,-23,-27,-26,-17,-41,-29,-42,-28,]),'EXECFILE':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,25,26,37,38,49,56,59,60,61,65,67,78,90,93,94,105,109,116,124,126,],[21,21,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-2,-15,-47,-45,-46,-36,-18,-21,-22,-24,-25,-16,-23,-27,-26,-17,-41,-29,-42,-28,]),'HELP':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,25,26,37,38,49,56,59,60,61,65,67,78,90,93,94,105,109,116,124,126,],[22,22,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-2,-15,-47,-45,-46,-36,-18,-21,-22,-24,-25,-16,-23,-27,-26,-17,-41,-29,-42,-28,]),'SHOW':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,25,26,37,38,49,56,59,60,61,65,67,78,90,93,94,105,109,116,124,126,],[23,23,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-2,-15,-47,-45,-46,-36,-18,-21,-22,-24,-25,-16,-23,-27,-26,-17,-41,-29,-42,-28,]),'UPDATE':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,25,26,37,38,49,56,59,60,61,65,67,78,90,93,94,105,109,116,124,126,],[24,24,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-2,-15,-47,-45,-46,-36,-18,-21,-22,-24,-25,-16,-23,-27,-26,-17,-41,-29,-42,-28,]),'$end':([1,2,3,4,5,6,7,8,9,10,11,12,13,14,25,26,37,38,49,56,59,60,61,65,67,78,90,93,94,105,109,116,124,126,],[0,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-2,-15,-47,-45,-46,-36,-18,-21,-22,-24,-25,-16,-23,-27,-26,-17,-41,-29,-42,-28,]),'END':([15,22,23,36,46,47,48,51,53,64,76,80,81,91,92,100,102,103,108,113,118,119,122,125,],[26,37,38,49,59,60,61,65,67,78,90,93,94,-19,105,109,-37,-39,116,-20,-38,-40,124,126,]),'STAR':([16,],[29,]),'COLUMN':([16,21,24,30,31,32,33,34,35,40,41,42,50,54,55,58,62,66,68,73,77,79,84,85,88,89,96,104,110,111,112,115,],[28,36,39,43,44,45,46,47,48,51,28,53,63,69,72,28,75,75,75,28,91,75,69,99,102,103,106,63,28,75,75,121,]),'TABLE':([17,19,],[30,33,]),'INDEX':([17,19,],[31,34,]),'INTO':([18,],[32,]),'FROM':([20,27,28,29,52,],[35,40,-43,42,-44,]),'RGPARENTH':([28,52,74,86,99,106,117,121,123,],[-43,-44,87,100,108,114,122,123,125,]),'COMMA':([28,70,71,82,91,95,98,114,120,],[41,84,-30,-32,104,-34,-31,-33,-35,]),'SET':([39,],[50,]),'LFPARENTH':([43,45,57,72,83,101,107,],[54,58,73,85,96,110,115,]),'ON':([44,],[55,]),'VALUES':([45,87,],[57,101,]),'WHERE':([48,51,53,64,91,113,],[62,66,68,79,-19,-20,]),'EQUAL':([63,75,],[77,89,]),'TYPE':([69,],[82,]),'CHAR':([69,],[83,]),'OP':([75,],[88,]),'UNIQUE':([82,114,],[95,120,]),'PRIMARY':([84,],[97,]),'KEY':([97,],[107,]),'AND':([102,103,],[111,112,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expressions':([0,],[1,]),'expression':([0,1,],[2,25,]),'exp_exit':([0,],[3,]),'exp_select':([0,1,],[4,4,]),'exp_create_table':([0,1,],[5,5,]),'exp_create_index':([0,1,],[6,6,]),'exp_insert':([0,1,],[7,7,]),'exp_drop_table':([0,1,],[8,8,]),'exp_drop_index':([0,1,],[9,9,]),'exp_delete':([0,1,],[10,10,]),'exp_execfile':([0,1,],[11,11,]),'exp_help':([0,1,],[12,12,]),'exp_show':([0,1,],[13,13,]),'exp_update':([0,1,],[14,14,]),'columns':([16,41,58,73,110,],[27,52,74,86,117,]),'exp_insert_end':([45,],[56,]),'exp_assign':([50,104,],[64,113,]),'exp_attributes':([54,],[70,]),'exp_attribute':([54,84,],[71,98,]),'exp_condition':([62,66,68,79,111,112,],[76,80,81,92,118,119,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expressions","S'",1,None,None,None),
  ('expressions -> expression','expressions',1,'p_statement_expr','interpreter.py',435),
  ('expressions -> expressions expression','expressions',2,'p_statement_expr','interpreter.py',436),
  ('expressions -> exp_exit','expressions',1,'p_statement_expr','interpreter.py',437),
  ('expression -> exp_select','expression',1,'p_expression_start','interpreter.py',444),
  ('expression -> exp_create_table','expression',1,'p_expression_start','interpreter.py',445),
  ('expression -> exp_create_index','expression',1,'p_expression_start','interpreter.py',446),
  ('expression -> exp_insert','expression',1,'p_expression_start','interpreter.py',447),
  ('expression -> exp_drop_table','expression',1,'p_expression_start','interpreter.py',448),
  ('expression -> exp_drop_index','expression',1,'p_expression_start','interpreter.py',449),
  ('expression -> exp_delete','expression',1,'p_expression_start','interpreter.py',450),
  ('expression -> exp_execfile','expression',1,'p_expression_start','interpreter.py',451),
  ('expression -> exp_help','expression',1,'p_expression_start','interpreter.py',452),
  ('expression -> exp_show','expression',1,'p_expression_start','interpreter.py',453),
  ('expression -> exp_update','expression',1,'p_expression_start','interpreter.py',454),
  ('exp_exit -> EXIT END','exp_exit',2,'p_expression_exit','interpreter.py',458),
  ('exp_update -> UPDATE COLUMN SET exp_assign END','exp_update',5,'p_expression_update','interpreter.py',464),
  ('exp_update -> UPDATE COLUMN SET exp_assign WHERE exp_condition END','exp_update',7,'p_expression_update','interpreter.py',465),
  ('exp_drop_table -> DROP TABLE COLUMN END','exp_drop_table',4,'p_expression_drop_table','interpreter.py',477),
  ('exp_assign -> COLUMN EQUAL COLUMN','exp_assign',3,'p_expression_assign','interpreter.py',485),
  ('exp_assign -> COLUMN EQUAL COLUMN COMMA exp_assign','exp_assign',5,'p_expression_assign','interpreter.py',486),
  ('exp_drop_index -> DROP INDEX COLUMN END','exp_drop_index',4,'p_expression_drop_index','interpreter.py',489),
  ('exp_delete -> DELETE FROM COLUMN END','exp_delete',4,'p_expression_delete','interpreter.py',498),
  ('exp_delete -> DELETE FROM COLUMN WHERE exp_condition END','exp_delete',6,'p_expression_delete','interpreter.py',499),
  ('exp_select -> SELECT columns FROM COLUMN END','exp_select',5,'p_expression_select','interpreter.py',510),
  ('exp_select -> SELECT STAR FROM COLUMN END','exp_select',5,'p_expression_select','interpreter.py',511),
  ('exp_select -> SELECT STAR FROM COLUMN WHERE exp_condition END','exp_select',7,'p_expression_select','interpreter.py',512),
  ('exp_select -> SELECT columns FROM COLUMN WHERE exp_condition END','exp_select',7,'p_expression_select','interpreter.py',513),
  ('exp_create_table -> CREATE TABLE COLUMN LFPARENTH exp_attributes COMMA PRIMARY KEY LFPARENTH COLUMN RGPARENTH RGPARENTH END','exp_create_table',13,'p_expression_create_table','interpreter.py',527),
  ('exp_create_index -> CREATE INDEX COLUMN ON COLUMN LFPARENTH COLUMN RGPARENTH END','exp_create_index',9,'p_expression_create_index','interpreter.py',542),
  ('exp_attributes -> exp_attribute','exp_attributes',1,'p_expression_attributes','interpreter.py',566),
  ('exp_attributes -> exp_attributes COMMA exp_attribute','exp_attributes',3,'p_expression_attributes','interpreter.py',567),
  ('exp_attribute -> COLUMN TYPE','exp_attribute',2,'p_expression_attribute','interpreter.py',571),
  ('exp_attribute -> COLUMN CHAR LFPARENTH COLUMN RGPARENTH','exp_attribute',5,'p_expression_attribute','interpreter.py',572),
  ('exp_attribute -> COLUMN TYPE UNIQUE','exp_attribute',3,'p_expression_attribute','interpreter.py',573),
  ('exp_attribute -> COLUMN CHAR LFPARENTH COLUMN RGPARENTH UNIQUE','exp_attribute',6,'p_expression_attribute','interpreter.py',574),
  ('exp_insert -> INSERT INTO COLUMN exp_insert_end','exp_insert',4,'p_expression_insert','interpreter.py',587),
  ('exp_condition -> COLUMN OP COLUMN','exp_condition',3,'p_expression_condition','interpreter.py',599),
  ('exp_condition -> COLUMN OP COLUMN AND exp_condition','exp_condition',5,'p_expression_condition','interpreter.py',600),
  ('exp_condition -> COLUMN EQUAL COLUMN','exp_condition',3,'p_expression_condition','interpreter.py',601),
  ('exp_condition -> COLUMN EQUAL COLUMN AND exp_condition','exp_condition',5,'p_expression_condition','interpreter.py',602),
  ('exp_insert_end -> VALUES LFPARENTH columns RGPARENTH END','exp_insert_end',5,'p_expresssion_insert_end','interpreter.py',608),
  ('exp_insert_end -> LFPARENTH columns RGPARENTH VALUES LFPARENTH columns RGPARENTH END','exp_insert_end',8,'p_expresssion_insert_end','interpreter.py',609),
  ('columns -> COLUMN','columns',1,'p_expression_columns','interpreter.py',615),
  ('columns -> COLUMN COMMA columns','columns',3,'p_expression_columns','interpreter.py',616),
  ('exp_show -> SHOW END','exp_show',2,'p_expression_show','interpreter.py',621),
  ('exp_execfile -> EXECFILE COLUMN END','exp_execfile',3,'p_expression_execfile','interpreter.py',626),
  ('exp_help -> HELP END','exp_help',2,'p_expression_help','interpreter.py',631),
]
