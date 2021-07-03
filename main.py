from Actions import Actions

if __name__ == '__main__':
    obj=Actions()
    mods=obj.get_exec_data('webservers')
    for mod,key in mods.items():
        if mod=='packages':
            print(key)
            #actions=packages()
            obj.package_manager(key)
        else:
            print("unsupported module")

            
