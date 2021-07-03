from Connect import Connect
class Actions(Connect):
    def __init__(self):
        super().__init__()
        print("packages ")

    def package_manager(self,package_list):
        connect_data=self.get_connect_data(self.play_name)
        for package_name, status in package_list.items():
            if status == "present":
                print("installing package %s with available latest version" %package_name)
                self.ssh(connect_data,'apt install -y %s' %package_name)
            elif status == "absent":
                print("Removing package %s" %package_name)
                self.ssh(connect_data,'apt remove -y %s' %(package_name))
            else:
                print("installing package %s with version %s" %(package_name,status))
                self.ssh(connect_data,'apt install -y %s=%s' %(package_name,status))