import enum
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

    def create_table(self):
        # attr[0]: name     attr[1]: type
        # attr[2]: length   attr[3]: uniqueness
        '''process self.tbl_attributes into the format above at first
        the process should be done after interpreter is complete'''
        names = [attr[0] for attr in self.tbl_attributes]
        checknames = set(names)
        if len(checknames) != len(names):
            raise Exception('Error: duplicate names for attributes!')
        for attr in self.tbl_attributes:
            if '"' in attr[0] or "'" in attr[0]:
                raise Exception('Error: illegal syntax in attribute name')
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
        self.catalog.create_table(
            self.tbl_name, self.tbl_pky, self.tbl_attributes)
        self.catalog.create_index(self.tbl_name, self.tbl_name, self.tbl_pky)
        self.record.create(self.tbl_name, self.tbl_attributes)
        self.index.create_index_file(self.tbl_name)

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
            self.drop_index(index)
        # drop the table at last
        self.record.drop_record_file(self.tbl_name)
        self.catalog.save()

    def create_index(self):
        # duplicate, existence and uniqueness is checked in this call
        self.catalog.create_index(self.idx_name, self.idx_tbl, self.idx_key)
        # attr[0]: name     attr[1]: type
        # attr[2]: length   attr[3]: uniqueness
        '''process self.tbl_attributes into the format above at first
        the process should be done after interpreter is complete'''
        key_idx = 0
        type = length = None
        for i in range(len(self.catalog.tables[self.idx_tbl].attributes)):
            # the index of the key in the table is i
            if self.catalog.tables[self.idx_tbl].attributes[i].name == self.idx_key:
                key_idx = i
                type = self.catalog.tables[self.idx_tbl].attributes[i].type
                length = self.catalog.tables[self.idx_tbl].attributes[i].length
        # read all the records
        attrlist = []
        for item in self.catalog.tables[self.idx_tbl].attributes:
            attrlist.append((item.name, item.type, item.length, item.uniqueness))
        records, addresses = self.record.scan_all(
            self.idx_tbl, [], attrlist)
        # extract the values
        values = [rec[key_idx] for rec in records]
        # order = (4096-2-1-2) // (length of key + 2) + 1
        order = (4096 - 5) // (length + 2) + 1
        # create the index
        self.index.create_index(self.idx_name, addresses, values, order)
        # save the B plus tree as a file
        self.index.save_Bplus(self.idx_name, type, length)

    def drop_index(self, index_name):
        # existence is checked in this call
        self.catalog.drop_index(index_name)
        self.index.drop_index_file(index_name)
        self.catalog.save()

    def insert_record(self, table, value, attr=None):
        # mind to encode the string before calling self.record.insert()
        '''check whether the number of values input equals to the number of attributes'''
        if attr is not None and (len(attr) != len(value)):
            print(
                "Error: The number of input values DOES NOT MATCH the number of input attributes")
            return False
        '''transform the input to the correct format'''
        # string process
        for i, item in enumerate(self.catalog.tables[table].attributes):
            if item.type[-1] == 's':
                value[i] = value[i][1:-1]
                value[i] = str(value[i])
                value[i] = value[i].encode('utf-8')
            elif item.type == 'i':
                value[i] = int(value[i])
            elif item.type == 'f':
                value[i] = float(value[i])
        '''call self.index.search() to check uniqueness'''
        primary = self.catalog.tables[table].primary_key
        if attr is None:
            primary_index = self.catalog.index_in_table(table, primary)
            attr = [[item.name, item.type, item.length, item.uniqueness]
                    for item in self.catalog.tables[table].attributes]
        else:
            pass
        # primary_value = value[primary_index]
        tmp = []
        '''read a record here and check all the uniqueness'''
        # primary_type = self.catalog.tables[table].attributes[primary_index].type
        # if primary_type[0] == 'i' or primary_type[0] == 'f':
        #     primary_length = 4
        # else:
        #     primary_length = int(primary_type[:-1])
        # uniqRes = self.index.search(table, primary_value, primary_type, primary_length)
        # if uniqRes : # Not unique
        #     raise Exception("ERROR: the input data has duplicated Primary Key Value")
        # else:
        check_record, check_ptr = self.record.scan_all(table, [], attr)
        for i in range(len(check_record)):
            for j, column in enumerate(self.catalog.tables[table].attributes):
                if column.uniqueness is True:
                    if len(column.type) == 1 and check_record[i][j] == value[j]:
                        raise Exception('Error: the uniqueness constraint')
                    elif len(column.type) != 1 and check_record[i][j].strip(b'\x00') == value[j]:
                        raise Exception('Error: the uniqueness constraint')
        '''call self.record.insert()'''
        attribute = [[item.name, item.type, item.length, item.uniqueness]
                     for item in self.catalog.tables[table].attributes]
        self.record.insert(table, attribute, value)
        '''call self.record.scan_all(), self.index.create_index() and self.index.save_Bplus() to update the index'''
        result_value, result_ptr = self.record.scan_all(table, [], attr)
        tmp.clear()
        for item in self.catalog.indices.keys():
            if self.catalog.indices[item][0] == table:
                idx = self.catalog.index_in_table(table, self.catalog.indices[item][1])
                tmp.append([item, idx, self.catalog.tables[table].attributes[idx].type, self.catalog.tables[table].attributes[idx].length])
        for index_name, i, type, length in tmp:
            key_value = [item[i] for item in result_value]
            order = (4096-2-1-2) // (length + 2) + 1
            self.index.create_index(index_name, result_ptr, key_value, order)
            self.index.save_Bplus(index_name, type, length)
        print('Successfully insert')

    def delete_record(self, table, conditions):
        '''update the record and the index'''
        self.catalog.table_not_exists(table)
        attrlist = []
        for item in self.catalog.tables[table].attributes:
            attrlist.append((item.name, item.type, item.length, item.uniqueness))
        # conditions process
        conditions = [list(item) for item in conditions]
        for item in conditions:
            if item[1] == '<':
                item[1] = 0
            elif item[1] == '<=':
                item[1] = 1
            elif item[1] == '>':
                item[1] = 2
            elif item[1] == '>=':
                item[1] = 3
            elif item[1] == '=':
                item[1] = 4
            elif item[1] == '<>':
                item[1] = 5
            else:
                raise Exception('Error: illegal operator')
            idx = self.catalog.index_in_table(table, item[0])
            if self.catalog.tables[table].attributes[idx].type == 'i': 
                item[2] = int(item[2])
            elif self.catalog.tables[table].attributes[idx].type == 'f':
                item[2] = float(item[2]) 
            item[0] = idx
        result_record, result_ptr = self.record.scan_all(table, conditions, attrlist)
        for bid, offset in result_ptr: 
            self.record.delete_with_index(table, bid, offset)
        # call self.record.scan_all(), self.index.create_index() and self.index.save_Bplus() to update the index
        attr = [[item.name, item.type, item.length, item.uniqueness] for item in self.catalog.tables[table].attributes]
        result_value, result_ptr = self.record.scan_all(table, [], attr)
        tmp = []
        for item in self.catalog.indices.keys():
            if self.catalog.indices[item][0] == table:
                idx = self.catalog.index_in_table(table, self.catalog.indices[item][1])
                tmp.append([item, idx, self.catalog.tables[table].attributes[idx].type, self.catalog.tables[table].attributes[idx].length])
        for index_name, i, type, length in tmp:
            key_value = [item[i] for item in result_value]
            order = (4096-2-1-2) // (length + 2) + 1
            self.index.create_index(index_name, result_ptr, key_value, order)
            self.index.save_Bplus(index_name, type, length)
        print("%d entrys affected" % len(result_record))
        print('Successfully delete')

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
        self.catalog.table_not_exists(table)
        attrlist = []
        col_index = []
        for item in self.catalog.tables[table].attributes:
            attrlist.append((item.name, item.type, item.length, item.uniqueness))
        if len(cols) == 0:
            cols = attrlist
        else:
            for item in cols:
                self.catalog.key_not_exists(table, item)
            tmp = [item for item in cols]
            cols.clear()
            for item in tmp:
                for i, attr in enumerate(attrlist):
                    if item == attr[0]:
                        cols.append(attr)
                        col_index.append(i)
                        break
        # process constraints
        conditions = [list(item) for item in conditions]
        for item in conditions:
            if item[1] == '<':
                item[1] = 0
            elif item[1] == '<=':
                item[1] = 1
            elif item[1] == '>':
                item[1] = 2
            elif item[1] == '>=':
                item[1] = 3
            elif item[1] == '=':
                item[1] = 4
            elif item[1] == '<>':
                item[1] = 5
            else:
                raise Exception('Error: illegal operator')
            idx = self.catalog.index_in_table(table, item[0])
            if self.catalog.tables[table].attributes[idx].type == 'i': 
                item[2] = int(item[2])
            elif self.catalog.tables[table].attributes[idx].type == 'f':
                item[2] = float(item[2]) 
            item[0] = idx
        (result_record, result_ptr) = self.record.scan_all(
            table, conditions, attrlist)
        if attrlist != cols:
            for i in range(len(result_record)):
                result_record[i] = list(result_record[i])
                temp = []
                for idx in col_index:
                    temp.append(result_record[i][idx])
                result_record[i].clear()
                result_record[i] = [item for item in temp]
        stringFlag = [0 for i in range(len(cols))]
        for item in cols:
            type = item[1]
            if type[-1] == 's':
                stringFlag[cols.index(item)] = int(type[:-1])
        namelength = 0
        print('-' * (17 * len(cols) + 1))
        for i in cols:
            namelength = namelength + len(i[0])
            if len(str(i[0])) > 14:
                output = str(i[0])[0:14]
            else:
                output = str(i[0])
            print('|', output.center(15), end='')
        print('|')
        print('-' * (17 * len(cols) + 1))
        for i in result_record:
            for j in range(len(cols)):
                if stringFlag[j] != 0:
                    string = i[j].decode("utf-8").strip('\x00')
                    if len(str(string)) > 14:
                        output = str(string)[0:14]
                    else:
                        output = str(string)
                else:
                    if len(str(i[j])) > 14:
                        output = str(round(i[j], 4))[0:14]
                    else:
                        output = str(round(i[j], 4))
                print('|', output.center(15), end='')
            print('|')
            print('-' * (17 * len(cols) + 1))
        print("Returned %d entrys" % len(result_record))

    # retrive data from interpreter
    def retrieve_table(self, _tbl_name, _tbl_pky=None, _attributes=None):
        self.tbl_name = _tbl_name
        self.tbl_pky = _tbl_pky
        # transform tuples into lists here
        if _attributes is not None:
            self.tbl_attributes = [list(attr) for attr in _attributes]
            for attr in self.tbl_attributes:
                if self.tbl_pky == attr[0]:
                    attr[3] = 1
                    break
            # print("api attr: ", self.tbl_attributes)

    # retrive data from interpreter
    def retrieve_index(self, _idx_name, _idx_key=None, _idx_tbl=None):
        self.idx_name = _idx_name
        self.idx_key = _idx_key
        self.idx_tbl = _idx_tbl

    def exit(self):
        self.catalog.save()


    def show(self): 
        print('tables:', end='')
        for tbl_name in self.catalog.tables.keys(): 
            print(' '+tbl_name, end='')
        print()
        print('indice:', end='')
        for idx_name in self.catalog.indices.keys(): 
            print(' '+idx_name, end='')
        print()