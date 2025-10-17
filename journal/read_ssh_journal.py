""" Prints SSH connection logs from the systemd journal for the last 24h. """

from datetime import datetime, timedelta

# sudo apt install python3-systemd
from systemd import journal

reader = journal.Reader()
reader.add_match(_SYSTEMD_UNIT='ssh.service')
reader.log_level(journal.LOG_INFO)
reader.seek_realtime(datetime.now() - timedelta(hours=24))

for entry in reader:
    entry_dt = entry['__REALTIME_TIMESTAMP']
    entry_msg = entry['MESSAGE']
    print(f'{entry_dt}: {entry_msg}')
