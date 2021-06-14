import struct
import os
import sys
import struct
import buffer as buffer

'''
To maintain the index, we decided to directly abandon the historical version of the index and
rebuild the index. For a table of small scale, the time of rebuilding is acceptable. For a table of
large scale, we believe that the usual case is the many records are added or deleted together and it is 
better to rebuild the index
'''

class Node():
    def __init__(self, isleaf = False, parent = None):
        self.keys = []
        self.children = []
        self.bid = 0
        self.isleaf = isleaf
        self.parent = parent

    # to tell whether a split or a merge is necessary
    def is_poor(self, order): 
        return len(self.children) < order // 2

    def is_leaf(self): 
        return self.isleaf

    def is_empty(self):
        return len(self.keys) == 0

    # children
    def is_full(self, order): 
        return len(self.children) > order

    def index_of_insert(self, key): 
        # insert at keys[0]
        if self.is_empty() or key<self.keys[0]: 
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
    def __init__(self, buffer_manager):
        self.roots = {}
        self.orders = {}
        self.buffer_manager = buffer_manager
    
    # length: the length of the key attribute
    # value:  the value to be found
    def search(self, name, value, type, length):
        keys = []
        children = []
        cur_bid = cur_offset = 0
        res_bid = res_offset = 0
        isleaf = False
        num = 0     # number of keys in this block
        while True: 
            # build a node
            cur_block = self.buffer_manager.read_block(name, 1, cur_bid)
            isleaf, num = struct.unpack('=?h', cur_block[:3])
            cur_offset = 3
            for i in range(num): 
                children.append(struct.unpack('=hh', cur_block[cur_offset:cur_offset+4]))
                cur_offset += 4
                key, = struct.unpack('='+type, cur_block[cur_offset:cur_offset+length])
                keys.append(key)
                cur_offset += length
                if type[-1:] == 's': 
                    keys[-1] = keys[-1].decode('utf-8').strip('\x00')
            # read one more child
            # for a leaf node, the last child is the pointer to the next leaf 
            children.append(struct.unpack('=hh', cur_block[cur_offset:cur_offset+4]))
            # print(keys)
            # print(children)
            # print('------------')
            # find the value
            if isleaf == False: 
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
                # the last child is the pointer
                if value not in keys[:num]:
                    raise Exception('The value %s is not in the table'%value) 
                else: 
                    res_bid, res_offset = children[keys.index(value)]
                    break
            keys = []
            children = []
            cur_offset = 0
        
        return res_bid, res_offset

    def __search_leaf(self, node, value): 
        # a leaf
        if node.is_leaf() is True: 
            return node

        # not a leaf
        k = 0
        for i in range(len(node.keys)):
            if value < node.keys[i]: 
                k = i
                break 
        
        # recursively search
        if value < node.keys[k]:
            return self.__search_leaf(node.children[i], value)
        else:  
            return self.__search_leaf(node.children[i+1], value)

    def __insert(self, index_name, address, value, order): 
        root = self.roots[index_name]
        leaf = self.__search_leaf(root, value)

        index = leaf.index_of_insert(value)
        leaf.keys.insert(index, value)
        leaf.children.insert(index, address)

        # fix up the node that is inserted
        self.__fixup(index_name, leaf, order)

    def __fixup(self, index_name, node, order): 
        if node.is_full(order): 
            # a new root needs to be created
            if node.parent == None: 
                self.roots[index_name] = newroot = Node()
                node.parent = newroot
                newkey, lchild, rchild = self.__split(node, order)
                newroot.keys.append(newkey)
                newroot.children.append(lchild)
                newroot.children.append(rchild)
            else :
                # not a root
                parent = node.parent
                newkey, lchild, rchild = self.__split(node, order)
                index = parent.index_of_insert(newkey)
                parent.keys.insert(index, newkey)
                parent.children.insert(index+1, rchild)
                self.__fixup(index_name, parent, order)
        else :
            return

    def __split(self, node, order): 
        half = order // 2
        # a leaf
        if node.is_leaf(): 
            newnode = Node(True, node.parent)
            newnode.keys = node.keys[half:]
            newnode.children = node.children[half:]
            newkey = node.keys[half]
            node.keys = node.keys[:half]
            node.children = node.children[:half] 
            node.children.append(newnode)   # pointer to the next leaf
        # internal node
        else :
            newnode = Node(False, node.parent)
            newnode.keys = node.keys[half+1:]
            newnode.children = node.children[half+1:]
            newkey = node.keys[half]
            node.keys = node.keys[:half]
            node.children = node.children[:half+1]

        return newkey, node, newnode

    def __remove(self, index_name, value):
        pass

    def __merge(self): 
        pass

    def build_Bplus(self, index_name, addresses, values, order): 
        # order = (4096-2-1-2) // (length of key + 2) + 1
        # 1 is for a bool variable 'isleaf'
        # 2 is for the number of keys in a certain node
        self.orders[index_name] = order
        self.roots[index_name] = Node(True, None) 
        self.roots[index_name].children.append(None)
        for i in range(len(values)): 
            self.__insert(index_name, addresses[i], values[i], order)

    def save_Bplus(self, index_name, type, length): 
        os.chdir(sys.path[0])
        # clear the previous index
        file = open('./index/'+index_name+'.ind', 'wb')
        file.close()
        stack = []
        stack.append(self.roots[index_name])
        while len(stack) != 0: 
            node = stack[0]
            del stack[0]
            bid = node.bid
            # not a leaf
            if not node.is_leaf(): 
                for child in node.children: 
                    stack.append(child)
                # go to corresponding block
                # self.buffer_manager.read_block(index_name, 1, bid)
                # print(node.keys)
                num = len(node.keys)  # number of keys
                cur_offset = 0
                content = struct.pack('=?h', node.isleaf, num)
                self.buffer_manager.write(index_name, 1, bid, cur_offset, content, 3)
                cur_offset += 3
                for i in range(num): 
                    content = struct.pack('=hh', node.children[i].bid, 0)
                    self.buffer_manager.write(index_name, 1, bid, cur_offset, content, 4)
                    cur_offset += 4
                    if type[-1:] == 's': 
                        content = struct.pack('='+type, node.keys[i].encode('utf-8'))
                    else: 
                        content = struct.pack('='+type, node.keys[i])
                    self.buffer_manager.write(index_name, 1, bid, cur_offset, content, length)
                    cur_offset += length
                # add the last pointer
                content = struct.pack('=hh', node.children[num].bid, 0)
                self.buffer_manager.write(index_name, 1, bid, cur_offset, content, 4)
                self.buffer_manager.commitOne(index_name, 1, bid)
            # a leaf
            else :
                # print(node.keys)
                num = len(node.keys)  # number of keys
                cur_offset = 0
                content = struct.pack('=?h', node.isleaf, num)
                self.buffer_manager.write(index_name, 1, bid, cur_offset, content, 3)
                cur_offset += 3
                for i in range(num): 
                    content = struct.pack('=hh', node.children[i][0], node.children[i][1])
                    self.buffer_manager.write(index_name, 1, bid, cur_offset, content, 4)
                    cur_offset += 4
                    if type[-1:] == 's': 
                        content = struct.pack('='+type, node.keys[i].encode('utf-8'))
                    else: 
                        content = struct.pack('='+type, node.keys[i])
                    self.buffer_manager.write(index_name, 1, bid, cur_offset, content, length)
                    cur_offset += length
                # add the last pointer
                if node.children[num] is None: 
                    content = struct.pack('=hh', -1, -1)
                else: 
                    content = struct.pack('=hh', node.children[num].bid, 0)
                self.buffer_manager.write(index_name, 1, bid, cur_offset, content, 4)
                self.buffer_manager.commitOne(index_name, 1, bid)

    def create_index(self, index_name, addresses, values, order):
        self.build_Bplus(index_name, addresses, values, order)
        self.print_tree(index_name)

    # may be of no use, do not use
    def drop_index(self, index_name):
        if index_name in self.roots.keys(): 
            del self.roots[index_name]
        else : 
            raise Exception('No such index "%s" in the memory'%index_name)

    # existence is checked outside index manager
    def drop_index_file(self, index_name):
        os.chdir(sys.path[0])
        os.remove('./index/'+index_name+'.ind')
        

    def print_tree(self, index_name): 
        stack = []
        bid = 0
        stack.append([self.roots[index_name], 1])
        while len(stack) != 0: 
            node, level = stack[0]
            node.bid = bid
            bid += 1
            del stack[0]
            if not node.is_leaf(): 
                for child in node.children: 
                    stack.append([child, level+1])
            # print('level: ', level)
            # print('is_leaf: ', node.isleaf)
            # print('bid: ', node.bid)
            # print('keys: ', node.keys)
            # print('--------------')

    def saveAll(self, index_names, types, lengths): 
        for i in range(len(index_names)): 
            if index_names[i] in self.roots.keys(): 
                self.save_Bplus(index_names[i], types[i], lengths[i])

    def build_from_file(self, index_name):
        pass 

# if __name__ == '__main__': 
#     buffer_m = buffer.bufferManager()
#     manager = index_manager(buffer_m) 
#     manager.drop_index_file('tobede')
#     index_name = 'test'
#     # values = [42, 151, 1, 1, 89, 196, 33, 61, 163, 139, 113, 24, 70, 55, 17, 31, 77, 27, 61, 20]
#     values = [42, 151, 1, 1, 89, 196, 33, 61, 163, 139, 113, 24]
#     addresses = [[40, 6], [17, 48], [6, 6], [16, 23], [37, 21], [39, 41], [23, 24], [19, 15], [24, 7], [11, 46], 
#                  [5, 24], [17, 3], [34, 22], [21, 8], [43, 44], [18, 40], [48, 12], [14, 47], [45, 8], [26, 15]]
#     # addresses = [[40, 6], [17, 48], [6, 6], [16, 23], [37, 21], [39, 41], [23, 24], [19, 15], [24, 7]]
#     manager.create_index(index_name, addresses, values, 4)
#     index_name = 'tt'
#     values = ['aaa', 'cde', 'xhice', 'xsc', 'hidcu', 'xhsayi', 'xui', 'chausi']
#     addresses = [[40, 6], [21, 8], [6, 6], [16, 23], [37, 21], [5, 24], [17, 3], [34, 22]]
#     manager.create_index(index_name, addresses, values, 4)
#     index_names = ['test', 'tt']
#     types = ['i', '10s']
#     lengths = [4, 10]
#     manager.saveAll(index_names, types, lengths)
#     print(manager.search('test', 196, 'i', 4))
#     print(manager.search('tt', 'xsc', '10s', 10))
#     print(manager.search('tt', 'xxx', '10s', 10))
