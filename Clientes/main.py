import tkinter as tk 
from tkinter import messagebox
import os
import json
import subprocess
import sys

cliente_file = "Clientes/Cadastrados/"
os.makedirs(cliente_file, exist_ok=True)

def exibir_conteudo(nome_cliente):
    janela_cliente = tk.Tk()
    janela_cliente.geometry("400x300")
    janela_cliente.title(nome_cliente)

    def exluir():
        #pergunta se quer mesmo excluir
        if messagebox.askokcancel("Excluir", "Deseja mesmo excluir o cliente?"):
            #exclui o arquivo
            os.remove(os.path.join(cliente_file, nome_cliente + ".json"))
            janela_cliente.destroy()
            atualizar_lista_clientes()
        else:
            janela_cliente.destroy()
            atualizar_lista_clientes()
    
    def editar():
        janela_editar = tk.Tk()
        janela_editar.geometry("400x300")
        janela_editar.title("Editar")

        def salvar_edicao():
            nome_cliente = nome_entry.get()
            credito_cliente = credito_entry.get()
            debito_cliente = debito_entry.get()
            cliente = {
                "nome": nome_cliente,
                "credito": credito_cliente,
                "debito": debito_cliente,
                "compras": "Nao comprou nada ainda"    
            }
            with open(os.path.join(cliente_file, nome_cliente + ".json"), "w") as f:
                json.dump(cliente, f)
            janela_editar.destroy()
            atualizar_lista_clientes()
            janela_editar.destroy()

        with open(os.path.join(cliente_file, nome_cliente + ".json"), "r") as f:
            cliente = json.load(f)
        label1 = tk.Label(janela_editar, text="Nome")
        label1.pack()
        nome_entry = tk.Entry(janela_editar)
        nome_entry.insert(0, cliente["nome"])
        nome_entry.pack()

        label2 = tk.Label(janela_editar, text="Credito")
        label2.pack()
        credito_entry = tk.Entry(janela_editar)
        credito_entry.insert(0, cliente["credito"])
        credito_entry.pack()

        label3 = tk.Label(janela_editar, text="Debito")
        label3.pack()
        debito_entry = tk.Entry(janela_editar)
        debito_entry.insert(0, cliente["debito"])
        debito_entry.pack()

        btn = tk.Button(janela_editar, text="Salvar", command=salvar_edicao)
        btn.pack()

        janela_editar.mainloop()
    with open(os.path.join(cliente_file, nome_cliente + ".json"), "r") as f:
        cliente = json.load(f)
    label_nome = tk.Label(janela_cliente, text="Nome: " + cliente["nome"])
    label_nome.pack()
    label_credito = tk.Label(janela_cliente, text="Credito: " + cliente["credito"])
    label_credito.pack()
    label_debito = tk.Label(janela_cliente, text="Debito: " + cliente["debito"])
    label_debito.pack()
    label_compras = tk.Label(janela_cliente, text="Compras: " + cliente["compras"])
    label_compras.pack()
    btn_exluir = tk.Button(janela_cliente, text="Excluir", command=exluir)
    btn_editar = tk.Button(janela_cliente, text="Editar", command=editar)
    btn_exluir.pack()
    btn_editar.pack()
    janela_cliente.mainloop()

def atualizar_lista_clientes():
    # Limpar os botões antigos
    for widget in painel.winfo_children():
        widget.destroy()

    # Repopular a lista de clientes
    clientes = os.listdir(cliente_file)
    if not clientes:
        labelvazio = tk.Label(painel, text="Não temos clientes cadastrados!")
        labelvazio.pack()
    else:
        for nome in clientes:
            nome_cliente, _ = os.path.splitext(nome)
            btn_cliente = tk.Button(painel, text=nome_cliente, height=2, width=50)
            btn_cliente.config(command=lambda nome=nome_cliente: exibir_conteudo(nome))
            btn_cliente.grid()

def novo_cliente():
    janela2 = tk.Tk()
    janela2.geometry("400x300")
    janela2.title("Novo cliente")

    id = 1
    if os.listdir(cliente_file):
        id = int(max([os.path.splitext(nome)[0] for nome in os.listdir(cliente_file)])) + 1
                    
    def salvar_cliente():
        nome_cliente = nome_entry.get()
        credito_cliente = credito_entry.get()
        debito_cliente = debito_entry.get()
        cliente = {
            "ID": id,
            "nome": nome_cliente,
            "credito": credito_cliente,
            "debito": debito_cliente,
            "compras": "Nao comprou nada ainda"    
        }
        #verifica se o nome do cliente ja existe
        if os.path.exists(os.path.join(cliente_file, str(id) + ".json")):
            messagebox.showerror("Erro", "Cliente já existe!")
            return
        with open(os.path.join(cliente_file, str(id) + ".json"), "w") as f:
            json.dump(cliente, f)

        janela2.destroy()
        atualizar_lista_clientes()

    label1 = tk.Label(janela2, text="Nome")
    label1.pack()
    nome_entry = tk.Entry(janela2)
    nome_entry.pack()

    label2 = tk.Label(janela2, text="Credito")
    label2.pack()
    credito_entry = tk.Entry(janela2)
    credito_entry.pack()

    label3 = tk.Label(janela2, text="Debito")
    label3.pack()
    debito_entry = tk.Entry(janela2)
    debito_entry.pack()

    btn = tk.Button(janela2, text="Salvar", command=salvar_cliente)
    btn.pack()

    janela2.mainloop()

def Voltar():
    #eu sou burro 
    janela.destroy()
    subprocess.Popen([sys.executable, "inicio.py"])
   

janela = tk.Tk()
janela.geometry("700x600")
janela.title("Clientes")

def perform_search():
    for widget in painel.winfo_children():
        widget.destroy()
    nome_cliente = entry.get()
    if nome_cliente:
        try:
            with open(os.path.join(cliente_file, nome_cliente + ".json"), "r") as f:
                cliente = json.load(f)
            btn_scres_cliente = tk.Button(painel, text=cliente["nome"], height=2, width=50,command=lambda: exibir_conteudo(nome_cliente))
            btn_scres_cliente.place(x=0, y=0)
        except FileNotFoundError:
            labelvazio = tk.Label(painel, text="Cliente não encontrado!")
            labelvazio.pack()
        except json.JSONDecodeError:
            labelvazio = tk.Label(painel, text="Erro ao ler o arquivo JSON do cliente!")
            labelvazio.pack()
    else:
        labelvazio = tk.Label(painel, text="Nome do cliente não especificado!")
        labelvazio.pack()

label1 = tk.Label(janela, text="Pesquisar")
entry = tk.Entry(janela)
btn = tk.Button(janela, text="Pesquisar", command=perform_search, height=1, width=10)
btn2 = tk.Button(janela,text="Novo",command=novo_cliente , height=1, width=10)

painel = tk.Frame(janela)
painel.place(x=0,y=50)
# Lista para armazenar os nomes dos clientes
buttons = []
for nome in os.listdir(cliente_file):
    if os.path.isfile(os.path.join(cliente_file, nome)):
        nome_sem_extensao, _ = os.path.splitext(nome)
        buttons.append(nome_sem_extensao)

# Verifica se a lista está vazia
if not buttons:
    labelvazio = tk.Label(painel, text="Não temos clientes cadastrados!")
    labelvazio.pack()
else:
    for nome in buttons:
        btn_cliente = tk.Button(painel, text=nome, height=2, width=50,command=lambda: exibir_conteudo(nome))
        btn_cliente.grid()

btn_atualizar = tk.Button(janela,text="atualizar",command=atualizar_lista_clientes, height=1, width=10)
btn_atualizar.place(x=400,y=10)

btn_voltar = tk.Button(janela,text="Voltar",command=Voltar, height=1, width=10)
btn_voltar.place(x=500,y=10)

label1.place(x=10, y=10)
entry.place(x=80, y=10)
btn.place(x=300, y=10)
btn2.place(x=200, y=10)

atualizar_lista_clientes()
janela.mainloop()
