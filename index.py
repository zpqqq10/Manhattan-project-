import struct
import minisql.catalog as catalog

class Node():
    def __init__(self, isleaf = False):
        self.keys = []
        self.children = []
        self.isleaf = isleaf

    # to tell whether a split or a merge is necessary
    def poor(self, order): 
        return len(self.keys) < order // 2 +1

    def is_leaf(self): 
        return self.isleaf

    def is_empty(self):
        return len(self.keys) == 0

    # children
    def is_full(self, order): 
        return len(self.children) >= order

    def index_of_insert(self, key): 
        # insert at keys[0]
        if self.is_empty or key<self.keys[0]: 
            return 0
        
        # isnert at the last position
        length = len(self.keys)
        if key >= self.keys[length-1]: 
            return length
        
        # insert 
        if length >= 2: 
            for i in range(length-1): 
                if key >=self.keys[i] and key < self.keys[i+1]: 
                    return i+1

        raise Exception('The key has no position to place')

class index_manager():
    def __init__(self, order, buffer_manager):
        self.root = Node(); 
        # order = (4096-4-1-2) // (length of key + 4) + 1
        # 1 is for a bool variable 'isleaf'
        # 2 is for the number of keys in a certain node
        self.order = order
        self.buffer_manager = buffer_manager
    

    # length: the length of the key attribute
    # value:  the value to be found
    def search(self, name, value, type, length):
        path = './index/' + name +'idx'
        keys = []
        children = []
        cur_bid = cur_offset = 0
        res_bid = res_offset = 0
        isleaf = False
        num = 0     # number of keys in this block
        while True: 
            # build a node
            cur_block = self.buffer_manager.read_block(path, cur_bid)
            isleaf, num = struct.unpack('=?h', cur_block[:3])
            cur_offset = 3
            for i in range(num): 
                children.append(struct.unpack('=hh', cur_block[cur_offset:cur_offset+4]))
                cur_offset += 4
                keys.append(struct.unpack('='+type, cur_block[cur_offset:cur_offset+length]))
                cur_offset += length
                if type[-1:] == 's': 
                    keys[-1] = keys[-1].decode('utf-8')
            if isleaf == True: 
                # read one more child
                children.append(struct.unpack('=hh', cur_block[cur_offset:cur_offset+4]))
            # find the value
            if isleaf == True: 
                # go deeper
                if value >= keys[num-1]: 
                    cur_bid = children[num][0]
                elif value < keys[0]: 
                    cur_bid = children[0][0]
                else: 
                    for i in range(num-1): 
                        if value >= keys[i] and value < keys[i+1]: 
                            cur_bid = children[i+1][0]
                            break
            else: 
                # find the value and return its position
                if value not in keys:
                    raise Exception('The value is not in the table') 
                else: 
                    res_bid, res_offset = children[keys.index(value)]
                    break
            keys = []
            children = []
            cur_offset = 0
        
        return res_bid, res_offset

    def insert(key, addr): 
        pass

    def remove(key):
        pass

    def split(): 
        pass

    def merge(): 
        pass

    def build_Bplus(): 
        pass

    def save_Bplus(): 
        pass

    def create_index():
        pass

    def drop_index():
        pass


# # attribute[0] = value of key
# # attribute[1] = address
# def create_index(index_name, table_name, key, attribute): 
#     catalog.table_not_exists(table_name)    # check if the table exists
#     catalog.index_exists(index_name)    # check duplicate index
#     new_index = Bplus()
#     for attr in attribute: 
#         new_index.insert(attr[0], attr[1])
#     catalog.create_index(index_name, table_name, key)   # add inofrmation to catalog
    

# def drop_index(index_name): 
#     catalog.index_not_exists(index_name)    # check if the index exists
#     # remove the corresponding index file
#     catalog.drop_index(index_name)

# def access_by_index():  # limit?
#     pass

# def update_index_insert(index_name, attribute): 
#     pass

# def update_index_remove(index_name, attribute): 
#     pass
