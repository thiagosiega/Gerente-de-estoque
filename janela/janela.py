import tkinter as tk

#file: janela/janela.py
class Janela ():
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Hello World")
        self.janela.geometry("300x300")
        self.janela.mainloop()