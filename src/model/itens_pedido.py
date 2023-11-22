from model.carrinhos import Carrinho
from model.produtos import Produto

class ItemCarrinho:
    def __init__(self, 
                 codigo_item:int=None,
                 quantidade:float=None,
                 valor_unitario:float=None,
                 carrinho:Carrinho=None,
                 produto:Produto=None
                 ):
        self.set_codigo_item(codigo_item)
        self.set_quantidade(quantidade)
        self.set_valor_unitario(valor_unitario)
        self.set_carrinho(carrinho)
        self.set_produto(produto)

    def set_codigo_item(self, codigo_item:int):
        self.codigo_item = codigo_item

    def set_quantidade(self, quantidade:float):
        self.quantidade = quantidade

    def set_valor_unitario(self, valor_unitario:float):
        self.valor_unitario = valor_unitario
    
    def set_carrinho(self, carrinho:Carrinho):
        self.carrinho = carrinho

    def set_produto(self, produto:Produto):
        self.produto = produto

    def get_codigo_item(self) -> int:
        return self.codigo_item

    def get_quantidade(self) -> float:
        return self.quantidade

    def get_valor_unitario(self) -> float:
        return self.valor_unitario
    
    def get_carrinho(self) -> Carrinho:
        return self.carrinho

    def get_produto(self) -> Produto:
        return self.produto

    def to_string(self):
        return f"Item: {self.get_codigo_item()} | Quant.: {self.get_quantidade()} | Vlr. Unit.: {self.get_valor_unitario()} | Prod.: {self.get_produto().get_descricao()} | Ped: {self.get_carrinho().get_codigo_carrinho()}"