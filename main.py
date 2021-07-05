from Actions import Actions

if __name__ == '__main__':
    obj=Actions()
    mods=obj.get_exec_data('webservers')
    connect_data=obj.get_connect_data('webservers')
    for connect in connect_data.items():
        print("running actions on =================%s:%s================" %(connect[0], connect[1]['ip']))
        obj.set_connect_data(connect) # I messed up, ssh function needed to return std err and out but I was sending multiple host data at once. spliting the data and looping it and setting it back with single host again here.
        for mod,key in mods.items():
            if mod=='packages':
                #actions=packages()
                #obj.package_manager(key)
                print("skip")
            elif mod=='files':
                #print(key)
                obj.file_manager(key)
            else:
                print("unsupported module")

            
