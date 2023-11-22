from datetime import date
from model.clientes import Cliente
from model.fornecedores import Fornecedor

class Pedido:
    def __init__(self, 
                 id_carrinho:int=None,
                 data_criacao:date=None,
                 cliente:Cliente= None,
                 fornecedor:Fornecedor=None
                 ):
        self.set_id_carrinho(id_carrinho)
        self.set_data_criacao(data_criacao)
        self.set_cliente(cliente)
        self.set_fornecedor(fornecedor)


    def set_id_carrinho(self, id_carrinho:int):
        self.id_carrinho = id_carrinho

    def set_data_criacao(self, data_criacao:date):
        self.data_criacao = data_criacao

    def set_cliente(self, cliente:Cliente):
        self.cliente = cliente

    def set_fornecedor(self, fornecedor:Fornecedor):
        self.fornecedor = fornecedor

    def get_id_carrinho(self) -> int:
        return self.id_carrinho

    def get_data_criacao(self) -> date:
        return self.data_criacao

    def get_cliente(self) -> Cliente:
        return self.cliente

    def get_fornecedor(self) -> Fornecedor:
        return self.fornecedor

    def to_string(self) -> str:
        return f"Pedido: {self.get_id_carrinho()} | Data: {self.get_data_criacao()} | Cliente: {self.get_cliente().get_nome()} | Fornecedor: {self.get_fornecedor().get_nome_fantasia()}"