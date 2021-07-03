import paramiko
from Site import Site
class Connect(Site):

    def __init__(self):
        super().__init__()
        # print("connecting "+self.host_file)

    def ssh(self,connect_data,command):
        for key, host in connect_data.items():
            self.ssh_hostname=host['ip']
            self.ssh_user=host['user']
            
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
            
            else:
                print("command %s executed successfully " %command)
            return ssh_stdout, ssh_stderr