from sys import version
import ply.lex as lex
import ply.yacc as yacc
from catalog import catalog_manager,Table
import collections
catalog = None
tokens = (
    'LFPARENTH',
    'RGPARENTH',
    'TABLE',
    'CREATE',
    'INSERT',
    # 'UPDATE',
    'INTO',
    'VALUES',
    'SELECT',
    'COLUMN',
    "COMMA",
    'WHERE',
    'FROM',
    'AND',
    # 'SET',
    # 'EQUAL',
    'STAR',
    "END",
    "OP",
    "TYPE"
)


t_LFPARENTH = r'\('
t_RGPARENTH = r'\)'
t_SELECT = r'SELECT|select'
t_CREATE = r'CREATE|create'
t_INSERT = r'INSERT|insert'
# t_UPDATE = r'UPDATE|update'
t_INTO = r'INTO|into'
t_VALUES = r'VALUES|values'
t_WHERE = r'WHERE|where'
t_FROM = r'FROM|from'
t_AND = r'AND|and'
# t_SET = r'SET|set'
# t_EQUAL = r'\='
t_TABLE = r'TABLE|table'
t_COMMA = r','
t_STAR = r'\*'
t_END = r';'
t_OP = r'>|<|>=|<=|='
t_TYPE = r'INT|CHAR|FLOAT|int|char|float'


def t_COLUMN(t):
    r'[a-zA-Z0-9/.-]+'
    if t.value in ['FROM', 'from']:
        t.type = 'FROM'
    if t.value in ['CREATE', 'create']:
        t.type = 'CREATE'
    if t.value in ['TABLE', 'table']:
        t.type = 'TABLE'
    if t.value in ['INSERT', 'insert']:
        t.type = 'INSERT'
    if t.value in ['INTO', 'into']:
        t.type = 'INTO'
    if t.value in ['VALUES', 'values']:
        t.type = 'VALUES'
    # if t.value in ['UPDATE', 'update']:
    #     t.type = 'UPDATE'
    if t.value in ['SET', 'set']:
        t.type = 'SET'
    if t.value in ['WHERE', 'where']:
        t.type = 'WHERE'
    if t.value in ['SELECT', 'select']:
        t.type = 'SELECT'
    if t.value in ['AND', 'and']:
        t.type = 'AND'
    if t.value in ['INT','int','FLOAT','float','char','CHAR']:
        t.type = 'TYPE'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print("Illegal character {0}".format(t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()

datas = {}


class Stack(object):

    def __init__(self):
        self.is_columns = False
        self._stack = []

    def reset(self):
        self._stack = []

    def append(self, value):
        self._stack.append(value)

    def __iter__(self):
        return iter(self._stack)

    def __len__(self):
        return len(self._stack)

    def __str__(self):
        print(self._stack)
        return "stack"

    def __getitem__(self, item):
        return self._stack[item]

    def __setslice__(self, i, j, sequence):
        return self._stack[i:j]


stack = Stack()

condition_stack = Stack()

current_action = None

columns_dict = {}

condition_dict = {}


def reset_action():
    global current_action, stack, columns_dict, condition_dict,condition_stack
    current_action = None
    stack.reset()
    condition_stack.reset()
    columns_dict = {}
    condition_dict = {}


class Select(object):

    def __init__(self):
        self.columns = []
        self.conditions = []
        self.table = None

    def set_table(self, table):
        self.table = table
        return table in catalog.tables.keys()

    def add_columns(self, stack):
        [self.columns.append(v) for v in stack if v not in self.columns]
    def add_conditions(self,condition_stack):
        [self.conditions.append(v) for v in condition_stack if v not in self.conditions]
        

    def action(self):
        """展示数据"""
        if self.table not in catalog.tables.keys():
            print("table {0} not exists")
            return

        print("self.values",self.columns,self.conditions)



class Create(object):

    def __init__(self):
        self.values = []
        self.table = None

    def set_table(self, table):
        self.table = table
        return table not in catalog.tables.keys()
        # return table not in datas

    def add_stack(self, stack):
        [self.add_values(v) for v in stack if v not in self.values]

    def add_values(self, value):
        self.values.append(value)

    def action(self):
        print("create : ", self.values,"table : ",self.table)

class Insert(object):

    def __init__(self):
        self.values = []
        self.columns = set()
        self.table = None
        self._stack = None

    def set_table(self, table):
        self.table = table
        return table not in catalog.tables.keys()

    def add_stack(self, stack):
        # 判断是否输入的sql 为 insert into table(c1, c2, c3) values(1,2,3)
        self._stack = stack

    def action(self):
        if self._stack.is_columns:
            if len(self._stack) and len(self._stack) % 2 == 0:
                index = int(len(self._stack) / 2)
                if index != len(catalog.tables[self.table].attributes):
                    print("error default columns")
                    return
                attrs  = self._stack[:index]
                values = self._stack[index:]
                print(attrs,values)

            else:
                print(" error columns and values not equal")
                return
        else:
            if len(catalog.tables[self.table].attributes) != len(self._stack):
                print("input values len {0} not equal table columes len {1}".
                      format(len(self._stack), len(catalog.tables[self.table].attributes)))
                return
            self._stack._stack.reverse()
            print(self._stack)





def p_statement_expr(t):
    '''expressions : expression
                    | expressions expression'''
    if current_action:
        current_action.action()
    reset_action()


def p_expression_start(t):
    '''expression :  exp_select
                    | exp_create
                    | exp_insert'''


def p_expression_select(t):
    '''exp_select : SELECT columns FROM COLUMN END
                    | SELECT STAR FROM COLUMN END
                    | SELECT STAR FROM COLUMN WHERE exp_condition END
                    | SELECT columns FROM COLUMN WHERE exp_condition END'''
    print(t[1], t[2],t[3],t[4],t[5])
    global current_action
    current_action = Select()
    if not current_action.set_table(t[4]):
        print("{0} table not exists".format(t[4]))
        return
    if not t[2]:
        current_action.add_columns(stack)
    if t[5] == "where":
        current_action.add_conditions(condition_stack)


def p_expression_create(t):
    '''exp_create : CREATE TABLE COLUMN LFPARENTH exp_attribute RGPARENTH END'''
    print(t[1])
    global current_action
    current_action = Create()
    if not current_action.set_table(t[3]):
        print("{0} table already exists".format(t[3]))
        return
    # 处理参数
    current_action.add_stack(stack)
def p_expression_attribute(t):
    '''exp_attribute : COLUMN TYPE 
                     | COLUMN TYPE LFPARENTH COLUMN RGPARENTH
                     | COLUMN TYPE COMMA exp_attribute
                     | COLUMN TYPE LFPARENTH COLUMN RGPARENTH COMMA exp_attribute'''
    if len(t) > 3 and t[3] == '(':
        stack.append((t[1],t[2],t[4]))
    else:
        stack.append((t[1],t[2]))


def p_expression_insert(t):
    '''exp_insert : INSERT INTO COLUMN exp_insert_end'''
    print(t[1])
    global current_action
    current_action = Insert()
    if current_action.set_table(t[3]):
        print("{0} table not exists".format(t[3]))
        reset_action()
        return
    # 处理insert的参数
    current_action.add_stack(stack)



def p_expression_condition(t):
    '''exp_condition : COLUMN OP COLUMN
                     | COLUMN OP COLUMN AND exp_condition'''
    print("condition",t[1],t[2],t[3])
    condition_stack.append((t[1],t[2],t[3]))


def p_expresssion_insert_end(t):
    '''exp_insert_end : VALUES LFPARENTH columns RGPARENTH END
                      | LFPARENTH columns RGPARENTH VALUES LFPARENTH columns RGPARENTH END'''
    if len(t) == 9:
        stack.is_columns = True


def p_expression_columns(t):
    '''columns : COLUMN
               | COLUMN COMMA columns'''
    stack.append(t[1])


def p_error(p):
    if p:
        print("Syntax error at {0}".format(p.value))
    else:
        print("Syntax error at EOF")
def interpreter(data):
    yacc.yacc()
    yacc.parse(data)
def set_catalog(catalog_m):
    global catalog
    catalog = catalog_m
if __name__ == "__main__":
    catalog = catalog_manager()
    print(catalog.tables.keys())
    while True:
        data = input("sql>")
        yacc.yacc()
        yacc.parse(data)
