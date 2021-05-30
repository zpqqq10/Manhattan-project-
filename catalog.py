tables = {}  # dictionary for all tables
indices = {}  # dictionary for all indices


class class_table():
    def __init__(self, table_name, primary_key, number_attributes):
        self.table_name = table_name
        self.primary_key = primary_key
        self.attributes = {}
        self.number_attributes = number_attributes


# type = int, char(n) and 1<=n<=255, float
# length is n
class attribute():
    def __init__(self, uniqueness=False, type='char', length=20):
        # self.attribute_name = name
        self.uniqueness = uniqueness
        self.type = type
        self.length = length


# raise an exception if the table exists
def table_exists(name):
    # for tbl_name in tables.keys():
    #     if name == tbl_name:
    #         raise Exception("Table '%s' exists" % name)
    if name in tables.keys(): 
        raise Exception("Table '%s' exists" % name)


# raise an exception if the table does not exist
def table_not_exists(name):
    if name not in tables.keys(): 
        raise Exception("Table '%s' doesn't exist" % name)


# raise an exception if the index exists
def index_exists(name):
    if name in indices.keys(): 
        raise Exception("Index '%s' exists" % name)


# raise an exception if the index does not exist
def index_not_exists(name):
    if name not in indices.keys(): 
        raise Exception("Index '%s' doesn't exist" % name)


# raise an exception if the key does not exist in the table
def key_not_exists(tbl_name, key):
    for att in tables[tbl_name].attributes:
        if key == att.name: 
            return 
    raise Exception("Key '%s' doesn't exist in table ''" % (key, tbl_name))


# raise an exception if the key is not unique
def key_not_unique(tbl_name, key):
    if tables[tbl_name].attributes[key].uniqueness is False: 
        raise Exception("The key '%s' is not unique" % key)


# update the file & tables
# assume that the values have been processed by the interpreter
def create_table(tbl_name, primary_key, attrlist):
    global tables
    tmp = class_table(tbl_name, primary_key, len(attrlist))
    for attr in attrlist: 
        tmp.attributes[attr[0]] = attribute(attr[1], attr[2], attr[3])
    tables[tbl_name] = tmp
    # file?
    print("Successfully create table '%s'" % tbl_name)


# update the file & tables
def drop_table(tbl_name):
    global tables
    tables.pop(tbl_name)
    # file?
    print("Successfully drop table '%s'" % tbl_name)


# update the file & indices
def create_index(index_name, tbl_name, key):
    global indices
    key_not_exists(tbl_name, key)
    key_not_unique(tbl_name, key)
    indices[index_name] = [tbl_name, key]
    # index.build_index()


# update the file & indices
def drop_index(index_name):
    global indices
    indices.pop(index_name)
    # file?
    print("Successfully drop index '%s'" % index_name)