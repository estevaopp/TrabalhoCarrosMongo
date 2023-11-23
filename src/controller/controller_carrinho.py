import pandas as pd
from bson import ObjectId

from reports.relatorios import Relatorio

from model.carrinhos import Carrinho

from conexion.mongo_queries import MongoQueries
from datetime import datetime

class Controller_Carrinho:
    def __init__(self):
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()
        
    def inserir_carrinho(self) -> Carrinho:
        # Cria uma nova conexão com o banco
        self.mongo.connect()

        data_hoje = datetime.today().strftime("%m-%d-%Y")

        proximo_carrinho = input("Selecione o Id do carrinho:  ")
        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(id_carrinho=proximo_carrinho, data_criacao=data_hoje)
        # Insere e Recupera o código do novo carrinho
        id_carrinho = self.mongo.db["carrinhos"].insert_one(data)
        # Recupera os dados do novo produto criado transformando em um DataFrame
        df_carrinho = self.recupera_carrinho(id_carrinho.inserted_id)
        # Cria um novo objeto Produto
        novo_carrinho = Carrinho(df_carrinho.id_carrinho.values[0], df_carrinho.data_criacao.values[0])
        # Exibe os atributos do novo produto
        print(novo_carrinho.to_string())
        self.mongo.close()
        # Retorna o objeto novo_carrinho para utilização posterior, caso necessário
        return novo_carrinho

    def atualizar_carrinho(self) -> Carrinho:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do produto a ser alterado
        id_carrinho = input("Código do Carrinho que irá alterar: ")       

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_carrinho(id_carrinho):

            data_hoje = datetime.today().strftime("%m-%d-%Y")

            # Atualiza a descrição do produto existente
            self.mongo.db["carrinhos"].update_one({"id_carrinho": id_carrinho}, 
                                                {"$set": {
                                                          "data_criacao": data_hoje
                                                          }
                                                })
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_carrinho = self.recupera_carrinho_codigo(id_carrinho)
            # Cria um novo objeto Produto
            carrinho_atualizado = Carrinho(df_carrinho.id_carrinho.values[0], df_carrinho.data_criacao.values[0])
            # Exibe os atributos do novo produto
            print(carrinho_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto carrinho_atualizado para utilização posterior, caso necessário
            return carrinho_atualizado
        else:
            self.mongo.close()
            print(f"O código {id_carrinho} não existe.")
            return None

    def excluir_carrinho(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do produto a ser alterado
        id_carrinho = input("Código do Carrinho que irá excluir: ")        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_carrinho(id_carrinho):            
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_carrinho = self.recupera_carrinho_codigo(id_carrinho)
            
            opcao_excluir = input(f"Tem certeza que deseja excluir o carrinho {id_carrinho} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                print("Atenção, caso o carrinho possua itens, também serão excluídos!")
                opcao_excluir = input(f"Tem certeza que deseja excluir o carrinho {id_carrinho} [S ou N]: ")
                if opcao_excluir.lower() == "s":
                    # Revome o produto da tabela
                    self.mongo.db["itensCarrinhos"].delete_one({"id_carrinho": id_carrinho})
                    print("Itens do carrinho removidos com sucesso!")
                    self.mongo.db["carrinhos"].delete_one({"id_carrinho": id_carrinho})
                    # Cria um novo objeto Produto para informar que foi removido
                    carrinho_excluido = Carrinho(df_carrinho.id_carrinho.values[0], df_carrinho.data_criacao.values[0])
                    self.mongo.close()
                    # Exibe os atributos do produto excluído
                    print("Carrinho Removido com Sucesso!")
                    print(carrinho_excluido.to_string())
        else:
            self.mongo.close()
            print(f"O código {id_carrinho} não existe.")

    def verifica_existencia_carrinho(self, codigo:str=None, external: bool = False) -> bool:
        # Recupera os dados do novo carrinho criado transformando em um DataFrame
        df_carrinho = self.recupera_carrinho_codigo(codigo=codigo, external=external)
        return df_carrinho.empty

    def recupera_carrinho(self, _id:ObjectId=None) -> bool:
        # Recupera os dados do novo carrinho criado transformando em um DataFrame
        df_carrinho = pd.DataFrame(list(self.mongo.db["carrinhos"].find({"_id":_id}, {"id_carrinho": 1, "data_criacao": 1, "_id": 0})))
        return df_carrinho

    def recupera_carrinho_codigo(self, codigo:str=None, external: bool = False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo carrinho criado transformando em um DataFrame
        df_carrinho = pd.DataFrame(list(self.mongo.db["carrinhos"].find({"id_carrinho": codigo}, {"id_carrinho": 1, "data_criacao": 1, "_id": 0})))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_carrinho
