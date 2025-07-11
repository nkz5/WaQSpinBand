import sys
import os
import numpy as np
import tkinter as tk

import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinter import messagebox as tkMessageBox
from tkinter import filedialog as tkFileDialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

import services.graph as graph
import services.data as data

import components.BandSelectModal as BandSelectModal
import components.InputKLabelsModal as InputKLabelsModal


class Application(tk.Frame):
    DEBUG_LOG = True

    pw_main = None
    pw_band = None

    bands_df = None
    k_points_df = None
    bands_spin_df = None

    file_path = None
    kpoints_label_num = None
    each_kpoints_num = None
    kpoints_label_list = None
    # k_points_root = None
    k_range = None
    ylim = None

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.create_widgets()
        
    def create_widgets(self):
        """
        Create main widget, left tab widget and right band plot widget
        """
        
        self.pw_main = tk.PanedWindow(self.master, orient='horizontal')
        self.pw_main.pack(expand=True, fill = tk.BOTH, side="left")
        
        pw_tab = tk.PanedWindow(self.pw_main, bg="yellow", orient='vertical')
        self.pw_main.add(pw_tab)

        self.pw_band = tk.PanedWindow(self.pw_main, bg="cyan", orient='vertical', width=700)
        self.pw_main.add(self.pw_band)

        btn_tool_1 = tk.Button(pw_tab, text="Plot", command=lambda:self.open_modal(), height = 2, width = 10)
        btn_tool_1.pack()

        btn_tool_2 = tk.Button(pw_tab, text="Spin", command=lambda:self.select_spin(), height = 2, width = 10)
        btn_tool_2.pack()


    def open_modal(self):
        modal = BandSelectModal.ModalWindow(parent=self.master)
        print("result", modal.kpoints_label_num)
        self.file_path = modal.file_path
        self.kpoints_label_num = modal.kpoints_label_num
        self.each_kpoints_num = modal.each_kpoints_num


        modal2 = InputKLabelsModal.InputKLabelsModal(parent=self.master, kpoints_label_num = modal.kpoints_label_num)
        self.kpoints_label_list = modal2.kpoints_label_list

        self.bands_df, self.k_points_df = data.bands(self.file_path)

        self.plot_band(spin_flg=False)


    def select_spin(self):
        fTyp = [("", "*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        file_path = tkFileDialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        self.bands_spin_df, k_points_df = data.bands(file_path)

        self.plot_band(spin_flg=True)

    def plot_band(self, spin_flg:bool):
        self.pw_main.remove(self.pw_band)
        self.pw_band = tk.PanedWindow(self.pw_main, bg="cyan", orient='vertical', width=700)
        self.pw_main.add(self.pw_band)

        fig1 = graph.bands(bands_df=self.bands_df, k_points_positions=range(len(self.k_points_df)), k_points_each=self.each_kpoints_num, k_points_root=self.kpoints_label_list, Fermi=0, ylim=self.ylim, console=True, k_range=self.k_range, size=[5,5], spin=spin_flg, bands_spin_df=self.bands_spin_df)
        
        canvas = FigureCanvasTkAgg(fig1,master = self.pw_band)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, self.pw_band)
        toolbar.update()
        canvas.get_tk_widget().pack()
    

root = tk.Tk()
myapp = Application(master=root)
myapp.master.title("My Application")
myapp.master.geometry("1000x800")

myapp.mainloop()