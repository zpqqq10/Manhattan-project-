import os
import time
import sys
from typing import NewType
block_size = 4096
max_page = 16
max_timestamp = 10000000000000 # 14位，比全部的毫秒级13位时间戳更大，置于minHeap的最后


class bufferBlock():
    "Variable Specification: file & file_bid: the data source; modified: bool to identify"
    def __init__(self, timestamp = max_timestamp, content = None, file = None, file_bid = None, modified = False):
        self.timestamp = timestamp
        self.content = content
        self.file = file
        self.file_bid = file_bid
        self.modified = modified
        
    def read(self, file_name, file_type, bid, off, length):
        "file_name: the name(NOT included the file extension); file_type: record(0) or index(1); bid: block id of the file; off: offset value of the needed data beginning position ; length: the length of needed data"
        if self.modified : # if this block has been modified,commit it and reset it
            self.commit()
            self.content = self.file = self.file_bid = None
            self.modified = False
        os.chdir(sys.path[0]) # change to the same
        if (file_type == 0):
            path = "./record/" + file_name + ".rec"
        else:
            path = "./index/" + file_name + ".ind"
        file = open(path, "rb")
        # Q: 这里要不要考虑给的bid超出文件上限的判断
        file.seek(block_size*bid, 0)
        self.content = file.read(block_size)
        self.file = path
        self.file_bid = bid
        result = self.content[off:(off + length)]
        self.refreshTimestamp()
        # debug code begin:
        # print(self.content)
        # print(result)
        # debug code end
        return result

    def read_block(self, file_name, file_type, bid):
        "file_name: the name(NOT included the file extension); file_type: record(0) or index(1); bid: block id of the file; "
        if self.modified : # if this block has been modified,commit it and reset it
            self.commit()
            self.content = self.file = self.file_bid = None
            self.modified = False
        os.chdir(sys.path[0]) # change to the same         
        if (file_type == 0):
            path = "./record/" + file_name + ".rec"
        else:
            path = "./index/" + file_name + ".ind"
        file = open(path, "rb")
        # Q: 这里要不要考虑给的bid超出文件上限的判断
        file.seek(block_size*bid, 0)
        self.content = file.read(block_size)
        self.file = path
        self.file_bid = bid
        self.refreshTimestamp()
        return self.content

    def write(self, off, content, length):
        "off: offset value of the needed data beginning position; bid: block id of the file; content: binary data"
        # Q: 这里要不要做检测：1. content长是否为length; 2. content内容是否合法; 3. off + length是否超过上限
        self.modified = True
        data = self.content[0:off] + content + content[off + length:]
        self.content = data
        self.refreshTimestamp()
        return True
        
    def commit(self):
        if self.modified == True:
            file = open(self.file, "ab+")
            file.seek(block_size*self.file_bid, 0)
            file.write(self.content)
            file.close()
            self.modified = False
        self.refreshTimestamp()
    
    def refreshTimestamp(self):
        self.timestamp = int(round(time.time() * 1000))


class bufferManager():
    def __init__(self):
        self.blockArray = bufferBlock[max_page]

    def LRU(self):
        minTimestamp = max_timestamp
        minIndex = 0
        for i in range(max_page):
            if self.blockArray[i].timestamp <= minTimestamp:
                minTimestamp = self.blockArray[i].timestamp
                minIndex = i
        return minIndex

    def read(self, file_name, file_type, bid, off, length):
        "file_name: the name(NOT included the file extension); file_type: record(0) or index(1); bid: block id of the file; off: offset value of the needed data beginning position ; length: the length of needed data"
        if (file_type == 0):
            path = "./record/" + file_name + ".rec"
        else:
            path = "./index/" + file_name + ".ind"
        findFlag = False
        for i in range(max_page):
            if self.blockArray[i].file == path  and self.blockArray[i].file_bid == bid:
                findFlag = True
                break
        if findFlag:
            result = self.blockArray[i].content[off:(off + length)]
        else:
            minIndex = self.LRU()
            self.blockArray[minIndex].commit()
            result = self.blockArray[minIndex].read(file_name, file_type, bid, off, length)
        return result

    def read_block(self, file_name, file_type, bid):
        "file_name: the name(NOT included the file extension); file_type: record(0) or index(1); bid: block id of the file; "
        if (file_type == 0):
            path = "./record/" + file_name + ".rec"
        else:
            path = "./index/" + file_name + ".ind"
        findFlag = False
        for i in range(max_page):
            if self.blockArray[i].file == path  and self.blockArray[i].file_bid == bid:
                findFlag = True
                break
        if findFlag:
            result = self.blockArray[i].content
        else:
            minIndex = self.LRU()
            self.blockArray[minIndex].commit()
            result = self.blockArray[minIndex].read_block(file_name, file_type, bid)
        return result

    def write(self, file_name, file_type, bid, off, content, length):
        "off: offset value of the needed data beginning position; bid: block id of the file; content: binary data"
        # Q: 这里要不要做检测：1. content长是否为length; 2. content内容是否合法; 3. off + length是否超过上限
        if (file_type == 0):
            path = "./record/" + file_name + ".rec"
        else:
            path = "./index/" + file_name + ".ind"
        findFlag = False
        for i in range(max_page):
            if self.blockArray[i].file == path and self.blockArray[i].file_bid == bid:
                findFlag = True
                break
        if findFlag:
            self.blockArray[i].write(off, content, length)
        else:
            minIndex = self.LRU()
            self.blockArray[minIndex].commit()
            self.blockArray[minIndex].read_block(file_name, file_type, bid)
            self.blockArray[minIndex].write(off, content, length)
    
    def commitAll(self):
        for i in range(max_page):
            self.blockArray[i].commit()
   

