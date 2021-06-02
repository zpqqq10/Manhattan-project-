import struct
import os
import sys
from functools import reduce
class record_manager:
    def __init__(self):
        print(1)

    def insert(self, tbl_name, attr, value):
        # temporarily use file open, lately will use buffer
        f = open("./record/"+tbl_name, "rb+")
        bytes = f.read(8)
        # buffer.read(tbl_name,0,0,8)
        free_bid, free_off, tail_flag, length = struct.unpack("hh?h", bytes)
        print(free_bid, free_off, length, tail_flag)
        if tail_flag == False:
            # wirte the record in free_bid:free_off
            f.seek(free_bid * 4096 + free_off * 8, 0)
            # if the free record is not the tail, get the first bytes which record the pre free list head
            pre_free_list = f.read(5)
            # buffer.read(tbl_name,free_bid,free_off,5)
        length_ = sum([i[2] for i in attr])
        pad_num = (length << 3) - length_
        bytes = reduce(lambda x, y: x+y, map(lambda x,
                                             y: struct.pack(x[1], y), attr, value))
        bytes += pad_num * struct.pack("x")
        print(bytes)
        # wirte the record in free_bid:free_off
        f.seek(free_bid * 4096 + free_off * 8, 0)
        f.write(bytes)
        # buffer.write(tbl_name,free_bid,free_off,length,bytes)
        if tail_flag:
            new_off = free_bid * 4096 + free_off*8 + 8
            # compute the next free record
            free_bid = new_off // 4096
            free_off = new_off % 4096 >> 3
            bytes = struct.pack("hh?", free_bid, free_off, True)
        else:
            bytes = pre_free_list
        f.seek(0, 0)
        f.write(bytes)
        # buffer.write(tbl_name,0,0,bytes,5)

    def delete_with_index(self, tbl_name, bid, off):
        # temporarily use file open, lately will use buffer
        f = open("./record/"+tbl_name, "rb+")
        free_list = f.read(5)                           # read the free_list
        f.seek(bid * 4096 + off * 8, 0)
        f.write(free_list)
        # buffer.write(tbl_name,bid,off,free_list,5)
        bytes = struct.pack("hh?",bid,off,False)
        f.seek(0,0)
        f.write(bytes)
    def create(self, tbl_name, attr):
        # the header of a record file, every record align to 8
        # 0,1           the header of freelist:block id
        # 2,3           the header of freelist:offset,the offset need to multiple 8 to get the real offset
        # 4             bool if the freelist point to the tail
        # 5,6           the lenghth of a record
        # 7             pad
        # the first block...
        length = sum([i[2] for i in attr])
        # length = sum(attr[i][2]) mod 8
        length = (length % 8 != 0) + (length >> 3)
        content = struct.pack("hh?hx", 0, 1, True, length)
        print(content)
        with open("./record/"+tbl_name, "wb+") as f:
            f.write(content)
            f.close()
        return 0


if __name__ == "__main__":
    # test 
    os.chdir(sys.path[0])
    t = record_manager()
    t.create("abc",[("a","l",4),("b","l",4)])
    t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (4, 8))
    # t.delete_with_index("abc",0,1)
    # t.delete_with_index("abc",0,2)
