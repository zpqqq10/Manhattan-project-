from catalog import catalog_manager
from interpreter import interpreter,set_catalog,set_api
from buffer import bufferManager
from record import record_manager
from index import index_manager
from api import API
banner1 = \
'''
                                        __     
\    /_ | _ _ ._ _  _  _|_ _  |\/|o._ o(_  _.| 
 \/\/(/_|(_(_)| | |(/_  |_(_) |  ||| ||__)(_|| 
                                            |  

'''
banner = \
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
    # print(banner)
    catalog = catalog_manager()
    buffer = bufferManager()
    record = record_manager(buffer)
    index = index_manager(buffer)
    api = API(catalog, buffer, record, index)
    set_catalog(catalog)
    set_api(api)
    # support SHOW in the future
    print('tables:', end='')
    for tbl_name in catalog.tables.keys(): 
        print(' '+tbl_name, end='')
    print()
    print('indice:', end='')
    for idx_name in catalog.indices.keys(): 
        print(' '+idx_name, end='')
    print()
    
    while True:
        try:
            data = input("sql>")
            interpreter(data)
        except Exception as e:
            print(e)