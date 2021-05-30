import py.minisql.catalog as catalog

class Node():
    def __init__(self, isleaf = False):
        self.keys = []
        self.children = []
        self.isleaf = isleaf

    # to tell whether a split or a merge is necessary
    def poor(self, order): 
        return len(self.keys) < order // 2 +1

class Bplus():
    def __init__(self):
        self.root = Node(); 
        # order?
    
    def search(key):
        pass

    def insert(key, addr): 
        pass

    def remove(key):
        pass

    def split(): 
        pass

    def merge(): 
        pass

    def build_from_file(): 
        pass

# attribute[0] = value of key
# attribute[1] = address
def create_index(index_name, table_name, key, attribute): 
    catalog.table_not_exists(table_name)    # check if the table exists
    catalog.index_exists(index_name)    # check duplicate index
    new_index = Bplus()
    for attr in attribute: 
        new_index.insert(attr[0], attr[1])
    catalog.create_index(index_name, table_name, key)   # add inofrmation to catalog
    

def drop_index(index_name): 
    catalog.index_not_exists(index_name)    # check if the index exists
    # remove the corresponding index file
    catalog.drop_index(index_name)

def access_by_index():  # limit?
    pass

def update_index_insert(index_name, attribute): 
    pass

def update_index_remove(index_name, attribute): 
    pass
