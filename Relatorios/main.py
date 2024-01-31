import tkinter as tk
from tkinter import Button
import os
import json

def main():
    root = tk.Tk()
    root.title("Relatórios")
    root.geometry("300x200")

    def relatorio(venda):
        janela2 = tk.Toplevel(root)
        janela2.geometry("500x400")
        janela2.title("Relatório do dia: " + venda)
        file = "Relatorios/vendas/" + venda + ".json"

        with open(file, "r") as f:
            data = json.load(f)
            text = tk.Text(janela2)
            
            # Iterar sobre cada chave e valor em "vendas"
            for key, items in data.items():
                text.insert(tk.END, f"Chapa {key}:\n")
                for item in items:
                    text.insert(tk.END, f"  - {item}\n")
                text.insert(tk.END, "\n")  # Adiciona uma linha extra entre as quantidades
            
            text.pack()

        janela2.mainloop()
    
    file = "Relatorios/vendas/"
    vendas = [f.replace(".json", "") for f in os.listdir(file) if f.endswith(".json")]
    
    for venda in vendas:
        btn = Button(root, text=venda, command=lambda v=venda: relatorio(v))
        btn.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
