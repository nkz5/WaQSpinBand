import tkinter as tk
import tkinter.ttk as ttk

class InputKLabelsModal(tk.Toplevel):
    def __init__(self, parent, kpoints_label_num):
        super().__init__(parent)
        self.title("KLabelsModal")
        self.geometry("500x500")
        self.transient(parent)
        self.grab_set()
        
        label1 = tk.Label(self, text="Input K lavel name")
        label1.pack(expand=True)

        self.input_list = []

        for i in range(int(kpoints_label_num)):
            input = tk.Entry(self)
            input.pack(expand=True)
            self.input_list.append(input)

        close_button = tk.Button(self, text="plot", command=lambda:self.plot_band())
        close_button.pack(expand=True)

        self.wait_window()
        
    def plot_band(self):
        self.kpoints_label_list = []
        for i in self.input_list:
            self.kpoints_label_list.append(i.get())
        
        print(self.kpoints_label_list)
        self.destroy()
