#!/usr/bin/env python3

import tkinter as tk
import socket
import subprocess


# some functions
def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except socket.error:
        return False
    return True


def get_ips_list():
    return subprocess.check_output(['hostname', '--all-ip-addresses']).split()


# some class
class MainFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        # tk strings vars
        self.set_ipv4_str = tk.StringVar(value='10.0.0.1')
        self.ip_status_str = tk.StringVar(value='')
        # widgets setup
        self.ent_ipv4 = tk.Entry(self, width='16', justify=tk.CENTER,
                                 font=('Verdana', 30), textvariable=self.set_ipv4_str)
        self.ent_ipv4.pack(anchor='center', expand=True)
        self.but_set_ipv4 = tk.Button(self, text='Affectation de l\'adresse',
                                      font=('Verdana', 20), command=self.set_ipv4_addr)
        self.but_set_ipv4.pack(anchor='center', expand=True, ipadx=20, ipady=20)
        self.lab_ips = tk.Label(self, justify=tk.CENTER, font=('Verdana', 20), textvariable=self.ip_status_str)
        self.lab_ips.pack(anchor='center', expand=True, ipadx=50, ipady=50)
        # periodic job
        self.do_every(self.every_1s_job, every_ms=1000)
        # install callback
        self.set_ipv4_str.trace('w', self.ipv4_str_update)

    def ipv4_str_update(self, *args):
        if is_valid_ipv4_address(self.set_ipv4_str.get()):
            self.ent_ipv4.config(bg='white')
            self.but_set_ipv4.config(state='normal')
        else:
            self.ent_ipv4.config(bg='red')
            self.but_set_ipv4.config(state='disabled')

    def set_ipv4_addr(self):
        set_cmd = 'sudo ifconfig eth0:1 %s' % self.set_ipv4_str.get()
        subprocess.call(set_cmd.split(), timeout=2.0)

    def every_1s_job(self):
        if self.set_ipv4_str.get().encode('utf8') in get_ips_list():
            self.ip_status_str.set('Adresse IP OK')
        else:
            self.ip_status_str.set('Adresse IP non défini')

    def do_every(self, do_cmd, every_ms=1000):
        do_cmd()
        self.after(every_ms, lambda: self.do_every(do_cmd, every_ms=every_ms))


if __name__ == '__main__':
    app = tk.Tk()
    app.wm_title('IPv4 setup')
    app.attributes('-fullscreen', True)
    MainFrame(app).pack(side='top', fill='both', expand=True)
    app.mainloop()
