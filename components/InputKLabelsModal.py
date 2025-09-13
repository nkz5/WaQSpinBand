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
        

    def convert_greek(self, input_char: str):
        """
        convert small letter to greek character. Only 4 letters in order.

        Parameters
        ------------------
        input_char : String
            character entered in each label input

        Returns
        ------------------
        character which small letter is converted to greek character
        """
        greek_char_map = {
            'g': 'Γ',
            'd': 'Δ',
            's': 'Σ',
            'l': 'Λ',
            'c2': r"$C_2$",
            'y2': r"$Y_2$"
        }

        converted_char = greek_char_map.get(input_char)
        return converted_char if (converted_char != None) else input_char

    def plot_band(self):
        self.kpoints_label_list = []
        for i in self.input_list:
            self.kpoints_label_list.append(self.convert_greek(i.get()))
        
        self.destroy()
