import os
import struct
import sys
import pathlib


class Table():
    def __init__(self, table_name, primary_key, number_attributes):
        self.table_name = table_name
        self.primary_key = primary_key
        self.attributes = []
        self.number_attributes = number_attributes


# type = int, char(n) and 1<=n<=255, float
# length is n
class Attribute():
    def __init__(self, name, type='20s', length=20, uniqueness=False):
        self.name = name
        self.uniqueness = uniqueness
        self.type = type
        self.length = length


class catalog_manager:
    def __init__(self):
        # check catalog
        self.__check_catalog()
        self.tables = {}  # dictionary for all tables
        self.indices = {}  # dictionary for all indices
        # build tables
        os.chdir(sys.path[0])
        file = open('./catalog/table_catalog.dat', 'rb')
        # the number of all the tables
        table_num, = struct.unpack('=i', file.read(4))
        for i in range(table_num):
            len_tbl, len_pky, num_attr = struct.unpack('=iii', file.read(3*4))
            table_name, primary = struct.unpack(
                '='+str(len_tbl)+'s'+str(len_pky)+'s', file.read(len_tbl+len_pky))
            table_name = table_name.decode('utf-8')
            primary = primary.decode('utf-8')
            self.tables[table_name] = Table(
                table_name, primary, num_attr)  # read a table
            for i in range(num_attr):
                len_name, = struct.unpack('=i', file.read(4))
                attr_name, = struct.unpack(
                    '='+str(len_name)+'s', file.read(len_name))
                attr_name = attr_name.decode('utf-8')
                uniqueness, = struct.unpack('=?', file.read(1))
                type, = struct.unpack('=B', file.read(1))
                if type == 1:
                    self.tables[table_name].attributes.append(
                        Attribute(attr_name, 'i', 4, uniqueness))
                elif type == 2:
                    self.tables[table_name].attributes.append(
                        Attribute(attr_name, 'f', 4, uniqueness))
                elif type == 3:
                    length, = struct.unpack('=i', file.read(4))
                    self.tables[table_name].attributes.append(
                        Attribute(attr_name, str(length)+'s', length, uniqueness))
        file.close()
        # build indices
        file = open('./catalog/index_catalog.dat', 'rb')
        index_num, = struct.unpack('=i', file.read(4))
        for i in range(index_num):
            len_index, len_tbl, len_key = struct.unpack('=iii', file.read(3*4))
            index, = struct.unpack(
                '='+str(len_index)+'s', file.read(len_index))
            tbl,   = struct.unpack('='+str(len_tbl)+'s', file.read(len_tbl))
            key,   = struct.unpack('='+str(len_key)+'s', file.read(len_key))
            index = index.decode('utf-8')
            tbl = tbl.decode('utf-8')
            key = key.decode('utf-8')
            self.indices[index] = [tbl, key]
        file.close()
        # check existence
        for table in self.tables.keys(): 
            self.check_record_files(table)
        for index in self.indices.keys(): 
            self.check_index_files(index)
        

    # save the catalog
    def save(self):
        # save tables
        os.chdir(sys.path[0])
        file = open('./catalog/table_catalog.dat', 'wb+')
        file.write(struct.pack('=i', len(self.tables)))  # the number of tables
        for table in self.tables:
            len_tbl = len(table)  # length of table name
            # length of the name of the primary key
            len_pky = len(self.tables[table].primary_key)
            file.write(struct.pack('=iii', len_tbl, len_pky,
                       len(self.tables[table].attributes)))
            file.write(struct.pack('='+str(len_tbl)+'s'+str(len_pky)+'s',
                       table.encode('utf-8'), self.tables[table].primary_key.encode('utf-8')))
            for attr in self.tables[table].attributes:
                len_name = len(attr.name)
                file.write(struct.pack('=i'+str(len_name)+'s',
                           len_name, attr.name.encode('utf-8')))   # name
                file.write(struct.pack('=?', attr.uniqueness))   # uniqueness
                if attr.type == 'i':                    # type
                    file.write(struct.pack('=B', 1))
                elif attr.type == 'f':
                    file.write(struct.pack('=B', 2))
                elif attr.type[-1:] == 's':
                    file.write(struct.pack('=Bi', 3, attr.length))
        file.close()
        # save indices
        file = open('./catalog/index_catalog.dat', 'wb+')
        # the number of indices
        file.write(struct.pack('=i', len(self.indices)))
        for index in self.indices:
            len_index = len(index)
            len_tbl = len(self.indices[index][0])
            len_key = len(self.indices[index][1])
            file.write(struct.pack('=iii', len_index, len_tbl, len_key))
            # name of index
            file.write(struct.pack('='+str(len_index) +
                       's', index.encode('utf-8')))
            file.write(struct.pack('='+str(len_tbl)+'s',
                       self.indices[index][0].encode('utf-8')))   # name of table
            file.write(struct.pack('='+str(len_key)+'s',
                       self.indices[index][1].encode('utf-8')))   # name of key
        file.close()

    # raise an exception if the table exists
    def table_exists(self, name):
        # for tbl_name in tables.keys():
        #     if name == tbl_name:
        #         raise Exception("Table '%s' exists" % name)
        if name in self.tables.keys():
            raise Exception("INVALID IDENTIFIER: Table '%s' exists" % name)

    # raise an exception if the table does not exist
    def table_not_exists(self, name):
        if name not in self.tables.keys():
            raise Exception("INVALID IDENTIFIER: Table '%s' doesn't exist" % name)

    # raise an exception if the index exists
    def index_exists(self, name):
        if name in self.indices.keys():
            raise Exception("INVALID IDENTIFIER: Index '%s' exists" % name)

    # raise an exception if the index does not exist
    def index_not_exists(self, name):
        if name not in self.indices.keys():
            raise Exception("INVALID IDENTIFIER: Index '%s' doesn't exist" % name)

    # raise an exception if the key does not exist in the table
    def key_not_exists(self, tbl_name, key):
        self.table_not_exists(tbl_name)
        for attr in self.tables[tbl_name].attributes:
            if key == attr.name:
                return
        raise Exception("INVALID IDENTIFIER: Key '%s' doesn't exist in table '%s'" %
                        (key, tbl_name))

    # raise an exception if the key is not unique
    def key_not_unique(self, tbl_name, key):
        self.table_not_exists(tbl_name)
        for attr in self.tables[tbl_name].attributes:
            if key == attr.name and attr.uniqueness is False:
                raise Exception("INVALID ATTR FOR INDEX: The key '%s' is not unique" % key)

    def is_index_key(self, tbl_name, key):
        self.table_not_exists(tbl_name)
        self.key_not_exists(tbl_name, key)
        for idx_name in self.indices.keys():
            if tbl_name == self.indices[idx_name][0] and key == self.indices[idx_name][1]:
                return idx_name
        return False

    def index_in_table(self, tbl_name, idx_name):
        for i, attr in enumerate(self.tables[tbl_name].attributes):
            if attr.name == idx_name:
                return i

    # update the file & tables
    # assume that the values have been processed by the interpreter
    def create_table(self, tbl_name, primary_key, attrlist):
        self.table_exists(tbl_name)
        tmp = Table(tbl_name, primary_key, len(attrlist))
        for attr in attrlist:
            tmp.attributes.append(
                Attribute(attr[0], attr[1], attr[2], attr[3]))
        self.tables[tbl_name] = tmp

    # update the file & tables
    def drop_table(self, tbl_name):
        self.table_not_exists(tbl_name)
        self.tables.pop(tbl_name)

    # update the file & indices
    def create_index(self, index_name, tbl_name, key):
        self.key_not_exists(tbl_name, key)
        self.key_not_unique(tbl_name, key)
        self.index_exists(index_name)
        self.indices[index_name] = [tbl_name, key]

    # update the file & indices
    def drop_index(self, index_name):
        self.index_not_exists(index_name)
        self.indices.pop(index_name)


    def __check_catalog(self): 
        os.chdir(sys.path[0])
        if not pathlib.Path('./catalog').exists(): 
            raise Exception('ERROR: The catalog folder is missing! The program exits and please rebuild the folder!')
        if not pathlib.Path('./catalog/table_catalog.dat').exists(): 
            raise Exception('ERROR: The file for tables "table_catalog.dat" is missing! The program exits and please rebuild the file!')
        if not pathlib.Path('./catalog/index_catalog.dat').exists(): 
            raise Exception('ERROR: The file for indices "index_catalog.dat" is missing! The program exits and please rebuild the file!')

    def check_record_files(self, table): 
        if len(self.tables) != 0: 
            # check folders
            os.chdir(sys.path[0])
            record_folder = pathlib.Path('./record')
            if not record_folder.exists(): 
                raise Exception('ERROR: ALL the metadata may be lost! Please check your files!')
            # check record files
            recpath = './record/'+table+'.rec'
            if not pathlib.Path(recpath).exists(): 
                raise Exception('ERROR: Metadata of table %s may be lost! Please check your files! Choose to drop this table or rebuild this table'%table)


    def check_index_files(self, index): 
        if len(self.indices) != 0: 
            # check folders
            os.chdir(sys.path[0])
            index_folder  = pathlib.Path('./index')
            if not index_folder.exists(): 
                raise Exception('ERROR: ALL the indices may be lost! Please check your files!')
            # check record files
            indpath = './index/'+index+'.ind'
            if not pathlib.Path(indpath).exists(): 
                raise Exception('ERROR: Index %s may be lost! Please check your files! Choose to drop this index or rebuild this index'%index)

if __name__ == "__main__":
    t = catalog_manager()
    print(t.tables)
    # print(t.tables['abc'].attributes[0])
    # print(t.tables['abc'].attributes[0].type)
    print(t.indices)
    print(t.is_index_key('xyz', 'sid'))
    print(t.is_index_key('xyz', 'xxx'))
    t.create_table('xyz', 'sid', [['sid', '11s', 11, True], [
                   'name', '3s', 3, False], ['sex', 'i', 20, False]])
    t.create_table('abc', 'sid', [['sid', '20s', 20, True], [
                   'name', '3s', 3, False], ['sex', 'i', 20, False]])

    # t.drop_table('xyz')
    # t.create_index('indexabc', 'abc', 'sid')
    # t.create_index('index_xyz', 'xyz', 'sid')
    # t.drop_index('indexabc')
    t.save()

