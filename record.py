import struct
import os
import sys
from functools import reduce


class record_manager:
    def __init__(self):
        print(1)

    # attr here is teh format of struct
    def insert(self, tbl_name, attr, value):
        # temporarily use file open, lately will use buffer
        f = open("./record/"+tbl_name+".rec", "rb+")
        bytes = f.read(8)
        # buffer.read(tbl_name,0,0,8)
        print(bytes)
        valid_bytes, free_bid, free_off, tail_flag, length = struct.unpack(
            "=?hh?h", bytes)
        print(valid_bytes, free_bid, free_off, length, tail_flag)
        if tail_flag == False:
            # wirte the record in free_bid:free_off
            f.seek(free_bid * 4096 + free_off * 8, 0)
            # if the free record is not the tail, get the first bytes which record the pre free list head
            pre_free_list = f.read(6)
            # buffer.read(tbl_name,free_bid,free_off,6)

        length_ = sum([i[2] for i in attr]) + 1
        pad_num = (length << 3) - length_
        bytes = struct.pack("=?", True)+reduce(lambda x, y: x+y, map(lambda x,
                                                                     y: struct.pack(x[1], y), attr, value))
        bytes += pad_num * struct.pack("=x")
        print(bytes)
        # wirte the record in free_bid:free_off
        f.seek(free_bid * 4096 + free_off * 8, 0)
        f.write(bytes)
        # buffer.write(tbl_name,free_bid,free_off,length << 3,bytes)
        if tail_flag:
            new_off = free_bid * 4096 + free_off*8 + (length << 3)
            # compute the next free record
            next_free_bid = new_off // 4096
            next_free_off = new_off % 4096 >> 3
            if (4096 - free_off * 8) < length * 8:
                next_free_bid = free_bid + 1
                next_free_off = 0
            # print(next_free_bid,next_free_off,new_off)
            bytes = struct.pack(
                "=?hh?", False, next_free_bid, next_free_off, True)
        else:
            bytes = pre_free_list
        f.seek(0, 0)
        f.write(bytes)
        f.close()
        # buffer.write(tbl_name,0,0,bytes,6)

    def delete_with_index(self, tbl_name, bid, off):
        # temporarily use file open, lately will use buffer
        f = open("./record/"+tbl_name+".rec", "rb+")
        free_list = f.read(6)                           # read the free_list
        f.seek(bid * 4096 + off * 8, 0)
        f.write(free_list)
        # buffer.write(tbl_name,bid,off,free_list,6)
        bytes = struct.pack("=?hh?", False, bid, off, False)
        f.seek(0, 0)
        f.write(bytes)
        f.close()

    def create(self, tbl_name, attr):
        # the header of a record file, every record align to 8
        # 0             the bool the valid byte
        # 1,2           the header of freelist:block id
        # 3,4           the header of freelist:offset,the offset need to multiple 8 to get the real offset
        # 5             bool if the freelist point to the tail
        # 6,7           the lenghth of a record
        # the first block...
        length = sum([i[2] for i in attr]) + 1
        # length = sum(attr[i][2]) mod 8
        length = (length % 8 != 0) + (length >> 3)
        content = struct.pack("=?hh?h", False, 0, 1, True, length)
        print(content)
        with open("./record/"+tbl_name+".rec", "wb") as f:
            f.write(content)
            f.close()
        return 0

    def scan_all(self, attr):
        print(1)


if __name__ == "__main__":
    # test
    os.chdir(sys.path[0])
    t = record_manager()
    t.create("abc", [("a", "l", 4), ("b", "l", 4)])
    t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (4, 8))
    t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (4, 8))
    t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (5, 6))
    t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (3, 7))
    t.delete_with_index("abc", 0, 3)
    t.delete_with_index("abc", 0, 1)
    # t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (5, 6))
    # t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (3, 7))
