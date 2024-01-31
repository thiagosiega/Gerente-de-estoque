import tkinter as tk
import os
import subprocess
import sys

janela = tk.Tk()

janela.geometry("600x300")
janela.title("Gerente de estoque")

texbtn = [
    "Estoque",
    "Clientes",
    "Vender",
    "Relatorios"
]
def btn_click(x):
     # Verifica se o diretório existe
    if not os.path.exists(x):
        print("Erro: conteúdo não encontrado!")
    else:
        script_path = os.path.join(x, "main.py")        
        if os.path.isfile(script_path):
            janela.destroy()
            subprocess.Popen([sys.executable, script_path])
        else:
            print("Erro: arquivo não encontrado!")
            

bottom_frame = tk.Frame(janela)
bottom_frame.pack(side='bottom', fill='x', pady=5)

for i in texbtn:
    btn = tk.Button(bottom_frame, text=i, command=lambda x=i: btn_click(x))
    btn.pack(side='left', padx=5, pady=5)

janela.mainloop()
