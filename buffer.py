import os
import queue
import sys
from typing import NewType
from queue import Queue
block_size = 4096
max_page = 16

class bufferBlock():
    "Variable Specification: file & file_bid: the data source; modified: bool to identify"
    def __init__(self, content = None, file = None, file_bid = None, modified = False):
        self.content = content
        self.file = file
        self.file_bid = file_bid
        self.modified = modified

    def read(self, tbl_name, bid, off, length):
        "tbl_name: the name(NOT included the file extension); bid: block id of the file; off: offset value of the needed data beginning position ; length: the length of needed data"
        if self.modified : # if this block has been modified,commit it and reset it
            self.commit()
            self.content = self.file = self.file_bid = None
            self.modified = False
        os.chdir(sys.path[0]) # change to the same 
        path = "./record/" + tbl_name + ".rec"
        file = open(path, "rb")
        # Q: 这里要不要考虑给的bid超出文件上限的判断
        file.seek(block_size*bid, 0)
        self.content = file.read(block_size)
        self.file = path
        self.file_bid = bid
        result = self.content[off:(off + length)]
        # debug code begin:
        # print(self.content)
        # print(result)
        # debug code end
        return result

    def read_block(self, tbl_name, bid):
        "tbl_name: the name(NOT included the file extension); bid: block id of the file; "
        if self.modified : # if this block has been modified,commit it and reset it
            self.commit()
            self.content = self.file = self.file_bid = None
            self.modified = False
        os.chdir(sys.path[0]) # change to the same 
        path = "./record/" + tbl_name + ".rec"
        file = open(path, "rb")
        # Q: 这里要不要考虑给的bid超出文件上限的判断
        file.seek(block_size*bid, 0)
        self.content = file.read(block_size)
        self.file = path
        self.file_bid = bid
        return self.content

    def write(self, off, content, length):
        "off: offset value of the needed data beginning position; bid: block id of the file; content: binary data"
        # Q: 这里要不要做检测：1. content长是否为length; 2. content内容是否合法; 3. off + length是否超过上限
        self.modified = True
        data = self.content[0:off] + content + content[off + length:]
        self.content = data
        return True
        
    def commit(self):
        file = open(self.file, "wb")
        file.seek(block_size*self.file_bid, 0)
        file.write(self.content)
        file.close()
        self.modified = False


class bufferManager():
    def __init__(self):
        self.blockQueue = Queue(maxsize = max_page)
        for i  in range(max_page):
            item = bufferBlock()
            self.blockQueue.put(item)
        
    def read(self, tbl_name, bid, off, length):
        "tbl_name: the name(NOT included the file extension); bid: block id of the file; off: offset value of the needed data beginning position ; length: the length of needed data"
        block = self.blockQueue.get()
        result = block.read(tbl_name, bid, off, length)
        self.blockQueue.put(block)
        return result

    def read_block(self, tbl_name, bid):
        "tbl_name: the name(NOT included the file extension); bid: block id of the file; "
        block = self.blockQueue.get()
        result = block.read_block(tbl_name, bid)
        self.blockQueue.put(block)
        return result

    def write(self, off, content, length):
        "off: offset value of the needed data beginning position; bid: block id of the file; content: binary data"
        # Q: 这里要不要做检测：1. content长是否为length; 2. content内容是否合法; 3. off + length是否超过上限
        block = self.blockQueue.get()
        result = block.write(off, content, length)
        self.blockQueue.put(block)
    