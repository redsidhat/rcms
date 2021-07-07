# RCMS
## _rudimentary configuration management system_



RCMS is a ssh based stand alone configuration management system built in python


## Features

- Package installtion, and removal with version number support
- File management - Creation, deletion, updation and refreshing services on content change
- Service managment - running, stopped, reloaded.




## code

Dillinger uses a number of open source projects to work properly:

- [main.py](https://github.com/terminalninja/rcms/blob/master/main.py) -  entry point
- [Actions.py](https://github.com/terminalninja/rcms/blob/master/Actions.py) - All the actions and commands
- [Connect.py](https://github.com/terminalninja/rcms/blob/master/Connect.py) - SSH connaction class
- [Site.py](https://github.com/terminalninja/rcms/blob/master/Site.py) - Reads manifests and other configs
- [Config.py](https://github.com/terminalninja/rcms/blob/master/Config.py) - Real configurations for the tool kep here
- [Express] - fast node.js network app framework [@tjholowaychuk]
- [Gulp] - the streaming build system
- [manifests.json](https://github.com/terminalninja/rcms/blob/master/manifests/manifests.json) - Manifest to apply on hosts
- [hosts.json](https://github.com/terminalninja/rcms/blob/master/hosts/hosts.json) - hosts file with ip and user to connect to and mapped to the manifest


## Installation

RCMS requires [python](https://www.python.org/downloads/release/python-380/) v3.8+ and [paramiko](http://www.paramiko.org/) to run.

Install the dependencies and devDependencies and run rcms.

```sh
cd rcms
pip3 install paramiko
python3 main.py
```

## Writting manifests

Supported manifests are mentioned as below.

Manifest file:
Always start with play followed by the play name (webserver here). Play name is mapped in the hosts file. Play will be applied to the hosts in hosts file that has the mapping to a particular play.
```json
{
    "play":{ 
        "webservers":{
            "packages":{
                "package_name1": "version_number",
                "package_name2": "absent",
                "package_name3":"present"
            },
    
            "files":{
                "/full/path/to/file":{
                    "source": "files/sourcefilename",
                    "owner": "owner_username",
                    "group": "group_name",
                    "chmod": 644,
                    "status": "absent or present", 
                    "refresh": "service_name"
                },
                "/full/path/to/directory":{
                    "owner": "root",
                    "group": "root",
                    "chmod": 755,
                    "status": "directory or absent"
                },
            },
            "services":{
                "service_name1":{
                    "status":"running or stop or restart"
                }
            }
        }
    }
}

```

Host file:

```json
{
    "webservers": {
        "host1": {
            "ip": "54.167.39.148",
            "user": "root"
        },
        "host2": {
            "ip": "35.175.188.148",
            "user": "root"
        }
    }
}
```

#### Limitations
