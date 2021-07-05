from Actions import Actions

if __name__ == '__main__':
    obj=Actions()
    mods=obj.get_exec_data('webservers')
    connect_data=obj.get_connect_data('webservers')
    for connect in connect_data.items():
        print("\n\n==================================%s:%s=================================\n" %(connect[0], connect[1]['ip']))
        obj.set_connect_data(connect) # I messed up, ssh function needed to return std err and out but I was sending multiple host data at once. spliting the data and looping it and setting it back with single host again here.
        for mod,key in mods.items():
            if mod=='packages':
                print("-------------PACKAGES-START-------------")
                obj.package_manager(key)
                print("-------------PACKAGES-FINISH------------\n\n")
            elif mod=='files':
                print("-------------FILES-START----------------")
                obj.file_manager(key)
                print("-------------FILES-FINISH---------------\n\n")
            else:
                print("unsupported module")

            
