from Config import Config 
import json
import getpass

class Site(Config):

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
        # if 'ssh_password' not in locals():
        try:
            self.ssh_password = getpass.getpass()
        except Exception as error:
            print('ERROR', error)

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









