from Connect import Connect
import re
import hashlib
class Actions(Connect):
    def __init__(self):
        super().__init__()
        # print("Actions are initiated")

    # def init_connections(self):
    #     self.connect_data=self.get_connect_data(self.play_name)
        # print("Initiated connect data")
        # print(self.connect_data)

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
            print("Processing file %s" %filename)
            is_file_content_changed = False
            is_file_present = False
            is_file_permission_changed = False
            server_md5 = ''
            actul_md5 = ''
            #checking if file exist in server


            if filedata['status'] == 'present':
                stdout, stderr = self.ssh(self.connect_data,'md5sum %s' %filename)
                if stdout.channel.recv_exit_status() == 0:
                    is_file_present = True
                    server_md5 = stdout.read().decode('ascii').split(' ')[0]
                   # file_permission = awk '{k=0;for(i=0;i<=8;i++)k+=((substr($1,i+2,1)~/[rwx]/) *2^(8-i));if(k)printf("%0o ",k);print $1}'
                    cmd="stat -c '%a %U %G' "+ filename
                    stdout, stderr = self.ssh(self.connect_data, cmd )
                    output = stdout.read().decode('ascii').strip('\n').split(' ')
                    server_file_permisison = output[0]
                    server_file_owner= output[1]
                    server_file_group= output[2]
                    if filedata['owner'] != server_file_owner or filedata['group'] != server_file_group:
                        is_file_permission_changed= True
                        print("updating ownership for %s" %filename)
                        self.ssh(self.connect_data, 'chown %s:%s %s' %(filedata['owner'],filedata['group'], filename) )
                    if filedata['chmod'] != int(server_file_permisison):
                        is_file_permission_changed = True
                        print("updating permissions for %s" %filename)
                        self.ssh(self.connect_data, 'chmod %s %s' %(filedata['chmod'], filename))

                if 'source' in filedata:
                    with open(filedata['source'], 'r',) as file:
                        file_content = file.read()
                        actul_md5 = hashlib.md5()
                        actul_md5.update(file_content.encode())
                else:
                    print("no file source or content defined skipping resource.")
                    break
                if not is_file_present:
                    is_file_content_changed = True
                else:
                    if actul_md5.hexdigest() == server_md5:
                        print("No changes for file %s" %filename)
                    else:
                        is_file_content_changed = True

                if is_file_content_changed:
                    stdout, stderr = self.ssh(self.connect_data,'echo -n %s>%s' %(file_content,filename))
                else:
                    print("no write required %s" %filename)


            elif filedata['status'] =='directory':
                stdout, stderr = self.ssh(self.connect_data,'mkdir -p %s' %(filename))
            elif filedata['status'] =='absent':
                stdout, stderr = self.ssh(self.connect_data,'rm -f %s' %(filename))
            else:
                print("bad config.")
                break

                
