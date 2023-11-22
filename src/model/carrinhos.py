from datetime import datetime

class Carrinho:
    def __init__(self, 
                 id_carrinho:str=None, 
                 data_criacao:datetime=None
                ):
        self.set_id_carrinho(id_carrinho)
        self.set_data_criacao(data_criacao)

    def set_id_carrinho(self, id_carrinho:str):
        self.id_carrinho = id_carrinho

    def set_data_criacao(self, data_criacao:datetime):
        self.data_criacao = data_criacao

    def get_id_carrinho(self) -> datetime:
        return self.id_carrinho

    def get_data_criacao(self) -> str:
        return self.data_criacao

    def to_string(self) -> str:
        return f"id_carrinho: {self.get_id_carrinho()} | Data Criação: {self.get_data_criacao()}"