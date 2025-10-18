""" Prints systemd log events in real time. """

import select

# sudo apt install python3-systemd
from systemd import journal

# init journal reader
reader = journal.Reader()
reader.log_level(journal.LOG_INFO)

# move the read cursor to the end of the journal (the latest entry).
# this is done to ensure we only read new, live entries added *after* this point.
reader.seek_tail()
# read the entry just before the tail to correctly position the cursor
reader.get_previous()

# polling setup (monitor file descriptors for events)
p = select.poll()
# register the journal file descriptor
p.register(reader, reader.get_events())

# start the monitoring loop ('p.poll()' will block and wait until an event occurs)
while p.poll():
    # process only new entries added to the end of journal, skip other events
    if reader.process() != journal.APPEND:
        continue
    # read all new messages available
    for entry in reader:
        entry_dt = entry['__REALTIME_TIMESTAMP']
        entry_sys_unit = entry.get('_SYSTEMD_UNIT', 'kernel')
        entry_msg = entry['MESSAGE']
        if entry_msg != "":
            print(f'{entry_dt} {entry_sys_unit}: {entry_msg}')
