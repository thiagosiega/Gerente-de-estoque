import sys
import tkinter as tk
from tkinter import messagebox
import os
import json
import subprocess
import datetime


dia = datetime.datetime.now().strftime("%d-%m-%Y")

def mostrar_erro_e_sair(mensagem):
    # Cria uma janela raiz temporária somente para exibir a mensagem de erro
    temp_janela = tk.Tk()
    temp_janela.withdraw()  # Esconde a janela principal
    messagebox.showerror("Erro", mensagem)
    temp_janela.destroy()
    sys.exit()

# Verifica se algum argumento foi passado
if len(sys.argv) > 1:
    mesa = sys.argv[1]
    if mesa != "":
        janela = tk.Tk()
        janela.geometry("700x500")
        janela.title(f"Vendedor - Mesa {mesa}")
        carrinho = []

        def mostrar_carrinho():
            janela_carrinho = tk.Toplevel(janela)
            janela_carrinho.geometry("500x400")
            janela_carrinho.title(f"Carrinho - Mesa {mesa}")

            def finalizar_compra():
                if len(carrinho) == 0:
                    messagebox.showerror("Erro", "Carrinho vazio")
                else:
                    # Abre o .json e adiciona o carrinho
                    file_path = f"Clientes/Cadastrados/{mesa}.json"
                    with open(file_path, "r") as file:
                        data = json.load(file)
                    
                    data["compras"] = carrinho

                    with open(file_path, "w") as file:
                        json.dump(data, file, indent=4)

                    file_refisto = "Relatorios/vendas/"+dia+".json"
                    if os.path.exists(file_refisto):
                        #verifica se a messa existe no arquivo
                        with open(file_refisto, "r") as file:
                            data = json.load(file)
                            if mesa in data:
                                data[mesa] += carrinho
                            else:
                                data[mesa] = carrinho
                        with open(file_refisto, "w") as file:
                            json.dump(data, file, indent=4)
                    else:
                        with open(file_refisto, "w") as file:
                            data = {mesa: carrinho}
                            json.dump(data, file, indent=4)

                    janela_carrinho.destroy()
                    janela.destroy()
                    subprocess.run(["python", "Vender/main.py", mesa])


            # Função para atualizar a visualização do carrinho
            def atualizar_carrinho():
                for widget in painel_carrinho.winfo_children():
                    widget.destroy()
                mostrar_itens_carrinho()  # Chamada para reconstruir a visualização do carrinho

            # Função para remover item do carrinho e atualizar a visualização
            def remover_item_carrinho(produto):
                carrinho.remove(produto)
                atualizar_carrinho()  # Atualiza a visualização após remover um item

            # Função para mostrar os itens do carrinho
            def mostrar_itens_carrinho():
                if len(carrinho) == 0:
                    label = tk.Label(painel_carrinho, text="Carrinho vazio", font=("Arial", 20))
                    label.pack(pady=20)
                else:
                    produtos_unicos = list(set(carrinho))
                    for i, produto in enumerate(produtos_unicos):
                        qtd = carrinho.count(produto)
                        label = tk.Label(painel_carrinho, text=f"{produto} x{qtd}", font=("Arial", 20))
                        btn_cancelar = tk.Button(painel_carrinho, text="Cancelar", command=lambda p=produto: remover_item_carrinho(p), height=1, width=10, bg="red", fg="white")
                        label.grid(row=i, column=0, padx=10, pady=10)
                        btn_cancelar.grid(row=i, column=1, padx=10, pady=10)

                frame_botao_finalizar = tk.Frame(janela_carrinho)
                frame_botao_finalizar.pack(pady=20)  # Use o pack no novo Frame

                btn_finalizar = tk.Button(frame_botao_finalizar, text="Finalizar compra", command=finalizar_compra , height=2, width=20, bg="green", fg="white")
                btn_finalizar.pack() 

            painel_carrinho = tk.Frame(janela_carrinho)
            painel_carrinho.pack(pady=20)

            mostrar_itens_carrinho()  # Inicializa a visualização dos itens do carrinho

            janela_carrinho.mainloop()

        labels_quantidade = {}
        def remover_item_carrinho(produto):
            carrinho.remove(produto)
        def adicionar_produto_carrinho(produto):
            carrinho.append(produto)
        def pesquisar(produto):
            #limpa o painel
            for widget in painel.winfo_children():
                widget.destroy()
            #pega o texto da caixa de pesquisa
            pesquisa_texto = pesquisa.get()
            #verifica se o produto existe
            if os.path.exists(file_estoque + pesquisa_texto + ".txt"):
                #cria um botao para o produto
                btn_remover = tk.Button(painel, text="-", command=lambda p=produto: remover_carrinho(p), height=1, width=10, bg="red", fg="white")
                btn_produto = tk.Button(painel, text=produto, height=3, width=20, bg="blue", fg="white")
                btn_adicionar = tk.Button(painel, text="+", command=lambda p=produto: adicionar_produto(p), height=1, width=10, bg="green", fg="white")  

                # Adiciona os botões e label ao painel usando o método grid
                btn_remover.grid(row=i, column=0, padx=5, pady=5)
                btn_produto.grid(row=i, column=1, padx=5, pady=5)
                btn_adicionar.grid(row=i, column=2, padx=5, pady=5)
            else:
                #se nao existir, mostra uma mensagem
                label = tk.Label(painel, text="Produto não encontrado")
                label.place(x=10, y=50)

        
        file_estoque = "Estoque/estoque/"
        #le todos os arquivos do estoque e remove a extensão
        produtos = [f.split(".")[0] for f in os.listdir(file_estoque)]
        #cria um painel para exibir os produtos
        painel = tk.Frame(janela)
        painel.grid(row=1, column=0, padx=10, pady=10)
        #cria um botão para cada produto
        volume = list(set(carrinho))

        def atualizar_quantidade_produto():
            for produto, label in labels_quantidade.items():
                label.config(text=f"x{carrinho.count(produto)}")

        def adicionar_produto(produto):
            carrinho.append(produto)
            atualizar_quantidade_produto()

        def remover_carrinho(produto):
            try:
                carrinho.remove(produto)
                atualizar_quantidade_produto()
            except ValueError:
                pass 

        def atualizar_label():
            for widget in painel.winfo_children():
                widget.destroy()
            return
        

        for i, produto in enumerate(produtos):
            btn_remover = tk.Button(painel, text="-", command=lambda p=produto: remover_carrinho(p), height=1, width=10, bg="red", fg="white")
            btn_produto = tk.Button(painel, text=produto, height=3, width=20, bg="blue", fg="white")
            btn_adicionar = tk.Button(painel, text="+", command=lambda p=produto: adicionar_produto(p), height=1, width=10, bg="green", fg="white")
            
            # Adiciona os botões e label ao painel usando o método grid
            btn_remover.grid(row=i, column=0, padx=5, pady=5)
            btn_produto.grid(row=i, column=1, padx=5, pady=5)
            btn_adicionar.grid(row=i, column=2, padx=5, pady=5)
            
            # Cria e adiciona o label de quantidade ao painel
            label_quantidade = tk.Label(painel, text=f"x{carrinho.count(produto)}", font=("Arial", 10))
            labels_quantidade[produto] = label_quantidade
            label_quantidade.grid(row=i, column=3, padx=5, pady=5)  # Ajustado para a coluna 2



        pesquisa = tk.Entry(janela, width=40, font=("Arial", 20))
        pesquisa.grid(row=0, column=0)
        btn_pesquisar = tk.Button(janela, text="Pesquisar", command=lambda: pesquisar(pesquisa.get()),height=2, width=10, bg="blue", fg="white")
        btn_pesquisar.grid(row=0, column=1)
        
        # Cria um frame para o conteúdo principal
        frame_conteudo = tk.Frame(janela)
        frame_conteudo.grid(row=2, column=0, sticky="nsew")

        # Cria um frame separado para o botão "Carrinho" na parte inferior
        frame_carrinho = tk.Frame(janela)
        frame_carrinho.grid(row=3, column=0, sticky="ew")

        # Adiciona o botão "Carrinho" ao frame do carrinho
        btn_carrinho = tk.Button(frame_carrinho, text="Carrinho", command=mostrar_carrinho, height=2, width=10, bg="blue", fg="white")
        btn_carrinho.pack(pady=10)  # Centraliza o botão no frame


        janela.mainloop()
else:
    mostrar_erro_e_sair("Erro grave: Número da mesa não recebido\nArquivo chamado incorretamente\nErro na linha 1")
    subprocess.call(["python", "Vender/main.py"])
