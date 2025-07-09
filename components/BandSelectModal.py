import tkinter as tk

class ModalWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("ModalWindow")
        self.geometry("500x500")
        self.transient(parent)
        self.grab_set()

        label = tk.Label(self, text="Modal Test")
        label.pack(expand=True)

        close_button = tk.Button(self, text="close", command=self.destroy)
        close_button.pack(expand=True)

        self.wait_window()