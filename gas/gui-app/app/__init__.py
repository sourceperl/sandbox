import tkinter as tk
from tkinter import ttk

from .tab_sgerg import TabSGERG


class App(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title('My App')
        # build a notebook with tabs
        self.note = ttk.Notebook(self)
        self.tab_sgerg = TabSGERG(self)
        self.tab_aga8 = ttk.Frame(self)
        self.note.add(self.tab_sgerg, text='SGERG (F1)')
        self.note.add(self.tab_aga8, text='AGA8 (F2)')
        self.note.pack(fill=tk.BOTH, expand=True)
        # defaut selected tab
        self.note.select(self.tab_sgerg)
        # bind function keys to tabs
        self.bind('<F1>', lambda evt: self.note.select(self.tab_sgerg))
        self.bind('<F2>', lambda evt: self.note.select(self.tab_aga8))



def main():
    app = App()
    app.mainloop()
