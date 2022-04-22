import paramiko
import getpass
import time

username = input('Username: ')
password = getpass.getpass('Password: ')

for i in range(201, 204):
    ip  = '10.9.13.' + str(i)
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)
    print('Sucessfully connected to ', ip)
    command = ssh_client.invoke_shell()
    command.send('config t\n')
    command.send('router ospf 1\n')
    command.send('router-id ' + ip + '\n')
    command.send('end\n')
    command.send('wr\n')
    time.sleep(2)
    out = command.recv(65535)
    print(out.decode('ascii'))
ssh_client.close()

