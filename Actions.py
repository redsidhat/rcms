from Connect import Connect
import re
import hashlib
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
            is_file_changed = False
            is_file_present = False
            server_md5 = ''
            #checking if file exist in server
            stdout, stderr = self.ssh(self.connect_data,'md5sum %s' %filename)

            if stdout.channel.recv_exit_status() == 0:
                is_file_present = True
                server_md5 = stdout.read().decode('ascii').split(' ')[0]

            if filedata['status'] == 'present':
                if 'content' in filedata:
                    file_content=filedata['content']

                elif 'source' in filedata:
                    with open(filedata['source'], 'r') as file:
                        file_content = file.read()
                else:
                    print("no file source or content defined skipping resource.")
                    break
                if not is_file_present:
                    print("write file here")
                else:
                    m = hashlib.md5()
                    m.update(file_content)
                    actul_md5=m.hexdigest()
                    if actul_md5 == server_md5:
                        print("No changes for file %s" %filename)
                    else:
                        print('write file')

            elif filedata['status'] =='directory':
                print("create dir")
            elif filedata['status'] =='absent':
                print("delete file")
            else:
                print("bad config.")
                break

                
