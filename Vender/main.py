import tkinter as tk
from tkinter import messagebox
import os
import json
import subprocess
import sys

janela = tk.Tk()
janela.geometry("700x500")
janela.title("Vendedor")

mesas_abertas = []

# Verifica se algum argumento foi passado

        

def adicionar_mesa():
    num_mesa = messa.get()
    if num_mesa == "":
        messagebox.showerror("Erro", "Digite o número da mesa")
        return
    file_mesa = "Clientes/Cadastrados/"+ num_mesa + ".json"
    if not os.path.exists(file_mesa):
        messagebox.showerror("Erro", "Mesa não encontrada")
        return
    #le o arquivo
    with open(file_mesa, "r") as f:
        cliente = json.load(f)
        if float(cliente["credito"]) == 0 and float(cliente["debito"]) == 0:
            #pergunta se quer abrir a mesa
            resposta = messagebox.askyesno("Mesa", "Cliente sem débito ou crédito, deseja abrir a mesa?")
            if resposta == False:
                return
        if num_mesa in mesas_abertas:
            messagebox.showerror("Erro", "Mesa já aberta")
            return
        else:
            mesas_abertas.append(num_mesa)
            exibir_mesas()      
    
def remover_mesa():
    mesa = messa.get()
    if mesa == "":
        messagebox.showerror("Erro", "Digite o número da mesa")
        return
    if mesa in mesas_abertas:
        resposta = messagebox.askyesno("Mesa", "Deseja fechar a mesa: "+mesa+" ?")
        if resposta == True:
            mesas_abertas.remove(mesa)
            exibir_mesas()
        else:
            return
    else:
        messagebox.showerror("Erro", "Mesa não encontrada")
        return

def exibir_mesas():
    for widget in painel.winfo_children():
        widget.destroy()

    for i, mesa in enumerate(mesas_abertas):
        btn_mesa = tk.Button(painel, text=f"Mesa: {mesa}", command=lambda m=mesa: fazer_pedido(m),height=3, width=40, bg="blue", fg="white")
        btn_mesa.grid(row=i, column=0, padx=10, pady=10)

def fazer_pedido(mesa):
    janela.destroy()
    subprocess.run(["python", "Vender/vender_produtos.py", mesa])  

def voltar():
    janela.destroy()
    subprocess.run(["python", "inicio.pyw"])

btn_voltar = tk.Button(janela, text="Voltar", command=voltar, height=2, width=10, bg="blue", fg="white")

btn_adicionar_mesa = tk.Button(janela, text="+ Mesa", bg="green", fg="white", command=adicionar_mesa)
messa = tk.Entry(janela, bg="white", fg="black")
btn_remover_mesa = tk.Button(janela, text="- Mesa", bg="red", fg="white", command=remover_mesa)

btn_voltar.place(x=600, y=10)
btn_adicionar_mesa.place(x=10, y=10)
btn_remover_mesa.place(x=300, y=10)
messa.place(x=80, y=10)


painel = tk.Frame(janela, width=700, height=500, bd=5)
painel.place(x=0, y=50)

def messa_carregadas():
    for widget in painel.winfo_children():
        widget.destroy()

    for i, mesa in enumerate(mesas_abertas):
        btn_mesa = tk.Button(painel, text=f"Mesa: {mesa}", command=lambda m=mesa: fazer_pedido(m),height=3, width=40, bg="blue", fg="white")
        btn_mesa.grid(row=i, column=0, padx=10, pady=10)

if len(sys.argv) > 1:
    mesa = sys.argv[1]
    if mesa != "":
        mesas_abertas.append(mesa)
        messa_carregadas()
        
janela.mainloop()
