from Config import Config 
import json
import getpass
import paramiko
import sys
class site(Config):

    def __init__(self):
        print("Getting site details")
        super().__init__()
        self.host_file=self.get_property('HOSTS_FILE')
        self.manifest_file=self.get_property('MANIFEST_FILE')


    def get_connect_data(self,host_groups):
        print(self.host_file)
        try:
            f=open(self.host_file,'r')
        except IOError:
            print("Error: File does not appear to exist.")
            return False
        try:
            data=json.load(f)
        except:
            print("JSON load failef for file" + self.host_file)
        return data[host_groups]

    def get_exec_data(self,play_name):
        print(self.manifest_file)
        self.play_name=play_name
        try:
            f=open(self.manifest_file,'r')
        except IOError:
            print("Error: File does not appear to exist.")
            return False
        try:
            data=json.load(f)
        except:
            print("JSON load failef for file" + self.host_file)
        return data['play'][play_name]

 

class connect(site):

    def __init__(self):
        super().__init__()
        print("connecting "+self.host_file)

    def ssh(self,connect_data,command):
        for key, host in connect_data.items():
            print(host)
            self.ssh_hostname=host['ip']
            self.ssh_user=host['user']
            try:
                self.ssh_password = getpass.getpass()
            except Exception as error:
                print('ERROR', error)

            ssh = paramiko.SSHClient() 
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(self.ssh_hostname, username=self.ssh_user, password=self.ssh_password)
            except:
                print("[!] Cannot connect to the SSH Server")
            
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
            #except:
            if ssh_stdout.channel.recv_exit_status() != 0:
                print("Command execution failed \n--- \ncommand:%s \nstdout:%s \nstderr:%s \n---" %(command, ssh_stdout.read().decode(), ssh_stderr.read().decode()))
            
            print(ssh_stdout.read().decode())


class packages(connect):
    def __init__(self):
        super().__init__()
        print("packages ")
    def package_manager(self,package_list):
        dir(package_list)
        for package_name, status in package_list.items():
            if status == "present":
                print("installing package %s with available latest version" %package_name)
                connect_data=self.get_connect_data(self.play_name)
                print(connect_data)
                print('------------------')
                self.ssh(connect_data,'date')
            elif status == "absent":
                print("Removing package %s" %package_name)
            else:
                print("installing package %s with version %s" %(package_name,status))


if __name__ == '__main__':
    obj=packages()
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

