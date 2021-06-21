import struct
import os
import sys
from buffer import bufferManager,bufferBlock
from functools import reduce


class record_manager:
    def __init__(self,buffer):
        self.buffer_manager = buffer

    """
    tbl_name        : the name of the table
    attr            : the list of the attribute tuple
    value           : the tuple of value inserted
    return value    : the tuple (bid,off)  indicates the position the new record inserted
    """
    def insert(self, tbl_name, attr, value):
        # temporarily use file open, lately will use buffer
        bytes = self.buffer_manager.read(tbl_name,0,0,0,8)
        valid_bytes, free_bid, free_off, tail_flag, length = struct.unpack(
            "=?hh?h", bytes)
        if tail_flag == False:
            # wirte the record in free_bid:free_off
            # if the free record is not the tail, get the first bytes which record the pre free list head
            
            pre_free_list = self.buffer_manager.read(tbl_name,0,free_bid,free_off << 3,6)

        length_ = sum([i[2] for i in attr]) + 1
        pad_num = (length << 3) - length_
        bytes = struct.pack("=?", True)+reduce(lambda x, y: x+y, map(lambda x,
                                                                     y: struct.pack(x[1], y), attr, value))
        bytes += pad_num * struct.pack("=x")
        # wirte the record in free_bid:free_off
        self.buffer_manager.write(tbl_name,0,free_bid,free_off << 3,bytes,length << 3)
        if tail_flag:
            # compute the next free record
            next_free_bid = free_bid
            next_free_off = free_off+length
            if (4096 - next_free_off * 8 ) < length * 8:
                next_free_bid = free_bid + 1
                next_free_off = 0
            bytes = struct.pack(
                "=?hh?", False, next_free_bid, next_free_off, True)
        else:
            bytes = pre_free_list
        self.buffer_manager.write(tbl_name,0,0,0,bytes,6)
        return (free_bid,free_off << 3)
        
    """
    tbl_name        : the name of the table
    bid             : the bid of the record need to be delete
    off             : the offset of the record in the block
    return value    : none 
    """
    def delete_with_index(self, tbl_name, bid, off):
        # temporarily use file open, lately will use buffer
        # read the free_list
        free_list = self.buffer_manager.read(tbl_name,0,0,0,6)
        self.buffer_manager.write(tbl_name,0,bid,off,free_list,6)
        bytes = struct.pack("=?hh?", False, bid, off >> 3, False)
        self.buffer_manager.write(tbl_name,0,0,0,bytes,6)
    """
    tbl_name        : the name of the table
    attr            : the list of the attribute tuple
    return value    : none
    """
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
    """
    record          : the tuple of record 
    attr            : the list of the attribute tuple
    constraint      : the constraint list of tuples
    return value    : True if the record match the constraint
    """
    # constraint list of tuples
    # (attr_index0,ops,value)
    # ops (<,0) (<=,1) (>,2) (>=,3) (=,4) (<>, 5)
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
            elif item[1] == 5: 
                if record[item[0]+1] != item[2]: 
                    continue
                else: 
                    return False
        return True
    # this methods return the list of tuples corresponding to the constraints
    """
    tbl_name        : the name of the table
    constraint      : the constraint list of tuples
    attr            : the list of the attribute tuple 
    return value    : a tuple of two result list: list of the record value and list of the position of record 
    """
    def scan_all(self,tbl_name,constraint, attr):
        bid = 0
        result_record = []
        result_ptr = []
        format = "=?"+reduce(lambda x,y:x+y[1],attr,"")
        record_length_r = sum([i[2] for i in attr]) + 1
        block_len = 4096
        while block_len == 4096:
            block_content = self.buffer_manager.read_block(tbl_name,0,bid)
            block_len = len(block_content)
            idx = 0
            if bid==0:
                valid_bytes, free_bid, free_off, tail_flag, record_length_a = struct.unpack("=?hh?h", block_content[:8])
                idx += 8
            while idx + record_length_a * 8 <= block_len:
                record = struct.unpack(format,block_content[idx:idx+record_length_r])
                if record[0] & self.check_record(record,attr,constraint):
                    result_record.append(record[1:])
                    result_ptr.append((bid,idx))
                idx += record_length_a*8
            bid = bid + 1
        result = (result_record,result_ptr)
        return result        
    # domain : a list of tuples (bid,off)
    #(bid,off) should be valid, this methods will not check the correctness
    """
    tbl_name        : the name of the table
    constraint      : the constraint list of tuples
    attr            : the list of the attribute tuple 
    domain          : the list of the position of the record need to be scanned
    return value    : a tuple of two result list: list of the record value and list of the position of record 
    """
    def scan_with_index(self,tbl_name,constraint,attr,domain):
        result_record = []
        result_ptr = []
        format = "=?"+reduce(lambda x,y:x+y[1],attr,"")
        record_length_r = sum([i[2] for i in attr]) + 1
        for item in domain:
            content = self.buffer_manager.read(tbl_name,0,item[0],item[1],record_length_r)
            record = struct.unpack(format,content)
            if record[0] & self.check_record(record,attr,constraint):
                result_record.append(record[1:])
                result_ptr.append(item)
        return (result_record,result_ptr)

    # existence is checked outside record manager
    def drop_record_file(self, tbl_name):
        os.chdir(sys.path[0])
        os.remove('./record/'+tbl_name+'.rec')
            
if __name__ == "__main__":
    # test
    os.chdir(sys.path[0])
    buffer = bufferManager()
    t = record_manager(buffer)
    t.drop_record_file('tobe')
    # t.create("abc", [("a", "l", 4), ("b", "l", 4)])
    # print(t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (4, 8)))
    # print(t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (5, 6)))
    # print(t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (3, 7)))
    # for i in range(600):
    #     t.insert("abc", [("a", "i", 4), ("b", "i", 4)],(i%100,(i+1)%100))
    # t.delete_with_index("abc", 0, 8)
    # t.delete_with_index("abc", 0, 24)
    # print(t.scan_all("abc",[(0,2,98)], [("a", "l", 4), ("b", "l", 4)]))
    # print(t.scan_with_index("abc",[(0,1,98)], [("a", "l", 4), ("b", "l", 4)],[(0,8),(0,24)]))
    # print(t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (5, 6)))
    # print(t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (3, 7)))
    # print(t.insert("abc", [("a", "i", 4), ("b", "i", 4)], (22, 27)))
    # t.buffer_manager.commitAll()
