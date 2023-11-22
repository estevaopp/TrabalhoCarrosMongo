from datetime import datetime
from model.carrinho import Carrinho
from model.produto import Produto

class ItensCarrinho:
    def __init__(self, 
                 codigo_itensCarrinho:int=None,
                 data_itensCarrinho:datetime=None,
                 carrinho:Carrinho= None,
                 produto:Produto=None
                 ):
        self.set_codigo_itensCarrinho(codigo_itensCarrinho)
        self.set_data_itensCarrinho(data_itensCarrinho)
        self.set_carrinho(carrinho)
        self.set_produto(produto)


    def set_codigo_itensCarrinho(self, codigo_itensCarrinho:int):
        self.codigo_itensCarrinho = codigo_itensCarrinho

    def set_data_itensCarrinho(self, data_itensCarrinho:datetime):
        self.data_itensCarrinho = data_itensCarrinho

    def set_carrinho(self, carrinho:Carrinho):
        self.carrinho = carrinho

    def set_produto(self, produto:Produto):
        self.produto = produto

    def get_codigo_itensCarrinho(self) -> int:
        return self.codigo_itensCarrinho

    def get_data_itensCarrinho(self) -> datetime:
        return self.data_itensCarrinho

    def get_carrinho(self) -> Carrinho:
        return self.carrinho

    def get_produto(self) -> Produto:
        return self.produto

    def to_string(self) -> str:
        return f"Agendameto: {self.get_codigo_itensCarrinho()} | Data: {self.get_data_itensCarrinho()} | Carrinho: {self.get_carrinho().get_id_carrinho()} | Produto: {self.get_produto().get_nome()}"