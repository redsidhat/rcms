from Actions import Actions
if __name__ == '__main__':
    obj=Actions()
#    obj.ssh('webservers','host1','date1')
    mods=obj.get_exec_data('webservers')
    for mod,key in mods.items():
        if mod=='packages':
            print(key)
            #actions=packages()
            obj.package_manager(key)
        else:
            print("unsupported module")

            
   # print(str(obj.get_host_ip('webservers','host1','ip')))
