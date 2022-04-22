import sys, paramiko, getpass, socket, time

authenication_failed_list = []
ip_unreachable_list = []

username =  input('Username: ')
password = getpass.getpass('Password: ')

ipfile = open('iplist.txt', 'r')

for ip in ipfile.readlines():
    try:
        ip = ip.strip()
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip, username=username, password=password, look_for_keys=False)
        print('Sucessfully connected to ', ip)
        command = ssh_client.invoke_shell()
        cmdfile = open('cmdlist.txt', 'r')
        cmdfile.seek(0)
        for cfgline in cmdfile.readlines():
            command.send(cfgline + '\n')
        time.sleep(1)
        output = command.recv(65535)
        print(output.decode('ascii'))
    except paramiko.ssh_exception.AuthenticationException:
        print('user authenication failed for' + ip + '.')
        authenication_failed_list.append(ip)
    except socket.error:
        print(ip + ' is unreachable.')
        ip_unreachable_list.append(ip)
ipfile.close()
cmdfile.close()
ssh_client.close()
print('User authenication failed for below sw: ')
for sw in ip_unreachable_list:
    print(sw)
print('ip unreachable for below sw: ')
for sw in authenication_failed_list:
    print(sw)

