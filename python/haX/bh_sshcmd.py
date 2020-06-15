import threading
import paramiko
import subprocess
import sys

def ssh_command(ip, ssh_port, user, passwd, command):
    client = paramiko.SSHClient()
    client.load_host_keys('/home/sjbavier/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=ssh_port, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    
    if ssh_session.active:
        ssh_session.exec_command(command)
        print(ssh_session.recv(1024).decode("utf-8"))
    return

# incorportate CLI arguments            
server = sys.argv[1]
ssh_port = int(sys.argv[2])
command = sys.argv[3]

ssh_command(server, ssh_port , 'userA', 'passwd', command)