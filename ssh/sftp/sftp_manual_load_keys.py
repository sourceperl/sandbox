import io
from base64 import b64decode
from pathlib import Path

from paramiko import PKey, RejectPolicy, RSAKey, SSHClient
from private_data_2 import HOSTNAME, PORT, USER

# create SSH client
ssh = SSHClient()

# only accept known hosts (production environment)
ssh.set_missing_host_key_policy(RejectPolicy())

# update custom known_hosts with your server public key
host_keys = ssh.get_host_keys()
# use ssh-keyscan HOSTNAME to get this
srv_ed25519_str = 'AAAAC3NzaC1lZDI1NTE5AAAAIDt3g+yCiOaRUIIm6vkxAs4aoEDchnM291nV95UGnJbQ'
srv_ed25519_pkey = PKey.from_type_string('ssh-ed25519', b64decode(srv_ed25519_str))
host_keys.add(hostname=HOSTNAME, keytype='ssh-ed25519', key=srv_ed25519_pkey)

# load current user private key as a string and use it to connect
openssh_private_key_as_str = open(Path.home() / '.ssh/id_rsa', mode='r').read()
pkey = RSAKey.from_private_key(io.StringIO(openssh_private_key_as_str))
print(f'client fingerprint is {pkey.fingerprint}')

# connect to remote server
ssh.connect(hostname=HOSTNAME, port=PORT, username=USER, pkey=pkey)

# open SFTP session
sftp = ssh.open_sftp()

# open the remote file and read its contents as bytes
with sftp.open(filename='carousel-img/index.sha256', mode='rb') as f:
    file_bytes = f.read()

# show file contents
print(file_bytes)

# close connections
sftp.close()
ssh.close()
