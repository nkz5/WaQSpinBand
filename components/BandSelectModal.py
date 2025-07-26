import os

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as tkFileDialog

class ModalWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("ModalWindow1")
        self.geometry("500x500")
        self.transient(parent)
        self.grab_set()

        self.file_path = None

        label = tk.Label(self, text="Modal Test")
        label.pack(expand=True)

        file_button = tk.Button(self, text="File Select", command=self.select_band)
        file_button.pack(expand=True)

        file_label = tk.Label(self, text=self.file_path)
        file_label.pack(expand=True)

        kpoints_label_num_label = tk.Label(self, text="K points num")
        kpoints_label_num_label.pack(expand=True)

        self.kpoints_label_num_input = tk.Entry(self)
        self.kpoints_label_num_input.pack(expand=True)

        each_kpoints_num_label = tk.Label(self, text="Each K points num")
        each_kpoints_num_label.pack(expand=True)

        self.each_kpoints_num_input = tk.Entry(self)
        self.each_kpoints_num_input.pack(expand=True)

        next_button = tk.Button(self, text="next", command=lambda:self.next_window())
        next_button.pack(expand=True)

        self.wait_window()


    def select_band(self):
        fTyp = [("", "*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        self.file_path = tkFileDialog.askopenfilename(filetypes=fTyp, initialdir=iDir)


    def next_window(self):
        self.kpoints_label_num = int(self.kpoints_label_num_input.get())
        self.each_kpoints_num = int(self.each_kpoints_num_input.get())
        self.destroy()