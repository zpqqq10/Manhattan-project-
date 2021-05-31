import os
import struct
import sys

class record_manager():
    def __init__(self):
        pass

    def new_table(tbl_name): 
        os.chdir(sys.path[0])
        file = open('./table/'+tbl_name+'.rec', 'wb+')
        file.write(struct.pack('h', 0)) # block id
        file.write(struct.pack('h', 8)) # offset
        file.close()

    def insert(tbl_name, attribute): 
        pass

    def remove(tbl_name, attribute): 
        pass

# record_manager.new_table('xyz')
# print('success')