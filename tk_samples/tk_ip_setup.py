#!/usr/bin/env python3
# IPv4 basic configuraion GUI tool
# 
# need external lib netifaces:
#   sudo apt install python3-netifaces

from netifaces import ifaddresses, gateways, AF_LINK, AF_INET
from ipaddress import IPv4Address, IPv4Interface
import subprocess
import tkinter as tk

# some consts
DEFAULT_IP = '10.0.0.100'
DEFAULT_MASK = '255.255.255.0'
DEFAULT_GW = '10.0.0.1'
ETH_IF = 'eth0'


# some class
class NumPad(tk.Frame):
    btn_map = [['7', '8', '9'],
               ['4', '5', '6'],
               ['1', '2', '3'],
               ['.', '0', '<']]

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # public
        self.parent = parent
        self.btn_key_d = {}
        # numpad create
        for row, line in enumerate(NumPad.btn_map):
            for column, key in enumerate(line):
                cmd = lambda k=key: self._on_key_press(k)
                self.btn_key_d[key] = tk.Button(self, text=key,
                                                font=('Verdana', 16),
                                                width=5, command=cmd)
                self.btn_key_d[key].grid(row=row, column=column)
        # default is disabled
        self.off()

    def on(self, *args):
        for key, btn in self.btn_key_d.items():
            btn.config(state='normal')

    def off(self, *args):
        for key, btn in self.btn_key_d.items():
            btn.config(state='disabled')

    def _on_key_press(self, key):
        # find focused widget on tk parent
        f_widget = self.parent.focus_get()
        # if it's an Entry widget update it
        if isinstance(f_widget, tk.Entry):
            c_pos = f_widget.index(tk.INSERT)
            if key == '<':
                f_widget.delete(c_pos - 1)
            else:
                f_widget.insert(c_pos, key)


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
        # Numpad frame
        self.npad_fr = NumPad(self)
        self.npad_fr.grid(row=3, columnspan=5, pady=20)
        # periodic job
        self.do_every(self.every_1s_job, every_ms=1000)
        # callback setup
        self.set_ipv4_str.trace('w', self.on_entry_update)
        self.set_mask_str.trace('w', self.on_entry_update)
        self.set_gw_str.trace('w', self.on_entry_update)
        # turn on numpad for every Entry widget focused
        for w in self.winfo_children():
            if isinstance(w, tk.Entry):
                w.bind('<FocusIn>', self.npad_fr.on)
                w.bind('<FocusOut>', self.npad_fr.off)

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
        except ValueError:
            self.ent_gw.config(bg='red')
            self.but_set_gw.config(state='disabled')

    def set_ipv4_addr(self):
        set_cmd = 'sudo ifconfig %s %s up' % (ETH_IF, self._ipv4_interface)
        print(set_cmd.split())
        subprocess.call(set_cmd.split(), timeout=2.0)

    def set_gw_addr(self):
        # remove all default gw
        rm_cmd = 'sudo ip route del 0/0'
        print((rm_cmd.split()))
        subprocess.call((rm_cmd.split()))
        # set new default gw
        set_cmd = 'sudo ip route add default via %s dev %s' % (self._gw_address, ETH_IF)
        print(set_cmd.split())
        subprocess.call(set_cmd.split())

    def every_1s_job(self):
        # get physical link  configuration
        try:
            if_addr_d = ifaddresses(ETH_IF)[AF_LINK][0]
            mac = if_addr_d['addr']
        except (ValueError, IndexError):
            mac = 'n/a'
        # get IPv4 configuration
        try:
            if_addr_d = ifaddresses(ETH_IF)[AF_INET][0]
            ip = if_addr_d['addr']
            mask = if_addr_d['netmask']
        except (ValueError, IndexError):
            ip = 'n/a'
            mask = 'n/a'
        # get default gateway data
        try:
            gw_d = gateways()
            gw = gw_d['default'][AF_INET][0]
        except (ValueError, IndexError):
            gw = 'n/a'
        # update ip_status label
        status_str = 'Configuration actuelle de l\'interface %s (%s)\nIPv4: %s\nMasque: %s\nPasserelle: %s'
        self.ip_status_str.set(status_str % (ETH_IF, mac, ip, mask, gw))

    def do_every(self, do_cmd, every_ms=1000):
        do_cmd()
        self.after(every_ms, lambda: self.do_every(do_cmd, every_ms=every_ms))


if __name__ == '__main__':
    app = tk.Tk()
    app.wm_title('IPv4 setup')
    app.attributes('-fullscreen', True)
    MainFrame(app).place(relx=0.5, rely=0.52, anchor=tk.CENTER)
    app.mainloop()
