import pandas as pd
from bson import ObjectId

from reports.relatorios import Relatorio

from model.itensCarrinho import ItensCarrinho
from model.produtos import Produto
from model.pedidos import Pedido

from controller.controller_produto import Controller_Produto
from controller.controller_pedido import Controller_Pedido

from conexion.mongo_queries import MongoQueries

class Controller_ItensCarrinho:
    def __init__(self):
        self.ctrl_produto = Controller_Produto()
        self.ctrl_pedido = Controller_Pedido()
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()
        
    def inserir_itensCarrinho(self) -> ItensCarrinho:
        # Cria uma nova conexão com o banco
        self.mongo.connect()
        
        # Lista os pedido existentes para inserir no item de pedido
        self.relatorio.get_relatorio_pedidos()
        id_carrinho = int(str(input("Digite o número do Pedido: ")))
        pedido = self.valida_pedido(id_carrinho)
        if pedido == None:
            return None

        # Lista os produtos existentes para inserir no item de pedido
        self.relatorio.get_relatorio_produtos()
        codigo_produto = int(str(input("Digite o código do Produto: ")))
        produto = self.valida_produto(codigo_produto)
        if produto == None:
            return None

        # Solicita a quantidade de itens do pedido para o produto selecionado
        quantidade = float(input(f"Informe a quantidade de itens do produto {produto.get_descricao()}: "))
        # Solicita o valor unitário do produto selecionado
        valor_unitario = float(input(f"Informe o valor unitário do produto {produto.get_descricao()}: "))

        proximo_itensCarrinho = self.mongo.db["itensCarrinho"].aggregate([
                                                    {
                                                        '$group': {
                                                            '_id': '$itensCarrinho', 
                                                            'proximo_itensCarrinho': {
                                                                '$max': '$codigo_itensCarrinho'
                                                            }
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'proximo_itensCarrinho': {
                                                                '$sum': [
                                                                    '$proximo_itensCarrinho', 1
                                                                ]
                                                            }, 
                                                            '_id': 0
                                                        }
                                                    }
                                                ])

        proximo_itensCarrinho = int(list(proximo_itensCarrinho)[0]['proximo_itensCarrinho'])
        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(codigo_itensCarrinho=proximo_itensCarrinho, valor_unitario=valor_unitario, quantidade=quantidade, id_carrinho=int(pedido.get_id_carrinho()), codigo_produto=int(produto.get_codigo()))
        # Insere e Recupera o código do novo item de pedido
        id_itensCarrinho = self.mongo.db["itensCarrinho"].insert_one(data)
        # Recupera os dados do novo item de pedido criado transformando em um DataFrame
        df_itensCarrinho = self.recupera_itensCarrinho(id_itensCarrinho.inserted_id)
        # Cria um novo objeto Item de Pedido
        novo_itensCarrinho = ItensCarrinho(df_itensCarrinho.codigo_itensCarrinho.values[0], df_itensCarrinho.quantidade.values[0], df_itensCarrinho.valor_unitario.values[0], pedido, produto)
        # Exibe os atributos do novo Item de Pedido
        print(novo_itensCarrinho.to_string())
        self.mongo.close()
        # Retorna o objeto novo_itensCarrinho para utilização posterior, caso necessário
        return novo_itensCarrinho

    def atualizar_itensCarrinho(self) -> ItensCarrinho:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do item de pedido a ser alterado
        codigo_itensCarrinho = int(input("Código do Item de Pedido que irá alterar: "))        

        # Verifica se o item de pedido existe na base de dados
        if not self.verifica_existencia_itensCarrinho(codigo_itensCarrinho):

            # Lista os pedido existentes para inserir no item de pedido
            self.relatorio.get_relatorio_pedidos()
            id_carrinho = int(str(input("Digite o número do Pedido: ")))
            pedido = self.valida_pedido(id_carrinho)
            if pedido == None:
                return None

            # Lista os produtos existentes para inserir no item de pedido
            self.relatorio.get_relatorio_produtos()
            codigo_produto = int(str(input("Digite o código do Produto: ")))
            produto = self.valida_produto(codigo_produto)
            if produto == None:
                return None

            # Solicita a quantidade de itens do pedido para o produto selecionado
            quantidade = float(input(f"Informe a quantidade de itens do produto {produto.get_descricao()}: "))
            # Solicita o valor unitário do produto selecionado
            valor_unitario = float(input(f"Informe o valor unitário do produto {produto.get_descricao()}: "))

            # Atualiza o item de pedido existente
            self.mongo.db["itensCarrinho"].update_one({"codigo_itensCarrinho": codigo_itensCarrinho},
                                                     {"$set": {"quantidade": quantidade,
                                                               "valor_unitario":  valor_unitario,
                                                               "id_carrinho": int(pedido.get_id_carrinho()),
                                                               "codigo_produto": int(produto.get_codigo())
                                                          }
                                                     })
            # Recupera os dados do novo item de pedido criado transformando em um DataFrame
            df_itensCarrinho = self.recupera_itensCarrinho_codigo(codigo_itensCarrinho)
            # Cria um novo objeto Item de Pedido
            itensCarrinho_atualizado = ItensCarrinho(df_itensCarrinho.codigo_itensCarrinho.values[0], df_itensCarrinho.quantidade.values[0], df_itensCarrinho.valor_unitario.values[0], pedido, produto)
            # Exibe os atributos do item de pedido
            print(itensCarrinho_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto pedido_atualizado para utilização posterior, caso necessário
            return itensCarrinho_atualizado
        else:
            self.mongo.close()
            print(f"O código {codigo_itensCarrinho} não existe.")
            return None

    def excluir_itensCarrinho(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do item de pedido a ser alterado
        codigo_itensCarrinho = int(input("Código do Item de Pedido que irá excluir: "))        

        # Verifica se o item de pedido existe na base de dados
        if not self.verifica_existencia_itensCarrinho(codigo_itensCarrinho):            
            # Recupera os dados do novo item de pedido criado transformando em um DataFrame
            df_itensCarrinho = self.recupera_itensCarrinho_codigo(codigo_itensCarrinho)
            pedido = self.valida_pedido(int(df_itensCarrinho.id_carrinho.values[0]))
            produto = self.valida_produto(int(df_itensCarrinho.codigo_produto.values[0]))
            
            opcao_excluir = input(f"Tem certeza que deseja excluir o item de pedido {codigo_itensCarrinho} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                # Revome o item de pedido da tabela
                self.mongo.db["itensCarrinho"].delete_one({"codigo_itensCarrinho": codigo_itensCarrinho})
                # Cria um novo objeto Item de Pedido para informar que foi removido
                itensCarrinho_excluido = ItensCarrinho(df_itensCarrinho.codigo_itensCarrinho.values[0], 
                                                  df_itensCarrinho.quantidade.values[0], 
                                                  df_itensCarrinho.valor_unitario.values[0], 
                                                  pedido, 
                                                  produto)
                self.mongo.close()
                # Exibe os atributos do produto excluído
                print("Item do Pedido Removido com Sucesso!")
                print(itensCarrinho_excluido.to_string())
        else:
            self.mongo.close()
            print(f"O código {codigo_itensCarrinho} não existe.")

    def verifica_existencia_itensCarrinho(self, codigo:int=None) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_pedido = self.recupera_itensCarrinho_codigo(codigo=codigo)
        return df_pedido.empty

    def recupera_itensCarrinho(self, _id:ObjectId=None) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_pedido = pd.DataFrame(list(self.mongo.db["itensCarrinho"].find({"_id": _id}, {"codigo_itensCarrinho":1, "quantidade": 1, "valor_unitario": 1, "id_carrinho": 1, "codigo_produto": 1, "_id": 0})))
        return df_pedido

    def recupera_itensCarrinho_codigo(self, codigo:int=None) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_pedido = pd.DataFrame(list(self.mongo.db["itensCarrinho"].find({"codigo_itensCarrinho": codigo}, {"codigo_itensCarrinho":1, 
                                                                                                          "quantidade": 1, 
                                                                                                          "valor_unitario": 1, 
                                                                                                          "id_carrinho": 1, 
                                                                                                          "codigo_produto": 1, 
                                                                                                          "_id": 0})))
        return df_pedido

    def valida_pedido(self, id_carrinho:int=None) -> Pedido:
        if self.ctrl_pedido.verifica_existencia_pedido(id_carrinho, external=True):
            print(f"O pedido {id_carrinho} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_pedido = self.ctrl_pedido.recupera_pedido_codigo(id_carrinho, external=True)
            cliente = self.ctrl_pedido.valida_cliente(df_pedido.cpf.values[0])
            fornecedor = self.ctrl_pedido.valida_fornecedor(df_pedido.cnpj.values[0])
            # Cria um novo objeto cliente
            pedido = Pedido(df_pedido.id_carrinho.values[0], df_pedido.data_criacao.values[0], cliente, fornecedor)
            return pedido

    def valida_produto(self, codigo_produto:int=None) -> Produto:
        if self.ctrl_produto.verifica_existencia_produto(codigo_produto, external=True):
            print(f"O produto {codigo_produto} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_produto = self.ctrl_produto.recupera_produto_codigo(codigo_produto, external=True)
            # Cria um novo objeto Produto
            produto = Produto(df_produto.codigo_produto.values[0], df_produto.descricao_produto.values[0])
            return produto