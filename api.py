import time


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
        start = time.time()
        # attr[0]: name     attr[1]: type
        # attr[2]: length   attr[3]: uniqueness
        '''process self.tbl_attributes into the format above at first
        the process should be done after interpreter is complete'''
        for attr in self.tbl_attributes: 
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
        self.record.create(self.tbl_name, self.tbl_attributes)
        # the index is built when inserting
        end = time.time()
        print('Duration: %fs' % (end - start))
        # print('tables now:', end='')
        # for tbl_name in self.catalog.tables.keys(): 
        #     print(' '+tbl_name, end='')
        # print()

    def drop_table(self):
        start = time.time()
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
        end = time.time()
        print('Duration: %fs' % (end - start))

    def create_index(self):
        start = time.time()
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
        end = time.time()
        print('Duration: %fs' % (end - start))

    def drop_index(self):
        start = time.time()
        # existence is checked in this call
        self.catalog.drop_index(self.idx_name)
        self.index.drop_index_file(self.idx_name)
        end = time.time()
        print('Duration: %fs' % (end - start))

    def insert_record(self):
        start = time.time()
        # mind to encode the string before calling self.record.insert()
        '''check whether the number of values input equals to the number of attributes'''
        '''transform the input to the correct format'''
        '''call self.index.search() to check uniqueness'''
        '''call self.record.insert()'''
        '''call self.record.scan_all(), self.index.create_index() and self.index.save_Bplus() to update the index'''
        end = time.time()
        print('Duration: %fs' % (end - start))

    def delete_record(self):
        start = time.time()
        # mind to encode the string before calling self.record.insert()
        '''update the record and the index'''
        end = time.time()
        print('Duration: %fs' % (end - start))

    def select(self):
        start = time.time()
        # decode
        # if an index can be made use of, use the index
        # if not, scan all the records
        end = time.time()
        print('Duration: %fs' % (end - start))

    # retrive data from interpreter
    def retrieve_table(self, _tbl_name, _tbl_pky = None, _attributes = None):
        self.tbl_name = _tbl_name
        self.tbl_pky = _tbl_pky
        # transform tuples into lists here
        if _attributes is not None: 
            self.tbl_attributes = [list(attr) for attr in _attributes]
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


'''How to print: '''
    # print('-' * (17 * len(__columns_list_num) + 1))
    # for i in __columns_list:
    #     if len(str(i)) > 14:
    #         output = str(i)[0:14]
    #     else:
    #         output = str(i)
    #     print('|',output.center(15),end='')
    # print('|')
    # print('-' * (17 * len(__columns_list_num) + 1))
    # for i in results:
    #     for j in __columns_list_num:
    #         if len(str(i[j])) > 14:
    #             output = str(i[j])[0:14]
    #         else:
    #             output = str(i[j])
    #         print('|',output.center(15) ,end='')
    #     print('|')
    # print('-' * (17 * len(__columns_list_num) + 1))
    # print("Returned %d entrys," % len(results),end='')
