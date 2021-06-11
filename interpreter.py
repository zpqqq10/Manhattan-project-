import ply.lex as lex
import ply.yacc as yacc
from catalog import catalog_manager
import collections

tokens = (
    'LFPARENTH',
    'RGPARENTH',
    'TABLE',
    'CREATE',
    'INSERT',
    'UPDATE',
    'INTO',
    'VALUES',
    'SELECT',
    'COLUMN',
    "COMMA",
    'WHERE',
    'FROM',
    'AND',
    'SET',
    'EQUAL',
    'STAR',
    "END"
)


t_LFPARENTH = r'\('
t_RGPARENTH = r'\)'
t_SELECT = r'SELECT|select'
t_CREATE = r'CREATE|create'
t_INSERT = r'INSERT|insert'
t_UPDATE = r'UPDATE|update'
t_INTO = r'INTO|into'
t_VALUES = r'VALUES|values'
t_WHERE = r'WHERE|where'
t_FROM = r'FROM|from'
t_AND = r'AND|and'
t_SET = r'SET|set'
t_EQUAL = r'\='
t_TABLE = r'TABLE|table'
t_COMMA = r','
t_STAR = r'\*'
t_END = r';'


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
    if t.value in ['UPDATE', 'update']:
        t.type = 'UPDATE'
    if t.value in ['SET', 'set']:
        t.type = 'SET'
    if t.value in ['WHERE', 'where']:
        t.type = 'WHERE'
    if t.value in ['SELECT', 'select']:
        t.type = 'SELECT'
    if t.value in ['AND', 'and']:
        t.type = 'AND'
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

current_action = None

columns_dict = {}

condition_dict = {}


def reset_action():
    global current_action, stack, columns_dict, condition_dict
    current_action = None
    stack.reset()
    columns_dict = {}
    condition_dict = {}


class Select(object):

    def __init__(self):
        self.values = []
        self.table = None

    def set_table(self, table):
        self.table = table
        return table in datas

    def add_stack(self, stack):
        [self.add_values(v) for v in stack if v not in self.values]

    def add_values(self, value):
        self.values.append(value)

    def action(self):
        """展示数据"""
        if self.table not in datas:
            print("table {0} not exists")
            return
        table = datas[self.table]
        if self.values:
            for v in self.values:
                if v in table:
                    print("   {0} = {1}".format(v, table[v]))
                else:
                    print("   {0} not in table {1}".format(v, self.table))
        else:
            for v in table:
                print("   {0} = {1}".format(v, table[v]))


class Create(object):

    def __init__(self):
        self.values = []
        self.table = None

    def set_table(self, table):
        self.table = table
        return catalog.table_not_exists(table)
        # return table not in datas

    def add_stack(self, stack):
        [self.add_values(v) for v in stack if v not in self.values]

    def add_values(self, value):
        self.values.append(value)

    def action(self):
        datas[self.table] = collections.OrderedDict()
        for v in self.values:
            datas[self.table][v] = []
        print("create : ", datas)


class Insert(object):

    def __init__(self):
        self.values = []
        self.columns = set()
        self.table = None
        self._stack = None

    def set_table(self, table):
        self.table = table
        return table not in datas

    def add_stack(self, stack):
        # 判断是否输入的sql 为 insert into table(c1, c2, c3) values(1,2,3)
        self._stack = stack

    def action(self):
        table = datas[self.table]
        if self._stack.is_columns:
            if len(self._stack) and len(self._stack) % 2 == 0:
                index = int(len(self._stack) / 2)
                if index != len(table.keys()):
                    print("error default columns")
                    return
                for i in range(index):
                    if self._stack[i] in table:
                        table[self._stack[i]].append(self._stack[i + index])

            else:
                print(" error columns and values not equal")
                return
        else:
            if len(table.keys()) != len(self._stack):
                print("input values len {0} not equal table columes len {1}".
                      format(len(self._stack), len(table.keys())))
                return
            t_index = 0
            for v in table.keys():
                table[v].append(self._stack[t_index])
                t_index += 1
        print("insert : ", datas)


class Update(object):

    def __init__(self):
        self.values = []
        self.table = None
        self.condition_dict = {}
        self.columns_dict = {}
        self.index_list = None

    def set_table(self, table):
        self.table = table
        return table not in datas

    def add_stack(self, condition, colums):
        self.condition_dict = condition
        self.columns_dict = colums

    def check_dict_key(self, val_dict, table):
        for key in val_dict.keys():
            if key not in table:
                return False
        return True

    def find_keys(self, val_dict, table):
        keys = [key for key in val_dict]
        values = [val_dict[key] for key in val_dict]
        self.index_list = []
        print(keys)
        print(table)
        result_list = []
        if keys:
            first_line = table[keys[0]]
            for i in range(len(first_line)):
                detail_value = []
                for key in keys:
                    detail_value.append(table[key][i])
                result_list.append(detail_value)

        print(values)
        print(result_list)
        for index, v in enumerate(result_list):
            if v == values:
                self.index_list.append(index)

        print(self.index_list)
        return self.index_list

    def action(self):
        table = datas[self.table]
        if not (self.check_dict_key(self.condition_dict, table) and\
                self.check_dict_key(self.columns_dict, table)):
            print(" error found keys ")
            return
        index_list = self.find_keys(self.condition_dict, table)
        if not index_list:
            print(" update condition not found")
            return
        for k in self.columns_dict:
            for index in index_list:
                table[k][index] = self.columns_dict[k]


def p_statement_expr(t):
    '''expressions : expression
                    | expressions expression'''
    if current_action:
        current_action.action()
    reset_action()


def p_expression_start(t):
    '''expression :  exp_select
                    | exp_create
                    | exp_insert
                    | exp_update'''


def p_expression_select(t):
    '''exp_select : SELECT columns FROM COLUMN END
                    | SELECT STAR FROM COLUMN END'''
    print(t[1], t[2])
    global current_action
    current_action = Select()
    if not current_action.set_table(t[4]):
        print("{0} table not exists".format(t[4]))
        return
    if not t[2]:
        current_action.add_stack(stack)


def p_expression_create(t):
    '''exp_create : CREATE TABLE COLUMN LFPARENTH columns RGPARENTH END'''
    print(t[1])
    global current_action
    current_action = Create()
    if not current_action.set_table(t[3]):
        print("{0} table already exists".format(t[3]))
        return
    # 处理参数
    current_action.add_stack(stack)


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


def p_expression_update(t):
    '''exp_update : UPDATE COLUMN SET exp_update_colums WHERE exp_update_condition END'''
    print(t[1])
    global current_action
    current_action = Update()
    if current_action.set_table(t[2]):
        print("{0} table not exists".format(t[2]))
        return
    print(condition_dict, columns_dict)
    current_action.add_stack(condition_dict, columns_dict)


def p_expression_update_columns(t):
    '''exp_update_colums : COLUMN EQUAL COLUMN
                         | COLUMN EQUAL COLUMN COMMA exp_update_colums'''

    columns_dict[t[1]] = t[3]


def p_expression_update_condition(t):
    '''exp_update_condition : COLUMN EQUAL COLUMN
                            | COLUMN EQUAL COLUMN AND exp_update_condition'''
    condition_dict[t[1]] = t[3]


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
if __name__ == "__main__":
    catalog = catalog_manager()
    while True:
        data = input("sql>")
        yacc.yacc()
        yacc.parse(data)
