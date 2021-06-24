from catalog import catalog_manager
from interpreter import interpreter,set_catalog,set_api
from buffer import bufferManager
from record import record_manager
from index import index_manager
from api import API

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
    print(banner)
    catalog = catalog_manager()
    buffer = bufferManager()
    record = record_manager(buffer)
    index = index_manager(buffer)
    api = API(catalog, buffer, record, index)
    set_catalog(catalog)
    set_api(api)
    
    while True:
        try:
            data = input("minisql>")
            interpreter(data)
        except Exception as e:
            print(e)