from Config import Config 
import json
import getpass
import paramiko

class site(Config):

    def __init__(self):
        print("Getting site details")
        super().__init__()
        self.host_file=self.get_property('HOSTS_FILE')


    def get_connect_data(self,hosts,hostname,property):
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
        return data[hosts][hostname][property]


 

class connect(site):

    def __init__(self):
        super().__init__()
        print("connecting "+self.host_file)

    def ssh(self,hosts,hostname,command):
        self.ssh_hostname=self.get_connect_data(hosts,hostname,'ip')
        self.ssh_user=self.get_connect_data(hosts,hostname,'user')
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

if __name__ == '__main__':
    obj=connect()
    obj.ssh('webservers','host1','date1')
   # print(str(obj.get_host_ip('webservers','host1','ip')))

