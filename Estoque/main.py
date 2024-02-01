import tkinter as tk
import os
import subprocess
import sys

janela = tk.Tk()
janela.geometry("700x500")
janela.title("Gerente de estoque")

painel = tk.Frame(janela, width=700, height=500)
painel.pack()

def novo_produto():
    janela2 = tk.Tk()
    janela2.geometry("400x300")
    janela2.title("Novo produto")

    def salvar_produto():
        nome_produto = nome_entry.get()
        preco_produto = preco_entry.get()
        quantidade_produto = quantidade_entry.get()
        produto = {
            "nome": nome_produto,
            "preco": preco_produto,
            "quantidade": quantidade_produto
        }
        with open(os.path.join(file_estoque, nome_produto + ".txt"), "w") as f:
            f.write(str(produto))
        janela2.destroy()


    label1 = tk.Label(janela2, text="Nome")
    label1.pack()
    nome_entry = tk.Entry(janela2)
    nome_entry.pack()

    label2 = tk.Label(janela2, text="Preço")
    label2.pack()
    preco_entry = tk.Entry(janela2)
    preco_entry.pack()

    label3 = tk.Label(janela2, text="Quantidade")
    label3.pack()
    quantidade_entry = tk.Entry(janela2)
    quantidade_entry.pack()

    btn = tk.Button(janela2, text="Salvar", command=salvar_produto)
    btn.pack()

    janela2.mainloop()

def Voltar():
    janela.destroy()
    subprocess.Popen([sys.executable, "inicio.pyw"])
    
def Atualizar():
    #limpa o painel
    for widget in painel.winfo_children():
        widget.destroy()
    lista_produtos = os.listdir(file_estoque)
    if len(lista_produtos) == 0:
        lista_produtos = ["Nenhum produto cadastrado"]
    else:
        #le o arquivo de cada produto e adiciona na lista
        for i in range(len(lista_produtos)):
            #remove a extensao do arquivo
            lista_produtos[i] = lista_produtos[i].replace(".txt", "")
            #cria botoes para cada produto
            btn = tk.Button(painel, text=lista_produtos[i], height=2, width=50, command=lambda x=lista_produtos[i]: exibir_informacoes_produto(x))
            #separa os botoes com uma distancia de 50 pixels
            btn.place(x=10, y=50 + 30 * i)

def Pesquisar():
    #limpa o painel
    for widget in painel.winfo_children():
        widget.destroy()
    #pega o texto da caixa de pesquisa
    pesquisa_texto = pesquisa.get()
    #verifica se o produto existe
    if os.path.exists(file_estoque + pesquisa_texto + ".txt"):
        #cria um botao para o produto
        btn = tk.Button(painel, text=pesquisa_texto, height=2, width=50, command=lambda: exibir_informacoes_produto(pesquisa_texto))
        btn.place(x=10, y=50)
    else:
        #se nao existir, mostra uma mensagem
        label = tk.Label(painel, text="Produto não encontrado")
        label.place(x=10, y=50)

def exibir_informacoes_produto(nome_produto):
    # Crie uma nova janela para exibir as informações do produto
    janela2 = tk.Tk()
    janela2.geometry("400x300")
    janela2.title(nome_produto)

    # Abra o arquivo do produto
    with open(file_estoque + nome_produto + ".txt", "r") as f:
        produto = eval(f.read())

    # Crie labels para cada informação do produto
    label1 = tk.Label(janela2, text="Nome: " + produto["nome"])
    label1.pack()

    label2 = tk.Label(janela2, text="Preço: " + produto["preco"])
    label2.pack()

    label3 = tk.Label(janela2, text="Quantidade: " + produto["quantidade"])
    label3.pack()

    janela2.mainloop()

file_estoque = "Estoque/estoque/"
lista_produtos = os.listdir(file_estoque)
if len(lista_produtos) == 0:
    lista_produtos = ["Nenhum produto cadastrado"]
else:
    #le o arquivo de cada produto e adiciona na lista
    for i in range(len(lista_produtos)):
        #remove a extensao do arquivo
        lista_produtos[i] = lista_produtos[i].replace(".txt", "")
        #cria botoes para cada produto
        btn = tk.Button(painel, text=lista_produtos[i], height=2, width=50, command=lambda x=lista_produtos[i]: exibir_informacoes_produto(x))
        btn.place(x=10, y=50 + 30 * i)

pesquisa = tk.Entry(janela, width=50)
btn_pesquisa = tk.Button(janela, text="Pesquisar",height=1, command=Pesquisar)
btn_atualizar = tk.Button(janela, text="Atualizar",height=1, command=Atualizar)
btn_voltar = tk.Button(janela, text="Voltar",height=1, command=Voltar)
btn_novo = tk.Button(janela, text="Novo",height=1, command=novo_produto)

pesquisa.place(x=10, y=10)
btn_pesquisa.place(x=300, y=10)#ok
btn_atualizar.place(x=400, y=10)#ok
btn_voltar.place(x=500, y=10)#ok
btn_novo.place(x=600, y=10) #ok

janela.mainloop()
