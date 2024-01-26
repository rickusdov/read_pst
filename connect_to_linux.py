import paramiko

def connect_to_linux(ip, username, password):
    port = 22
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command('ls')
    print(stdout.read().decode('utf-8'))
    ssh.close()
connect_to_linux('37.27.52.55', 'dolvera', 'c2ded606ff2e8a5276c')
