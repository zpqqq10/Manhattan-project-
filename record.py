import struct
import os
import sys
from buffer import bufferManager,bufferBlock
from functools import reduce


class record_manager:
    def __init__(self,buffer):
        self.buffer_manager = buffer

    # attr here is teh format of struct
    def insert(self, tbl_name, attr, value):
        # temporarily use file open, lately will use buffer
        f = open("./record/"+tbl_name+".rec", "rb+")
        bytes = f.read(8)
        # buffer.read(tbl_name,0,0,8)
        valid_bytes, free_bid, free_off, tail_flag, length = struct.unpack(
            "=?hh?h", bytes)
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
        # wirte the record in free_bid:free_off
        f.seek(free_bid * 4096 + free_off * 8, 0)
        f.write(bytes)
        # buffer.write(tbl_name,free_bid,free_off,length << 3,bytes)
        if tail_flag:
            # compute the next free record
            next_free_bid = free_bid
            next_free_off = free_off+length
            if (4096 - next_free_off * 8 ) < length * 8:
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
        return (free_bid,free_off)
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
        with open("./record/"+tbl_name+".rec", "wb") as f:
            f.write(content)
            f.close()
        return 0
    # contraint list of tumples
    # (attr_index0,ops,value)
    # ops (<,0) (<=,1) (>,2) (>=,3) (==,4)
    def check_record(self,record,attr,constraint):
        for item in constraint:
            if item[1] == 0:
                if record[item[0]+1] < item[2]:
                    continue
                else:
                    return False 
            elif item[1] == 1:
                if record[item[0]+1] <= item[2]:
                    continue
                else:
                    return False 
            elif item[1] ==2:
                if record[item[0]+1] > item[2]:
                    continue
                else:
                    return False 
            elif item[1] == 3:
                if record[item[0]+1] >= item[2]:
                    continue
                else:
                    return False 
            elif item[1] == 4:
                if record[item[0]+1] == item[2]:
                    continue
                else:
                    return False 
        return True
    # this methods return the list of tuples corresponding to the constraints
    def scan_all(self,tbl_name,constraint, attr):
        f = open("./record/"+tbl_name+".rec", "rb+")
        bid = 0
        result = []
        format = "=?"+reduce(lambda x,y:x+y[1],attr,"")
        record_length_r = sum([i[2] for i in attr]) + 1
        block_len = 4096 >>3
        while block_len == 512:
            #content = buffer.read_block(tbl_name,bid)
            block_content = f.read(4096)
            block_len = len(block_content)
            block_len = block_len >> 3
            idx = 0
            if bid==0:
                valid_bytes, free_bid, free_off, tail_flag, record_length_a = struct.unpack("=?hh?h", block_content[:8])
                idx += 1
            while idx + record_length_a <= block_len:
                record = struct.unpack(format,block_content[idx<<3:(idx<<3)+record_length_r])
                
                if record[0] & self.check_record(record,attr,constraint):
                    result.append(record)
                idx += record_length_a
            bid = bid + 1
        return result        
    # domain : a list of tuples (bid,off)
    #(bid,off) should be valid, this methods will not check the correctness
    def scan_with_index(self,tbl_name,constraint,attr,domain):
        f = open("./record/"+tbl_name+".rec", "rb+")
        result = []
        format = "=?"+reduce(lambda x,y:x+y[1],attr,"")
        record_length_r = sum([i[2] for i in attr]) + 1
        for item in domain:
            f.seek(item[0] * 4096+ item[1] * 8)
            content = f.read(record_length_r)
            record = struct.unpack(format,content)
            if record[0] & self.check_record(record,attr,constraint):
                result.append(record)
        return result
            
if __name__ == "__main__":
    # test
    os.chdir(sys.path[0])
    buffer = bufferManager()
    t = record_manager(buffer)
    t.create("abc", [("a", "l", 4), ("b", "l", 4)])
    # t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (4, 8))
    # t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (4, 8))
    # t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (5, 6))
    # t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (3, 7))
    for i in range(10):
        t.insert("abc", [("a", "i", 4), ("b", "i", 4)],(i%10,(i+1)%10))
    t.delete_with_index("abc", 0, 3)
    t.delete_with_index("abc", 0, 1)
    print(t.scan_all("abc",[(0,2,2)], [("a", "l", 4), ("b", "l", 4)]))
    print(t.scan_with_index("abc",[(0,2,2)], [("a", "l", 4), ("b", "l", 4)],[(0,7),(0,5)]))
    # t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (5, 6))
    # t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (3, 7))
    # t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (22, 27))
