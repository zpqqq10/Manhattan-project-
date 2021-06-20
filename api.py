import struct

class optimizer(object):
    def __init__(self):
        pass

    # of no use temporarily
    def select_opt(self, keys, values, ops, index_dic):
        pass


class API():
    def __init__(self, catalog, buffer, record, index):
        self.catalog = catalog
        self.buffer = buffer
        self.record = record
        self.index = index
        # table
        #   name        primary key     attributes
        # tbl_attributes may be used for catalog or insert
        self.tbl_name = self.tbl_pky = self.tbl_attributes = None
        # index
        #   name        key of the index
        self.idx_name = self.idx_key = self.idx_tbl = None
        # search
        # columns to be listed
        #                keys to be selected on
        #                               values of the selected keys
        #                                               operations, <=>
        self.s_project = self.s_keys = self.s_values = self.s_ops = None

    def create_table(self):
        # attr[0]: name     attr[1]: type
        # attr[2]: length   attr[3]: uniqueness
        '''process self.tbl_attributes into the format above at first
        the process should be done after interpreter is complete'''
        names = [attr[0] for attr in self.tbl_attributes]
        checknames = set(names)
        if len(checknames) != len(names): 
            print('Error: duplicate names for attributes!')
            return False
        for attr in self.tbl_attributes: 
            if '"' in attr[0] or "'" in attr[0]: 
                print('Error: illegal syntax in attribute name')
                return False
            if attr[1] == 'int': 
                attr[1] = 'i'
            elif attr[1] == 'float': 
                attr[1] = 'f'
            elif attr[1] == 'char': 
                attr[1] = attr[2] + 's'
            attr[2] = int(attr[2])
            if attr[3] == 1: 
                attr[3] = True
            elif attr[3] == 0: 
                attr[3] = False
        # duplicate is checked in this call
        self.catalog.create_table(self.tbl_name, self.tbl_pky, self.tbl_attributes)
        self.catalog.create_index(self.tbl_name+'_DEFAULT_'+self.tbl_pky, self.tbl_name, self.tbl_pky)
        self.record.create(self.tbl_name, self.tbl_attributes)
        self.index.create_index_file(self.tbl_name+'_DEFAULT_'+self.tbl_pky)
        
        # print('tables now:', end='')
        # for tbl_name in self.catalog.tables.keys(): 
        #     print(' '+tbl_name, end='')
        # print()

    def drop_table(self):
        # existence is checked in this call
        self.catalog.drop_table(self.tbl_name)
        # drop indices based on the table at first
        tmp_indices = []
        for index in self.catalog.indices.keys():
            if self.catalog.indices[index][0] == self.tbl_name:
                tmp_indices.append(index)
        for index in tmp_indices:
            self.idx_name = index
            self.drop_index()
        # drop the table at last
        self.record.drop_record_file(self.tbl_name)

    def create_index(self):
        # duplicate, existence and uniqueness is checked in this call
        self.catalog.create_index(self.idx_name, self.idx_tbl, self.idx_key)
        # attr[0]: name     attr[1]: type
        # attr[2]: length   attr[3]: uniqueness
        '''process self.tbl_attributes into the format above at first
        the process should be done after interpreter is complete'''
        key_idx = 0
        type = length = None
        for i in range(len(self.catalog.tables[self.tbl_name].attributes)):
            # the index of the key in the table is i
            if self.catalog.tables[self.tbl_name].attributes[i].name == self.idx_key:
                key_idx = i
                type = self.catalog.tables[self.tbl_name].attributes[i].type
                length = self.catalog.tables[self.tbl_name].attributes[i].length
        # read all the records
        records, addresses = self.record.scan_all(
            self.tbl_name, [], self.tbl_attributes)
        # extract the values
        values = [rec[key_idx] for rec in records]
        # order = (4096-2-1-2) // (length of key + 2) + 1
        order = (4096 - 5) // (length + 2) + 1
        # create the index
        self.index.create_index(self.idx_name, addresses, values, order)
        # save the B plus tree as a file
        self.index.save_Bplus(self.idx_name, type, length)

    def drop_index(self):
        # existence is checked in this call
        self.catalog.drop_index(self.idx_name)
        self.index.drop_index_file(self.idx_name)

    def insert_record(self, table, attr, value):
        # mind to encode the string before calling self.record.insert()
        '''check whether the number of values input equals to the number of attributes'''
        if (len(attr) != len(value)):
            print("Error: The number of input values DOES NOT MATCH the number of input attributes")
            return False
        '''transform the input to the correct format'''
        # I think there is nothing need transforming
        '''call self.index.search() to check uniqueness'''
        primary = self.catalog.tables[table].primary_key
        for i, item in attr:
            if (item == primary):
                primary_index = i
                break
        primary_value = value[primary_index]
        for item in self.catalog.tables[table].attributes:
            if self.catalog.tables[table].attributes[item].name == primary:
                primary_type = self.catalog.tables[table].attributes[item].type
        if primary_type[0] == 'i' or primary_type[0] == 'f':
            primary_length = 4
        else:
            primary_length = int(primary_type[:-1])
        uniqRes = self.index.search(table, primary_value, primary_type, primary_length)
        if (uniqRes) : # Not unique
            print("ERROR: the input data has duplicated Primary Key Value")
            return False

        # string process
        for i, item in self.catalog.tables[table].attributes:
            if (item[-1] == 's'):
                if (value[i][0] == '"' and value[i][-1] == '"') or (value[i][0] == "'" and value[i][-1] == "'"):
                    value[i] = value[1:-1]
                else:
                    print("ERROR: The quote signal of string value is wrong")
                    return False
        '''call self.record.insert()'''
        self.record.insert(table, attr, value)
        '''call self.record.scan_all(), self.index.create_index() and self.index.save_Bplus() to update the index'''
        (result_value, result_ptr) = self.record.scan_all(table, (), attr)
        order = (4096-2-1-2) // (primary_length + 2) + 1
        for item in self.catalog.indices:
            if self.catalog.indices[item][0] == table:
                index_name = item
                break
        self.index.create_index(index_name, result_ptr, result_value, order)
        self.index.save_Bplus(index_name, primary_type, primary_length)

    def delete_record(self):
        # mind to encode the string before calling self.record.insert()
        '''update the record and the index'''

    def select(self, table, cols, conditions):
        # checke index
        # for item in self.catalog.indices:
        #     if (self.catalog.indices[item][0] == table):
        #         flag = True
        #         index = item
        #         break;
        #     else:
        #         flag = False
        # if an index can be made use of, use the index
        # if flag:
        #     result_record, result_ptr = self.record.scan_with_index(table, conditions, cols, domain)

        # if not, scan all the record
        
        # decode if need
        if len(cols) == 0:
            cols = []
            for item in self.catalog.tables[table].attributes:
                if item.length == 0:
                    cols.append((item.name, item.type, 4, item.uniqueness))
                else: 
                    cols.append((item.name, item.type, item.length, item.uniqueness))
                # print(item.length)
        (result_record, result_ptr) = self.record.scan_all(table, conditions, cols)
        stringFlag = [0 for i in range(len(cols) - 1)]
        for item in cols:
            for col in self.catalog.tables[table].attributes:
                if col.name == item[0]:
                    type = col.type
                    break
            if type[-1] == 's':
                stringFlag[cols.index(item)] = int(type[:-1])
        namelength = 0
        for i in cols:
            namelength = namelength + len(i[0])
            if len(str(i[0])) > 14:
                output = str(i[0])[0:14]
            else:
                output = str(i[0])
            print('|',output.center(15),end='')
        print('|\n')
        print('-' * (17 * len(cols) + 1))
        for i in result_record:
            for j in range(len(cols) - 1):
                if stringFlag[j] != 0:
                    string = i[j].decode("utf-8")
                    if len(str(string)) > 14:
                        output = str(string)[0:14]
                    else:
                        output = str(string)
                else:
                    if len(str(i[j])) > 14:
                        output = str(i[j])[0:14]
                    else:
                        output = str(i[j])
                print('|',output.center(15) ,end='')
            print('|\n')
            print('-' * (17 * len(cols) + 1))
        print("Returned %d entrys," % len(result_record),end='')    

    # retrive data from interpreter
    def retrieve_table(self, _tbl_name, _tbl_pky = None, _attributes = None):
        self.tbl_name = _tbl_name
        self.tbl_pky = _tbl_pky
        # transform tuples into lists here
        if _attributes is not None: 
            self.tbl_attributes = [list(attr) for attr in _attributes]
            for attr in self.tbl_attributes: 
                if self.tbl_pky == attr[0]: 
                    attr[3] = 1
                    break
            print("api attr: ", self.tbl_attributes)

    # retrive data from interpreter
    def retrieve_index(self, _idx_name, _idx_key = None, _idx_tbl = None):
        self.idx_name = _idx_name
        self.idx_key = _idx_key
        self.idx_tbl = _idx_tbl

    # retrive data from interpreter
    def retrieve_select(self, columns, conditions):
        self.s_project = columns
        # conditions may be empty but not None
        self.s_keys = [cdt[0] for cdt in conditions]
        self.s_values = [cdt[2] for cdt in conditions]
        self.s_ops = [cdt[1] for cdt in conditions]

    def exit(self): 
        self.catalog.save()



