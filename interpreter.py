from posixpath import join
from sys import version
import ply.lex as lex
import ply.yacc as yacc
from catalog import catalog_manager, Table
import collections
import time
import traceback
# global variables for each manager
catalog = None
record = None
index = None

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
    "END",
    "OP",
    "TYPE",
    "EXIT",
    "PRIMARY",
    "UNIQUE",
    "CHAR",
    "KEY",
    "DROP",
    "DELETE",
    "INDEX",
    "ON",
    "EXECFILE",
    "HELP",
    "SHOW",
    "IMPORT",
    "EXPORT"
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
t_EQUAL = r'='
t_TABLE = r'TABLE|table'
t_COMMA = r','
t_STAR = r'\*'
t_END = r';'
t_OP = r'<>|>=|<=|<|>'
t_TYPE = r'INT|FLOAT|int|float'
t_CHAR = r'CHAR|char'
t_EXIT = r'QUIT|quit|EXIT|exit'
t_PRIMARY = r'primary|PRIMARY'
t_KEY = r'KEY|key'
t_UNIQUE = r'UNIQUE|unique'
t_DROP = r'DROP|drop'
t_DELETE = r'DELETE|delete'
t_INDEX = r'index|INDEX'
t_ON = r'ON|on'
t_EXECFILE = r'EXECFILE|execfile'
t_HELP = r'HELP|help'
t_SHOW = r'SHOW|show'
t_IMPORT = r'import|IMPORT'
t_EXPORT = r'export|EXPORT'
# ''' '"[a-zA-Z0-9/ '_.-]+"|'[a-zA-Z0-9/ "_.-]+'| '''


def t_COLUMN(t):
    # r'[a-zA-Z0-9/_.-]+'
    r''' "[a-zA-Z0-9/ '_.-]+"|'[a-zA-Z0-9/ "_.-]+'|[a-zA-Z0-9/_.-]+ '''
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
    if t.value in ['INT', 'int', 'FLOAT', 'float']:
        t.type = 'TYPE'
    if t.value in ['char', 'CHAR']:
        t.type = 'CHAR'
    if t.value in ['QUIT', 'quit', 'EXIT', 'exit']:
        t.type = 'EXIT'
    if t.value in ['PRIMARY', 'primary']:
        t.type = 'PRIMARY'
    if t.value in ['KEY', 'key']:
        t.type = 'KEY'
    if t.value in ['UNIQUE', 'unique']:
        t.type = 'UNIQUE'
    if t.value in ['DROP', 'drop']:
        t.type = 'DROP'
    if t.value in ['DELETE', 'delete']:
        t.type = 'DELETE'
    if t.value in ['ON', 'on']:
        t.type = 'ON'
    if t.value in ['index', 'INDEX']:
        t.type = 'INDEX'
    if t.value in ['EXECFILE', 'execfile']:
        t.type = 'EXECFILE'
    if t.value in ['HELP', 'help']:
        t.type = 'HELP'
    if t.value in ['SHOW', 'show']:
        t.type = 'SHOW'
    if t.value in ['import', 'IMPORT']:
        t.type = 'IMPORT'
    if t.value in ['export', 'EXPORT']:
        t.type = 'EXPORT'
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

        return

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
    global current_action, stack, columns_dict, condition_dict, condition_stack
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

    def add_conditions(self, condition_stack):
        [self.conditions.append(v)
         for v in condition_stack if v not in self.conditions]

    def action(self):
        """????????????"""
        start = time.time()
        self.columns.reverse()
        api.select(self.table, self.columns, self.conditions)
        # print(self.table, self.columns, self.conditions)
        end = time.time()
        print('Duration: %fs' % (end - start))


class Delete(object):

    def __init__(self):
        self.columns = []
        self.conditions = []
        self.table = None

    def set_table(self, table):
        self.table = table
        return table in catalog.tables.keys()

    def add_conditions(self, condition_stack):
        [self.conditions.append(v)
         for v in condition_stack if v not in self.conditions]

    def action(self):
        """????????????"""
        start = time.time()
        api.delete_record(self.table, self.conditions)
        end = time.time()
        print('Duration: %fs' % (end - start))


class Create(object):
    def __init__(self):
        self.values = []
        self.table = None
        self.primary = ""
        self.attr = None
        self.is_Index = False
        self.skip = False
        self.from_import = None

    def set_table(self, table):
        self.table = table
        return table not in catalog.tables.keys()
        # return table not in datas

    def set_index(self, index):
        self.index = index
        return index not in catalog.indices.keys()

    def set_attr(self, attr):
        self.attr = attr
        return attr in [item.name for item in catalog.tables[self.table].attributes]

    def add_stack(self, stack):
        [self.add_values(v) for v in stack if v not in self.values]

    def add_values(self, value):
        self.values.append(value)

    def set_primary(self, value):
        self.primary = value

    def action(self):
        # the last value of the attribute tuple is whether the attribute is unique
        if self.is_Index:
            # create an index
            start = time.time()
            # print("Create Index on attribute ", self.attr, " of ",
            #       self.table, ", named as ", self.index)
            api.create_index(self.index, self.table, self.attr)
            print("Successfully create index '%s'" % self.index)
            end = time.time()
            print('Duration: %fs' % (end - start))
        else:
            # create a table
            start = time.time()
            attr = [item[0] for item in self.values]
            if self.primary not in attr:
                reset_action()
                raise Exception(
                    'SYNTAX Error: Invalid primary key! Check if it is in the attributes list.')
                # print("error PRIMARY KEY")
                # return
            # print("create : ", self.values, "table : ",
            #       self.table, "primary : ", self.primary)
            api.create_table(self.table, self.primary, self.values)
            print("Successfully create table '%s'" % self.table)
            if self.from_import:
                try:
                    f = open(self.from_import, 'r')
                    attr = f.readline()
                    attr = attr.strip().split(',')
                    for i in range(len(attr)):
                        if self.values[i][0] != attr[i]:
                            raise Exception(
                                "SYNTAX Error: Invalid attribute name %s" % self.values[i][0])
                    datas = f.readlines()
                    f.close()

                    for item in datas:
                        if item == datas[-1]:
                            j = item.split(',')
                            api.insert_record(self.table, j)
                        else:
                            j = item.split(',')
                            j[-1] = j[-1].strip('\n')
                            api.insert_record(self.table, j, import_flag=True)
                    print('%d rows affected' % len(datas))

                except:
                    api.drop_table(self.table)
                    raise
            end = time.time()
            print('Duration: %fs' % (end - start))


class Insert(object):

    def __init__(self):
        self.values = []
        self.columns = set()
        self.table = None
        self._stack = None
        self.skip = False

    def set_table(self, table):
        self.table = table
        return table not in catalog.tables.keys()

    def add_stack(self, stack):
        # ?????????????????????sql ??? insert into table(c1, c2, c3) values(1,2,3)
        self._stack = stack

    def action(self):
        if self._stack.is_columns:
            if len(self._stack) and len(self._stack) % 2 == 0:
                start = time.time()
                index = int(len(self._stack) / 2)
                if index != len(catalog.tables[self.table].attributes):
                    reset_action()
                    raise Exception('SYNTAX Error: Invalid default columns.')
                    # print("error default columns")
                    # return
                attrs = self._stack[:index]
                values = self._stack[index:]
                print("Insert with columns: attributes:",
                      attrs, "values:", values)
                api.insert_record(self.table, values, attrs)
                end = time.time()
                print('Duration: %fs' % (end - start))
            else:
                reset_action()
                raise Exception(
                    "SYNTAX Error: The number of input colomns is not equal to the number of input value.")
                # print(" error columns and values not equal")
                # return
        else:
            if len(catalog.tables[self.table].attributes) != len(self._stack):
                reset_action()
                raise Exception("INVALID VALUE Error: Input values len {0} not equal table columes len {1}".
                                format(len(self._stack), len(catalog.tables[self.table].attributes)))
                # return
            start = time.time()
            self._stack._stack.reverse()
            api.insert_record(self.table, self._stack._stack)
            print('1 row affected')
            print('Successfully insert')
            end = time.time()
            print('Duration: %fs' % (end - start))
            # print("Insert without columns: values:", self._stack)
            # print(self.table)


class Update(object):
    def __init__(self):
        self.table = None
        self.conditions = []
        self.fields = []

    def set_table(self, table):
        self.table = table
        return table in catalog.tables.keys()

    def add_conditions(self, condition_stack):
        [self.conditions.append(v)
         for v in condition_stack if v not in self.conditions]

    def add_fields(self, stack):
        [self.fields.append(v) for v in stack]

    def action(self):
        start = time.time()
        api.update(self.table, self.conditions, self.fields)
        end = time.time()
        print('Duration: %fs' % (end - start))
        # print(self.conditions)
        # print(self.fields)


class Drop(object):
    def __init__(self):
        self.table = None
        self.index = None

    def set_table(self, table):
        self.table = table
        return table in catalog.tables.keys()

    def set_index(self, index):
        self.index = index
        return index in catalog.indices.keys()

    def action(self):
        global catalog
        if self.table and self.table in catalog.tables.keys():
            start = time.time()
            api.drop_table(self.table)
            print("Successfully drop table '%s'" % self.table)
            end = time.time()
            print('Duration: %fs' % (end - start))
        if self.index and self.index in catalog.indices.keys():
            start = time.time()
            api.drop_index(self.index)
            print("Successfully drop index '%s'" % self.index)
            end = time.time()
            print('Duration: %fs' % (end - start))


class Help(object):
    def __init__(self):
        pass

    def action(self):
        print('----------------Minisql------------------')
        print('-----Developed by Cheung, SoonWhy and N7Utb-----')
        print('Support: ')
        print('- create a table')
        print('- create an index')
        print('- drop a table')
        print('- drop an index')
        print('- insert records into a table')
        print('- delete records from a table')
        print('- select from a table')
        print('- execute instructions in a file')
        print('- extra: use update instruction to update records in a table')
        print('- extra: use show instruction to view information of tables or indices')
        print('- extra: use import instruction to build a table with data from a csv file')
        print('- extra: use export instruction to output a table into a csv file')
        print('- enter "exit" or "quit" to exit Minisql')


def p_statement_expr(t):
    '''expressions : expression
                    | expressions expression
                    | exp_exit'''
    try:
        if current_action:
            current_action.action()
        reset_action()
    except Exception as e:
        reset_action()
        raise


def p_expression_start(t):
    '''expression :  exp_select
                    | exp_create_table
                    | exp_create_index
                    | exp_insert
                    | exp_drop_table
                    | exp_drop_index
                    | exp_delete
                    | exp_execfile
                    | exp_help
                    | exp_show_table
                    | exp_show_index
                    | exp_show
                    | exp_update
                    | exp_import
                    | exp_export'''


def p_expression_exit(t):
    ''' exp_exit : EXIT END'''
    api.exit()
    print("Goodbye")
    # a close method in api,commit the buffer and so on
    exit(1)


def p_expression_update(t):
    ''' exp_update : UPDATE COLUMN SET exp_assign END
                   | UPDATE COLUMN SET exp_assign WHERE exp_condition END'''
    global current_action
    current_action = Update()
    if not current_action.set_table(t[2]):
        reset_action()
        raise Exception(
            "INVALID IDENTIFIER Error: {0} table not exists".format(t[2]))
    if len({item[0] for item in stack._stack}) != len(stack._stack):
        reset_action()
        raise Exception("INVALID IDENTIFIER Error: update fields duplicate")
    current_action.add_conditions(condition_stack)
    current_action.add_fields(stack)


def p_expression_drop_table(t):
    '''exp_drop_table : DROP TABLE COLUMN END'''
    global current_action
    current_action = Drop()
    if not current_action.set_table(t[3]):
        reset_action()
        raise Exception(
            "INVALID IDENTIFIER Error: {0} table not exists".format(t[3]))


def p_expression_assign(t):
    '''exp_assign : COLUMN EQUAL COLUMN
                  | COLUMN EQUAL COLUMN COMMA exp_assign'''
    stack.append((t[1], t[3]))


def p_expression_drop_index(t):
    '''exp_drop_index : DROP INDEX COLUMN END'''
    global current_action
    current_action = Drop()
    if not current_action.set_index(t[3]):
        reset_action()
        raise Exception(
            "INVALID IDENTIFIER Error: {0} index not exists".format(t[3]))


def p_expression_delete(t):
    '''exp_delete : DELETE  FROM COLUMN END
                    | DELETE  FROM COLUMN WHERE exp_condition END'''
    global current_action
    current_action = Delete()
    if not current_action.set_table(t[3]):
        reset_action()
        raise Exception(
            "INVALID IDENTIFIER Error: {0} table not exists".format(t[3]))
    if t[4] == "where":
        current_action.add_conditions(condition_stack)


def p_expression_select(t):
    '''exp_select : SELECT columns FROM COLUMN END
                    | SELECT STAR FROM COLUMN END
                    | SELECT STAR FROM COLUMN WHERE exp_condition END
                    | SELECT columns FROM COLUMN WHERE exp_condition END'''
    global current_action
    current_action = Select()

    if not current_action.set_table(t[4]):
        reset_action()
        raise Exception(
            "INVALID IDENTIFIER Error: {0} table not exists".format(t[4]))
    if not t[2]:
        current_action.add_columns(stack)
    if t[5] == "where":
        current_action.add_conditions(condition_stack)


def p_expression_create_table(t):
    '''exp_create_table : CREATE TABLE COLUMN LFPARENTH exp_attributes COMMA PRIMARY KEY LFPARENTH COLUMN RGPARENTH RGPARENTH END'''
    global current_action
    current_action = Create()
    if not current_action.set_table(t[3]):
        reset_action()
        raise Exception(
            "INVALID IDENTIFIER Error: {0} table already exists".format(t[3]))
    # ????????????
    current_action.skip = False
    current_action.is_Index = False
    current_action.from_import = None
    current_action.set_primary(t[10])
    current_action.add_stack(stack)


def p_expression_create_index(t):
    '''exp_create_index : CREATE INDEX COLUMN ON COLUMN LFPARENTH COLUMN RGPARENTH END'''
    global current_action
    current_action = Create()
    if current_action.set_table(t[5]):
        reset_action()
        raise Exception(
            "INVALID IDENTIFIER Error: {0} table doesn't exist".format(t[5]))

    if not current_action.set_index(t[3]):
        reset_action()
        raise Exception(
            'INVALID IDENTIFIER Error: {0} index already exists'.format(t[3]))

    if not current_action.set_attr(t[7]):
        reset_action()
        raise Exception(
            "INVALID IDENTIFIER Error: {0} attr doesn't exists".format(t[7]))
    current_action.from_import = False
    current_action.is_Index = True
    # ????????????

# def p_expression_key(t):
#     '''exp_key : PRIMARY KEY LFPARENTH COLUMN RGPARENTH'''


def p_expression_attributes(t):
    '''exp_attributes : exp_attribute
                      | exp_attributes COMMA exp_attribute'''


def p_expression_attribute(t):
    '''exp_attribute : COLUMN TYPE 
                     | COLUMN CHAR LFPARENTH COLUMN RGPARENTH
                     | COLUMN TYPE UNIQUE
                     | COLUMN CHAR LFPARENTH COLUMN RGPARENTH UNIQUE'''

    if len(t) == 7:
        stack.append((t[1], t[2], t[4], 1))
    elif len(t) == 6:
        stack.append((t[1], t[2], t[4], 0))
    elif len(t) == 4:
        stack.append((t[1], t[2], 4, 1))
    else:
        stack.append((t[1], t[2], 4, 0))


def p_expression_insert(t):
    '''exp_insert : INSERT INTO COLUMN exp_insert_end'''
    global current_action
    current_action = Insert()
    if current_action.set_table(t[3]):
        reset_action()
        raise Exception(
            "INVALID IDENTIFIER Error: {0} table not exists".format(t[3]))

    # ??????insert?????????
    current_action.add_stack(stack)


def p_expression_import(t):
    '''exp_import : IMPORT COLUMN FROM COLUMN LFPARENTH exp_attributes COMMA PRIMARY KEY LFPARENTH COLUMN RGPARENTH RGPARENTH END'''
    global current_action
    current_action = Create()
    if not current_action.set_table(t[2]):
        reset_action()
        raise Exception(
            "INVALID IDENTIFIER Error: {0} table already exists".format(t[2]))
    # ????????????
    current_action.skip = False
    current_action.is_Index = False
    current_action.from_import = t[4]
    current_action.set_primary(t[11])
    current_action.add_stack(stack)


def p_expression_export(t):
    '''exp_export : EXPORT COLUMN FROM COLUMN END'''
    if t[4] not in catalog.tables.keys():
        raise Exception(
            "INVALID IDENTIFIER Error: {0} table doesn't exist".format(t[4]))
    api.output(t[4], t[2])


def p_expression_condition(t):
    '''exp_condition : COLUMN OP COLUMN
                     | COLUMN OP COLUMN AND exp_condition
                     | COLUMN EQUAL COLUMN
                     | COLUMN EQUAL COLUMN AND exp_condition'''
    # print("condition", t[1], t[2], t[3])
    condition_stack.append((t[1], t[2], t[3]))


def p_expresssion_insert_end(t):
    '''exp_insert_end : VALUES LFPARENTH columns RGPARENTH END
                      | LFPARENTH columns RGPARENTH VALUES LFPARENTH columns RGPARENTH END'''
    if len(t) == 9:
        stack.is_columns = True


def p_expression_columns(t):
    '''columns : COLUMN
               | COLUMN COMMA columns'''
    stack.append(t[1])


def p_expression_show_table(t):
    ''' exp_show_table : SHOW TABLE COLUMN END '''
    if t[3] not in catalog.tables.keys():
        raise Exception(
            "INVALID IDENTIFIER Error: {0} table not exists".format(t[3]))
    api.show_table(t[3])


def p_expression_show(t):
    ''' exp_show : SHOW END '''
    api.show()


def p_expression_show_index(t):
    '''exp_show_index : SHOW INDEX COLUMN END '''
    if t[3] not in catalog.indices.keys():
        raise Exception(
            "INVALID IDENTIFIER Error: {0} index not exists".format(t[3]))
    api.show_index(t[3])


def p_expression_execfile(t):
    '''exp_execfile : EXECFILE COLUMN END'''
    file_exec(t[2])


def p_expression_help(t):
    ''' exp_help : HELP END'''
    global current_action
    current_action = Help()


def p_error(p):
    if p:
        print(
            "SYNTAX Error: You have an error in your SQL syntax at {0}".format(p.value))
    else:
        print("SYNTAX Error: You have an error in your SQL syntax at EOF")


def interpreter(data):
    if not data.strip():
        return
    if data.split(' ')[0] not in ['execfile', 'EXECFILE', 'import', 'IMPORT', 'export', 'EXPORT']:
        data = data.lower()
    elif data.split(' ')[0] in ['import', 'IMPORT']:
        a = [item.lower() for item in data.split(' ')]
        a[3] = data.split(' ')[3]
        data = ' '.join(a)
    elif data.split(' ')[0] in ['EXPORT', 'export']:
        a = data.split(' ')
        a[3] = a[3].lower()
        data = ' '.join(a)
    yacc.yacc()
    yacc.parse(data)


def set_catalog(catalog_m):
    global catalog
    catalog = catalog_m


def set_api(api_m):
    global api
    api = api_m


def file_exec(file_name):
    with open(file_name, 'r') as f:
        i = 0
        data_list = f.readlines()
        print(">>>>>>>>>>>>>>>>> sql execute file start >>>>>>>>>>>>>>>>>\n")
        for data in data_list:
            try:
                i = i+1
                data = data.strip('\n')
                print("sql execute file line {0}>".format(i)+data)
                interpreter(data)
                print("")
            except Exception as e:
                print(e)
                # traceback.print_exc()
                print("")

        print("\n<<<<<<<<<<<<<<<<< sql execute file end <<<<<<<<<<<<<<<<<")


if __name__ == "__main__":
    catalog = catalog_manager()
    print([item.name for item in catalog.tables['xyz'].attributes])
    print(catalog.indices.keys())
    while True:
        data = input("sql>")
        yacc.yacc()
        yacc.parse(data)
