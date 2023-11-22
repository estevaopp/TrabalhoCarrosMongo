from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_produto import Controller_Produto
from controller.controller_carrinho import Controller_Carrinho
from controller.controller_itensCarrinho import Controller_ItensCarrinho

tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_carrinho = Controller_Carrinho()
ctrl_produto = Controller_Produto()
ctrl_itensCarrinho = Controller_ItensCarrinho()

def reports(opcao_relatorio:int=0):

    if opcao_relatorio == 1:
        relatorio.get_relatorio_itensCarrinhos()
    elif opcao_relatorio == 2:
        relatorio.get_relatorio_carrinhos()
    elif opcao_relatorio == 3:
        relatorio.get_relatorio_produtos()

def inserir(opcao_inserir:int=0):

    if opcao_inserir == 1:                               
        novo_carrinho = ctrl_carrinho.inserir_carrinho()
    elif opcao_inserir == 2:
        novo_produto = ctrl_produto.inserir_produto()
    elif opcao_inserir == 3:
        novo_itensCarrinho = ctrl_itensCarrinho.inserir_itensCarrinho()

def atualizar(opcao_atualizar:int=0):

    if opcao_atualizar == 1:
        relatorio.get_relatorio_carrinhos()
        carrinho_atualizado = ctrl_carrinho.atualizar_carrinho()
    elif opcao_atualizar == 2:
        relatorio.get_relatorio_produtos()
        produto_atualizado = ctrl_produto.atualizar_produto()
    elif opcao_atualizar == 3:
        relatorio.get_relatorio_itensCarrinhos()
        itensCarrinho_atualizado = ctrl_itensCarrinho.atualizar_itensCarrinho()

def excluir(opcao_excluir:int=0):

    if opcao_excluir == 1:
        relatorio.get_relatorio_carrinhos()
        ctrl_carrinho.excluir_carrinho()
    elif opcao_excluir == 2:                
        relatorio.get_relatorio_produtos()
        ctrl_produto.excluir_produto()
    elif opcao_excluir == 3:                
        relatorio.get_relatorio_itensCarrinhos()
        ctrl_itensCarrinho.excluir_itensCarrinho()

def run():
    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção [1-5]: "))
        config.clear_console(1)
        
        if opcao == 1: # Relatórios
            
            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção [0-3]: "))
            config.clear_console(1)

            reports(opcao_relatorio)

            config.clear_console(1)

        elif opcao == 2: # Inserir Novos Registros
            
            print(config.MENU_ENTIDADES)
            opcao_inserir = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            inserir(opcao_inserir=opcao_inserir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 3: # Atualizar Registros

            print(config.MENU_ENTIDADES)
            opcao_atualizar = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            atualizar(opcao_atualizar=opcao_atualizar)

            config.clear_console()

        elif opcao == 4:

            print(config.MENU_ENTIDADES)
            opcao_excluir = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            excluir(opcao_excluir=opcao_excluir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 5:

            print(tela_inicial.get_updated_screen())
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        else:
            print("Opção incorreta.")
            exit(1)

if __name__ == "__main__":
    run()