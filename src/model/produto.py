class Produto:
    def __init__(self, 
                 codigo_produto:str=None,
                 nome:str=None,
                 valor:float=None
                 ):
        self.set_codigo_produto(codigo_produto)
        self.set_nome(nome)
        self.set_valor(valor)

    def set_codigo_produto(self, codigo_produto:str):
        self.codigo_produto = codigo_produto

    def set_nome(self, nome:str):
        self.nome = nome

    def set_valor(self, valor:float):
        self.valor = valor

    def get_codigo_produto(self) -> str:
        return self.codigo_produto

    def get_nome(self) -> str:
        return self.nome
    
    def get_valor(self) -> float:
        return self.valor

    def to_string(self) -> str:
        return f"codigo_produto: {self.get_codigo_produto()} | Nome: {self.get_nome()} | Valor: {self.get_valor()}"