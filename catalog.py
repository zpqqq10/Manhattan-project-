import os
import struct

class catalog_manager:
    def __init__(self):
        self.tables = {}  # dictionary for all tables
        self.indices = {}  # dictionary for all indices
        # build tables
        file = open('./catalog/table_catalog.dat', 'rb')
        table_num = struct.unpack('i', file.read(4))
        for i in range(table_num):
            len_tbl, len_pky, len_attr = struct.unpack('iii', file.read(3*4))
            table_name, primary = struct.unpack(str(len_tbl)+'s'+str(len_pky)+'s', file.read(len_tbl+len_pky))
            self.tables[table_name] = Table(table_name, primary, len_attr)  # read a table
            for i in range(len_attr): 
                len_name, = struct.unpack('i', file.read(4))
                attr_name, = struct.unpack(str(len_name)+'s', file.read(len_name))
                uniqueness, = struct.unpack('?', file.read(1))
                type, = struct.unpack('i', file.read(4))
                if type == 1: 
                    self.tables[attr_name] = Attribute(uniqueness, 'int', 0)
                elif type == 2: 
                    self.tables[attr_name] = Attribute(uniqueness, 'float', 0)
                elif type == 3:
                    length, = struct.unpack('i', file.read(4))
                    self.tables[attr_name] = Attribute(uniqueness, 'char', length)
        file.close()
        # build indices
    
    def save(self): 
        # save tables
        file = open('./catalog/table_catalog.dat', 'wb+')
        file.write(struct.pack('i', len(self.tables)))  # the number of tables
        for table in self.tables: 
            len_tbl = len(table.table_name) # length of table name
            len_pky = len(table.primary_key)# length of the name of the primary key
            file.write(struct.pack('iii', len_tbl, len_pky, len(table.attributes.keys())))
            file.write(struct.pack(str(len_tbl)+'s'+str(len_pky)+'s', table.table_name.encode('utf-8'), table.primary_key.encode('utf-8')))
            for key in table.attributes.keys():
                len_name = len(key)
                file.write(struct.pack('i'+str(len_name)+'s', len_name, key.encode('utf-8')))   # name
                file.write(struct.pack('?', table.attributes[key].uniqueness))   # uniqueness
                if table.attributes[key].type == 'int':                    # type
                    file.write(struct.pack('i', 1))
                elif table.attributes[key].type == 'float': 
                    file.write(struct.pack('i', 2))
                elif table.attributes[key].type == 'char': 
                    file.write(struct.pack('ii', 3, table.attributes[key].length))
        file.close()
        # save indices

class Table():
    def __init__(self, table_name, primary_key, number_attributes):
        self.table_name = table_name
        self.primary_key = primary_key
        self.attributes = {}
        self.number_attributes = number_attributes


# type = int, char(n) and 1<=n<=255, float
# length is n
class Attribute():
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
    if name in catalog_manager.tables.keys(): 
        raise Exception("Table '%s' exists" % name)


# raise an exception if the table does not exist
def table_not_exists(name):
    if name not in catalog_manager.tables.keys(): 
        raise Exception("Table '%s' doesn't exist" % name)


# raise an exception if the index exists
def index_exists(name):
    if name in catalog_manager.indices.keys(): 
        raise Exception("Index '%s' exists" % name)


# raise an exception if the index does not exist
def index_not_exists(name):
    if name not in catalog_manager.indices.keys(): 
        raise Exception("Index '%s' doesn't exist" % name)


# raise an exception if the key does not exist in the table
def key_not_exists(tbl_name, key):
    for att in catalog_manager.tables[tbl_name].attributes:
        if key == att.name: 
            return 
    raise Exception("Key '%s' doesn't exist in table ''" % (key, tbl_name))


# raise an exception if the key is not unique
def key_not_unique(tbl_name, key):
    if catalog_manager.tables[tbl_name].attributes[key].uniqueness is False: 
        raise Exception("The key '%s' is not unique" % key)


# update the file & tables
# assume that the values have been processed by the interpreter
def create_table(tbl_name, primary_key, attrlist):
    global tables
    tmp = Table(tbl_name, primary_key, len(attrlist))
    for attr in attrlist: 
        tmp.attributes[attr[0]] = Attribute(attr[1], attr[2], attr[3])
    catalog_manager.tables[tbl_name] = tmp
    # file?
    print("Successfully create table '%s'" % tbl_name)


# update the file & tables
def drop_table(tbl_name):
    global tables
    catalog_manager.tables.pop(tbl_name)
    # file?
    print("Successfully drop table '%s'" % tbl_name)


# update the file & indices
def create_index(index_name, tbl_name, key):
    global indices
    key_not_exists(tbl_name, key)
    key_not_unique(tbl_name, key)
    catalog_manager.indices[index_name] = [tbl_name, key]
    # index.build_index()


# update the file & indices
def drop_index(index_name):
    global indices
    catalog_manager.indices.pop(index_name)
    # the catalog file?
    print("Successfully drop index '%s'" % index_name)