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


# アプリケーション（GUI）クラス
class Application(tk.Frame):
    DEBUG_LOG = True

    pw_main = None
    pw_band = None

    bands_df = None
    k_points_df = None
    bands_spin_df = None

    k_points_root = None
    k_range = None
    ylim = None

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.create_widgets()
        
    def create_widgets(self):
        # ペインウィンドウ
        # PanedWindow
        ##  orient : 配置（vertical or horizontal）
        ##  bg : 枠線の色
        # pack
        ##  expand ：可変（True or False(固定)
        ##  fill : スペースが空いている場合の動き（tk.BOTH　縦横に広がる）
        ##  side ：　配置する際にどの方向からつめていくか（side or top ・・・）
        self.pw_main = tk.PanedWindow(self.master, orient='horizontal')
        self.pw_main.pack(expand=True, fill = tk.BOTH, side="left")
        
        pw_tab = tk.PanedWindow(self.pw_main, bg="yellow", orient='vertical')
        self.pw_main.add(pw_tab)

        self.pw_band = tk.PanedWindow(self.pw_main, bg="cyan", orient='vertical', width=700)
        self.pw_main.add(self.pw_band)

        # plot_button = tk.Button(master = pw_tab,height = 2, width = 10, text = "Plot")
        # plot_button.pack()

        btn_tool_1 = tk.Button(pw_tab, text="Plot", command=lambda:self.select_band(), height = 2, width = 10)
        # btn_tool_1.grid(row=3, column=0, sticky=tk.W + tk.E, padx=2, pady=10)
        btn_tool_1.pack()

        btn_tool_2 = tk.Button(pw_tab, text="Spin", command=lambda:self.select_spin(), height = 2, width = 10)
        btn_tool_2.pack()

        btn_tool_3 = tk.Button(pw_tab, text="Modal", command=lambda:self.open_modal(), height = 2, width = 10)
        btn_tool_3.pack()

    def open_modal(self):
        BandSelectModal.ModalWindow(self.pw_main)

    def select_band(self):
        fTyp = [("", "*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        file_path = tkFileDialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        self.bands_df, self.k_points_df = data.bands(file_path)

        self.k_points_root = [r"$\Gamma$", "X", "S", "Y", r"$\Gamma$", "Z", "U", "R", "T", "Z"]
        self.k_range = [0, 10]
        self.ylim = [-2, 7]

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

        fig1 = graph.bands(bands_df=self.bands_df, k_points_positions=range(len(self.k_points_df)), k_points_each=10, k_points_root=self.k_points_root, Fermi=0, ylim=self.ylim, console=True, k_range=self.k_range, size=[5,5], spin=spin_flg, bands_spin_df=self.bands_spin_df)
        
        canvas = FigureCanvasTkAgg(fig1,master = self.pw_band)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, self.pw_band)
        toolbar.update()
        canvas.get_tk_widget().pack()
    

# 実行
root = tk.Tk()
myapp = Application(master=root)
myapp.master.title("My Application") # タイトル
myapp.master.geometry("1000x800") # ウィンドウの幅と高さピクセル単位で指定（width x height）

myapp.mainloop()