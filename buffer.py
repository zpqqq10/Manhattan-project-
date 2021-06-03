import os
import sys
block_size = 4096

class Buffer():
    def __init__():
        pass
    
    # relative path
    def read_block(path, block_id): 
        os.chdir(sys.path[0])
        file = open(path, "rb")
        file.seek(block_size*block_id, 0)
        content = file.read(block_size)
        return content

    def write_blcok(path, block_id, content): 
        pass

    def new_block(): 
        # buffer or memory management
        return bytearray(4096)

    def read_content(path, position, n):	# read the content of length n
        pass

    def commit(path): 	# save the update of the file?
        pass