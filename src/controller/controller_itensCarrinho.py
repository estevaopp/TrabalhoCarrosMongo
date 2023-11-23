import pandas as pd
from bson import ObjectId

from reports.relatorios import Relatorio

from model.itensCarrinho import ItensCarrinho
from model.produtos import Produto
from model.carrinhos import Carrinho

from controller.controller_produto import Controller_Produto
from controller.controller_carrinho import Controller_Carrinho

from conexion.mongo_queries import MongoQueries
from datetime import datetime

class Controller_ItensCarrinho:
    def __init__(self):
        self.ctrl_produto = Controller_Produto()
        self.ctrl_carrinho = Controller_Carrinho()
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()
        
    def inserir_itensCarrinho(self) -> ItensCarrinho:
        # Cria uma nova conexão com o banco
        self.mongo.connect()

        data_hoje = datetime.today().strftime("%m-%d-%Y")
        
        # Lista os carrinho existentes para inserir no item de carrinho
        self.relatorio.get_relatorio_carrinhos()
        id_carrinho = input("Digite o número do Carrinho: ")
        carrinho = self.valida_carrinho(id_carrinho)
        if carrinho == None:
            return None

        # Lista os produtos existentes para inserir no item de carrinho
        self.relatorio.get_relatorio_produtos()
        codigo_produto = int(str(input("Digite o código do Produto: ")))
        produto = self.valida_produto(codigo_produto)
        if produto == None:
            return None

        proximo_itensCarrinho = self.mongo.db["itensCarrinhos"].aggregate([
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

        proximo_itensCarrinho = int(input("Digite o id do item carrinho: "))
        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(codigo_itenscarrinho=proximo_itensCarrinho, data_itenscarrinho=data_hoje, id_carrinho=int(carrinho.get_id_carrinho()), codigo_produto=int(produto.get_codigo()))
        # Insere e Recupera o código do novo item de carrinho
        id_itensCarrinho = self.mongo.db["itensCarrinhos"].insert_one(data)
        # Recupera os dados do novo item de carrinho criado transformando em um DataFrame
        df_itensCarrinho = self.recupera_itensCarrinho(id_itensCarrinho.inserted_id)
        # Cria um novo objeto Item de Carrinho
        novo_itensCarrinho = ItensCarrinho(df_itensCarrinho.codigo_itenscarrinho.values[0], df_itensCarrinho.data_itenscarrinho.values[0], carrinho, produto)
        # Exibe os atributos do novo Item de Carrinho
        print(novo_itensCarrinho.to_string())
        self.mongo.close()
        # Retorna o objeto novo_itensCarrinho para utilização posterior, caso necessário
        return novo_itensCarrinho

    def atualizar_itensCarrinho(self) -> ItensCarrinho:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do item de carrinho a ser alterado
        codigo_itensCarrinho = int(input("Código do Item de Carrinho que irá alterar: "))        

        # Verifica se o item de carrinho existe na base de dados
        if not self.verifica_existencia_itensCarrinho(codigo_itensCarrinho):

            # Lista os carrinho existentes para inserir no item de carrinho
            self.relatorio.get_relatorio_carrinhos()
            id_carrinho = input("Digite o número do Carrinho: ")
            carrinho = self.valida_carrinho(id_carrinho)
            if carrinho == None:
                return None

            # Lista os produtos existentes para inserir no item de carrinho
            self.relatorio.get_relatorio_produtos()
            codigo_produto = int(str(input("Digite o código do Produto: ")))
            produto = self.valida_produto(codigo_produto)
            if produto == None:
                return None

            # Atualiza o item de carrinho existente
            self.mongo.db["itensCarrinhos"].update_one({"codigo_itenscarrinho": codigo_itensCarrinho},
                                                     {"$set": {
                                                               "id_carrinho": int(carrinho.get_id_carrinho()),
                                                               "codigo_produto": int(produto.get_codigo())
                                                          }
                                                     })
            # Recupera os dados do novo item de carrinho criado transformando em um DataFrame
            df_itensCarrinho = self.recupera_itensCarrinho_codigo(codigo_itensCarrinho)
            # Cria um novo objeto Item de Carrinho
            itensCarrinho_atualizado = ItensCarrinho(df_itensCarrinho.codigo_itenscarrinho.values[0], df_itensCarrinho.data_itenscarrinho.values[0],carrinho, produto)
            # Exibe os atributos do item de carrinho
            print(itensCarrinho_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto carrinho_atualizado para utilização posterior, caso necessário
            return itensCarrinho_atualizado
        else:
            self.mongo.close()
            print(f"O código {codigo_itensCarrinho} não existe.")
            return None

    def excluir_itensCarrinho(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do item de carrinho a ser alterado
        codigo_itensCarrinho = int(input("Código do Item de Carrinho que irá excluir: "))        

        # Verifica se o item de carrinho existe na base de dados
        if not self.verifica_existencia_itensCarrinho(codigo_itensCarrinho):            
            # Recupera os dados do novo item de carrinho criado transformando em um DataFrame
            df_itensCarrinho = self.recupera_itensCarrinho_codigo(codigo_itensCarrinho)
            carrinho = self.valida_carrinho(str(df_itensCarrinho.id_carrinho.values[0]))
            produto = self.valida_produto(int(df_itensCarrinho.codigo_produto.values[0]))
            
            opcao_excluir = input(f"Tem certeza que deseja excluir o item de carrinho {codigo_itensCarrinho} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                # Revome o item de carrinho da tabela
                self.mongo.db["itensCarrinhos"].delete_one({"codigo_itenscarrinho": codigo_itensCarrinho})
                # Cria um novo objeto Item de Carrinho para informar que foi removido
                itensCarrinho_excluido = ItensCarrinho(df_itensCarrinho.codigo_itenscarrinho.values[0], 
                                                       df_itensCarrinho.data_itenscarrinho.values[0],
                                                  carrinho, 
                                                  produto)
                self.mongo.close()
                # Exibe os atributos do produto excluído
                print("Item do Carrinho Removido com Sucesso!")
                print(itensCarrinho_excluido.to_string())
        else:
            self.mongo.close()
            print(f"O código {codigo_itensCarrinho} não existe.")

    def verifica_existencia_itensCarrinho(self, codigo:int=None) -> bool:
        # Recupera os dados do novo carrinho criado transformando em um DataFrame
        df_carrinho = self.recupera_itensCarrinho_codigo(codigo=codigo)
        return df_carrinho.empty

    def recupera_itensCarrinho(self, _id:ObjectId=None) -> bool:
        # Recupera os dados do novo carrinho criado transformando em um DataFrame
        df_carrinho = pd.DataFrame(list(self.mongo.db["itensCarrinhos"].find({"_id": _id}, {"codigo_itenscarrinho":1, "data_itenscarrinho":1, "id_carrinho": 1, "codigo_produto": 1, "_id": 0})))
        return df_carrinho

    def recupera_itensCarrinho_codigo(self, codigo:int=None) -> bool:
        # Recupera os dados do novo carrinho criado transformando em um DataFrame
        df_carrinho = pd.DataFrame(list(self.mongo.db["itensCarrinhos"].find({"codigo_itenscarrinho": codigo}, {"codigo_itenscarrinho":1,
                                                                                                          "data_itenscarrinho":1,
                                                                                                          "id_carrinho": 1, 
                                                                                                          "codigo_produto": 1, 
                                                                                                          "_id": 0})))
        return df_carrinho

    def valida_carrinho(self, id_carrinho:str=None) -> Carrinho:
        if self.ctrl_carrinho.verifica_existencia_carrinho(id_carrinho, external=True):
            print(f"O carrinho {id_carrinho} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo criado transformando em um DataFrame
            df_carrinho = self.ctrl_carrinho.recupera_carrinho_codigo(id_carrinho, external=True)
            carrinho = Carrinho(df_carrinho.id_carrinho.values[0], df_carrinho.data_criacao.values[0])
            return carrinho

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