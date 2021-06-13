from catalog import catalog_manager
from interpreter import interpreter,set_catalog
from buffer import bufferManager
from record import record_manager
from index import index_manager
banner1 = \
'''
                                        __     
\    /_ | _ _ ._ _  _  _|_ _  |\/|o._ o(_  _.| 
 \/\/(/_|(_(_)| | |(/_  |_(_) |  ||| ||__)(_|| 
                                            |  

'''
banner2 = \
'''
 ▄    ▄   ▀             ▀                  ▀▀█                                      
 ██  ██ ▄▄▄    ▄ ▄▄   ▄▄▄     ▄▄▄    ▄▄▄▄    █                  ▄ ▄▄    ▄▄▄         
 █ ██ █   █    █▀  █    █    █   ▀  █▀ ▀█    █    ▄▄▄  ▄        █▀  █  ▀   █  ▄▄▄  ▄
 █ ▀▀ █   █    █   █    █     ▀▀▀▄  █   █    █    ▀  ▀▀▀        █   █  ▄▀▀▀█  ▀  ▀▀▀
 █    █ ▄▄█▄▄  █   █  ▄▄█▄▄  ▀▄▄▄▀  ▀█▄██    ▀▄▄                █   █  ▀▄▄▀█        
                                        █                                           
                                        ▀                                                                                  
'''
if __name__ == "__main__":
    print(banner2)
    catalog = catalog_manager()
    buffer = bufferManager()
    record = record_manager(buffer)
    index = index_manager(buffer)
    # set_catalog(catalog)
    # while True:
    #     data = input("sql>")
    #     interpreter(data)
