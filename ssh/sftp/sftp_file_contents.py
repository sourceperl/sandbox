import paramiko
from private_data import HOSTNAME, PORT, PWD, USER

TEST_ENV = False

# create SSH client
ssh = paramiko.SSHClient()

if TEST_ENV:
    # accept unknown hosts (test environment)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
else:
    # accept only known hosts (production environment)
    ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
    # first connect with ssh cli to update the system known_hosts file
    ssh.load_system_host_keys()

# connect to remote server
ssh.connect(hostname=HOSTNAME, port=PORT, username=USER, password=PWD)

# open SFTP session
sftp = ssh.open_sftp()

# open the remote file and read its contents as bytes
with sftp.open(filename='/home/pi/hello.txt', mode='rb') as remote_file:
    file_bytes = remote_file.read()

# show file contents
print(file_bytes[:100])

# close connections
sftp.close()
ssh.close()
