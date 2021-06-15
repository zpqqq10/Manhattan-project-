from catalog import catalog_manager
from buffer import bufferManager
from record import record_manager
from index import index_manager

class optimizer(object):
    def __init__(self):
        pass

    # of no use temporarily
    def select_opt(self, keys, values, ops, index_dic): 
        pass

        

class API(): 
    def __init__(self):
        self.catalog = catalog_manager()
        self.buffer = bufferManager()
        self.record = record_manager(self.buffer)
        self.index = index_manager(self.buffer)
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
        self.s_project = self.s_keys = self.s_values  = self.s_ops = None

    def create_table(self): 
        # attr[0]: name     attr[1]: type
        # attr[2]: length   attr[3]: uniqueness
        '''process self.tbl_attributes into the format above at first
        the process should be done after interpreter is complete'''
        # duplicate is checked in this call
        self.catalog.create_table(self.tbl_name, self.tbl_pky)
        self.record.create(self.tbl_name, self.tbl_attributes)
        # the index is built when inserting

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
        records, addresses = self.record.scan_all(self.tbl_name, [], self.tbl_attributes)
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

    def insert_record(self): 
        # mind to encode the string before calling self.record.insert()
        '''check whether the number of values input equals to the number of attributes'''
        '''transform the input to the correct format'''
        '''call self.index.search() to check uniqueness'''
        '''call self.record.insert()'''
        '''call self.record.scan_all(), self.index.create_index() and self.index.save_Bplus() to update the index'''
        pass

    def delete_record(self): 
        # mind to encode the string before calling self.record.insert()
        '''update the record and the index'''
        pass

    def select(self): 
        # decode
        # if an index can be made use of, use the index
        # if not, scan all the records
        pass
# retrive data from interpreter
def retrieve_table(_tbl_name, _tbl_pky, _attributes): 
    global api
    api.tbl_name = _tbl_name
    api.tbl_pky = _tbl_pky
    # attributes may need process here
    api.tbl_attributes = _attributes

# retrive data from interpreter
def retrieve_index(_idx_name, _idx_key, _idx_tbl): 
    global api
    api.idx_name = _idx_name
    api.idx_key = _idx_key
    api.idx_tbl = _idx_tbl

# retrive data from interpreter
def retrieve_select(columns, conditions): 
    global api
    api.s_project = columns
    api.s_keys = [cdt[0] for cdt in conditions]
    api.s_values = [cdt[2] for cdt in conditions]
    api.s_ops = [cdt[1] for cdt in conditions]





