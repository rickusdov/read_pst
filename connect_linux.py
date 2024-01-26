import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('37.27.52.55', username='dolvera', password='c2ded606ff2e8a5276c')

ssh2 = paramiko.SSHClient()
ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh2.connect('192.168.56.50', username='dolvera', password='cxzcxz',
sock=ssh.get_transport().open_channel('direct-tcpip', ('192.168.56.50', 22), ('37.27.52.55', 22)))
# ssh_b.send('python3 MA_test/connect.py\n')
# ssh_b.send('from remote_script import get_mysql_connection\n')
# ssh_b.send('mysql_connection = get_mysql_connection()\n')
ssh2.exec_command('python3 MA_test/connect_test.py')
ssh2.exec_command('from connect_test import connect')
ssh2.exec_command('mysql_connection = connect()')
stdin.close()
print(mysql_connection)
# cur.execute("SELECT * FROM ac_directories")
# rows = cur.fetchall()
# print(rows)
ssh.close()
ssh2.close()