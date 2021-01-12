#!/usr/bin/env python3

from netifaces import ifaddresses, gateways, AF_INET
from ipaddress import IPv4Address, IPv4Interface
import socket
import struct
import subprocess
import tkinter as tk


# some consts
DEFAULT_IP = '10.0.0.100'
DEFAULT_MASK = '255.255.255.0'
DEFAULT_GW = '10.0.0.1'


# some class
class MainFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # public
        self.parent = parent
        # private
        self._ipv4_interface = IPv4Interface('%s/%s' % (DEFAULT_IP, DEFAULT_MASK))
        self._gw_address = IPv4Address(DEFAULT_GW)
        # tk strings vars
        self.set_ipv4_str = tk.StringVar(value=DEFAULT_IP)
        self.set_mask_str = tk.StringVar(value=DEFAULT_MASK)
        self.set_gw_str = tk.StringVar(value=DEFAULT_GW)
        self.ip_status_str = tk.StringVar(value='')
        # widgets setup
        # IPv4
        tk.Label(self, font=('Verdana', 16), text='@IPv4/masque').grid(row=0, column=0, padx=10)
        self.ent_ipv4 = tk.Entry(self, width='16', justify=tk.CENTER,
                                 font=('Verdana', 16), textvariable=self.set_ipv4_str)
        self.ent_ipv4.grid(row=0, column=1)
        # Mask
        tk.Label(self, font=('Verdana', 16), text='/').grid(row=0, column=2)
        self.ent_mask = tk.Entry(self, width='16', justify=tk.CENTER,
                                 font=('Verdana', 16), textvariable=self.set_mask_str)
        self.ent_mask.grid(row=0, column=3)
        # Valid button
        self.but_set_ipv4 = tk.Button(self, text='Set',
                                      font=('Verdana', 16), command=self.set_ipv4_addr)
        self.but_set_ipv4.grid(row=0, column=4, padx=10, pady=5, ipadx=10, ipady=10)
        # Gateway
        tk.Label(self, font=('Verdana', 16), text='Passerelle').grid(row=1, column=0, padx=10)
        self.ent_gw = tk.Entry(self, width='16', justify=tk.CENTER,
                               font=('Verdana', 16), textvariable=self.set_gw_str)
        self.ent_gw.grid(row=1, column=1, pady=20)
        # Valid button
        self.but_set_gw = tk.Button(self, text='Set',
                                    font=('Verdana', 16), command=self.set_gw_addr)
        self.but_set_gw.grid(row=1, column=4, padx=10, pady=5, ipadx=10, ipady=10)
        # Status label
        self.lab_status = tk.Label(self, justify=tk.CENTER, font=('Verdana', 16),
                                   textvariable=self.ip_status_str, bg='white')
        self.lab_status.grid(row=2, columnspan=5, pady=20, sticky='EW')
        # periodic job
        self.do_every(self.every_1s_job, every_ms=1000)
        # install callback
        self.set_ipv4_str.trace('w', self.on_entry_update)
        self.set_mask_str.trace('w', self.on_entry_update)
        self.set_gw_str.trace('w', self.on_entry_update)

    def on_entry_update(self, *args):
        # IP/mask update
        try:
            self._ipv4_interface = IPv4Interface('%s/%s' % (self.set_ipv4_str.get(), self.set_mask_str.get()))
            self.ent_ipv4.config(bg='white')
            self.ent_mask.config(bg='white')
            self.but_set_ipv4.config(state='normal')
        except ValueError:
            self.ent_ipv4.config(bg='red')
            self.ent_mask.config(bg='red')
            self.but_set_ipv4.config(state='disabled')
        # Gateway update
        try:
            self._gw_address = IPv4Address(self.set_gw_str.get())
            if self._gw_address not in self._ipv4_interface.network:
                raise ValueError
            self.ent_gw.config(bg='white')
            self.but_set_gw.config(state='normal')
        except:
            self.ent_gw.config(bg='red')
            self.but_set_gw.config(state='disabled')

    def set_ipv4_addr(self):
        set_cmd = 'sudo ifconfig eth0 %s up' % self._ipv4_interface
        print(set_cmd.split())
        subprocess.call(set_cmd.split(), timeout=2.0)

    def set_gw_addr(self):
        # remove all default gw
        rm_cmd = 'sudo ip route del 0/0'
        print((rm_cmd.split()))
        subprocess.call((rm_cmd.split()))
        # set new default gw
        set_cmd = 'sudo ip route add default via %s dev eth0' % self._gw_address
        print(set_cmd.split())
        subprocess.call(set_cmd.split())

    def every_1s_job(self):
        # get IPv4 configuration
        try:
            eth0_d = ifaddresses('eth0')[AF_INET][0]
            ip = eth0_d['addr']
            mask = eth0_d['netmask']
        except:
            ip = 'n/a'
            mask = 'n/a'
        # get default gateway data
        try:
            gw_d = gateways()
            gw = gw_d['default'][AF_INET][0]
        except:
            gw = 'n/a'
        # update ip_status label
        status_str = 'Configuration actuelle\nIPv4: %s\nMasque: %s\nPasserelle: %s'
        self.ip_status_str.set(status_str % (ip, mask, gw))

    def do_every(self, do_cmd, every_ms=1000):
        do_cmd()
        self.after(every_ms, lambda: self.do_every(do_cmd, every_ms=every_ms))


if __name__ == '__main__':
    app = tk.Tk()
    app.wm_title('IPv4 setup')
    app.attributes('-fullscreen', True)
    MainFrame(app).place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    app.mainloop()
