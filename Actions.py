from Connect import Connect
import re
class Actions(Connect):
    def __init__(self):
        super().__init__()
        print("packages ")

    def init_connections(self):
        self.connect_data=self.get_connect_data(self.play_name)

    def package_manager(self,package_list):
        #self.connect_data=self.get_connect_data(self.play_name)
        # print(self.connect_data)
        for package_name, status in package_list.items():
            available, installed , version= self.check_package_status(package_name)
            if status == "present" and installed:
                print("Package is already installed to version %s" %version)
            elif status == "present" and not installed and available:
                print("installing package %s with available latest version" %package_name)
                self.ssh(self.connect_data,'apt install -y %s' %package_name)
            elif status == 'present' and not available:
                print("Package %s is not available. Skipping installation")
            elif status == "absent" and installed:
                print("Removing package %s" %package_name)
                self.ssh(self.connect_data,'apt remove -y %s' %(package_name))
            elif status == "absent" and not installed:
                print("Package %s is not present no action needed" %package_name)
            elif status != "present" and status != "absent":
                if version == status:
                    print("Package %s is installed to version %s. no action needed" %(package_name, version))
                else:
                    print("installing package %s with version %s" %(package_name,status))
                    self.ssh(self.connect_data,'apt install -y %s=%s' %(package_name,status))

    def check_package_status(self, package_name):
        stdout, stderr = self.ssh(self.connect_data,'apt-cache policy %s' %(package_name))
        output=stdout.read().decode('ascii')
        if re.search(rf".*Installed:\s\(none\)", output):
            available=True
            installed=False
            version=None
        elif re.search(rf".*Installed:\s\d.*", output):
            available=True
            installed=True
            match=re.search(rf".*Installed:\s(\d.*)", output)
            version=match.group(1)

        else:
            available=False
            installed=False
            version=None
        return available, installed, version

    def file_manager(self,file_list):
        #self.connect_data=self.get_connect_data(self.play_name)
        for filename, filedata in file_list.items():
            print(filename)