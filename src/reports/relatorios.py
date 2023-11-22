from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        pass

    
    
    def get_relatorio_produtos(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["produtos"].find({}, 
                                                 {"codigo_produto": 1, 
                                                  "descricao_produto": 1, 
                                                  "_id": 0
                                                 }).sort("descricao_produto", ASCENDING)
        df_produto = pd.DataFrame(list(query_result))
        # Fecha a conexão com o Mongo
        mongo.close()
        # Exibe o resultado
        print(df_produto)        
        input("Pressione Enter para Sair do Relatório de Produtos")


    def get_relatorio_carrinhos(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["carrinhos"].find({}, 
                                                 {"id_carrinho": 1, 
                                                  "data_criacao": 1, 
                                                  "_id": 0
                                                 }).sort("id_carrinho", ASCENDING)
        
        df_carrinho = pd.DataFrame(list(query_result))
        # Fecha a conexão com o Mongo
        mongo.close()
        print(df_carrinho[["id_carrinho", "data_criacao", "cliente", "empresa", "itensCarrinho", "produto", "valor_total"]])
        input("Pressione Enter para Sair do Relatório de Carrinhos")
    
    def get_relatorio_itensCarrinhos(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Realiza uma consulta no mongo e retorna o cursor resultante para a variável
        query_result = mongo.db['itensCarrinho'].aggregate([{
                                                            '$lookup':{'from':'produtos',
                                                                       'localField':'codigo_produto',
                                                                       'foreignField':'codigo_produto',
                                                                       'as':'produto'
                                                                      }
                                                           },
                                                           {
                                                            '$unwind':{"path": "$produto"}
                                                           },
                                                           {'$project':{'id_carrinho':1, 
                                                                        'codigo_itensCarrinho':1,
                                                                    'codigo_produto':'$produto.codigo_produto',
                                                                    'descricao_produto':'$produto.descricao_produto',
                                                                    '_id':0
                                                                    }}
                                                          ])
        # Converte o cursos em lista e em DataFrame
        df_itensCarrinho = pd.DataFrame(list(query_result))
        # Troca o tipo das colunas
        df_itensCarrinho.codigo_itensCarrinho = df_itensCarrinho.codigo_itensCarrinho.astype(int)
        df_itensCarrinho.id_carrinho = df_itensCarrinho.id_carrinho.astype(int)
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_itensCarrinho[["id_carrinho", "codigo_itensCarrinho", "codigo_produto", "descricao_produto", "valor_total"]])
        input("Pressione Enter para Sair do Relatório de Itens de Carrinhos")