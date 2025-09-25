import datetime
import os

class ManutencaoItem:
    def __init__(self, nome, valor, data_troca, km_troca, km_proxima, meses_proxima):
        self.nome = nome
        self.valor = valor
        self.data_troca = data_troca
        self.km_troca = km_troca
        self.km_proxima = km_proxima
        self.meses_proxima = meses_proxima

    def __str__(self):
        proxima_troca_km = self.km_troca + self.km_proxima
        proxima_data_troca = self.data_troca + datetime.timedelta(days=self.meses_proxima * 30)
        return (
            f"--- {self.nome} ---\n"
            f"Valor: R$ {self.valor:.2f}\n"
            f"Data da troca: {self.data_troca.strftime('%d/%m/%Y')}\n"
            f"KM da troca: {self.km_troca} km\n"
            f"Próxima troca recomendada: {proxima_troca_km} km ou {proxima_data_troca.strftime('%d/%m/%Y')}\n"
        )

class GerenciadorManutencao:
    def __init__(self):
        self.itens = []
        self.diretorio_relatorios = "relatorios_manutencao"
        if not os.path.exists(self.diretorio_relatorios):
            os.makedirs(self.diretorio_relatorios)

    def adicionar_item(self):
        try:
            nome = input("Digite o nome da peça/item: ")
            valor = float(input("Digite o valor da peça/item (Ex: 50.00): "))
            data_troca_str = input("Digite a data da troca (DD/MM/AAAA): ")
            data_troca = datetime.datetime.strptime(data_troca_str, '%d/%m/%Y').date()
            km_troca = int(input("Digite a KM atual da moto na troca: "))
            km_proxima = int(input("Com quantos KM a peça deve ser trocada novamente? (Ex: 2000): "))
            meses_proxima = int(input("Em quantos meses a peça deve ser trocada novamente? (Ex: 12): "))

            item = ManutencaoItem(nome, valor, data_troca, km_troca, km_proxima, meses_proxima)
            self.itens.append(item)
            print("\nItem adicionado com sucesso!\n")
        except ValueError:
            print("\nErro: Formato de entrada inválido. Tente novamente.\n")

    def remover_item(self):
        if not self.itens:
            print("\nNenhum item para remover.\n")
            return

        print("\n--- Itens para Remoção ---")
        for i, item in enumerate(self.itens):
            print(f"[{i}] {item.nome}")

        try:
            indice = int(input("\nDigite o número do item que deseja remover: "))
            if 0 <= indice < len(self.itens):
                item_removido = self.itens.pop(indice)
                print(f"\nItem '{item_removido.nome}' removido com sucesso!\n")
            else:
                print("\nÍndice inválido.\n")
        except ValueError:
            print("\nErro: Digite um número válido.\n")

    def gerar_relatorio_tela(self):
        if not self.itens:
            print("\nNenhum item de manutenção registrado.\n")
            return

        print("\n--- Relatório de Manutenção ---\n")
        for item in self.itens:
            print(item)
            print("-" * 25)

    def gerar_relatorio_txt(self):
        if not self.itens:
            print("\nNenhum item para gerar relatório.\n")
            return

        data_hoje = datetime.date.today().strftime("%Y-%m-%d")
        nome_arquivo = os.path.join(self.diretorio_relatorios, f"relatorio_{data_hoje}.txt")
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DE MANUTENÇÃO\n")
            f.write("=" * 25 + "\n\n")
            for item in self.itens:
                f.write(str(item) + "\n")
                f.write("-" * 25 + "\n")
        
        print(f"\nRelatório salvo com sucesso em: {nome_arquivo}\n")

    def exibir_menu(self):
        while True:
            print("--- Menu de Manutenção Veicular ---")
            print("[1] Adicionar novo item de manutenção")
            print("[2] Remover item de manutenção")
            print("[3] Gerar relatório em tela")
            print("[4] Gerar relatório em arquivo de texto (.txt)")
            print("[5] Sair")
            
            escolha = input("\nEscolha uma opção: ")

            if escolha == '1':
                self.adicionar_item()
            elif escolha == '2':
                self.remover_item()
            elif escolha == '3':
                self.gerar_relatorio_tela()
            elif escolha == '4':
                self.gerar_relatorio_txt()
            elif escolha == '5':
                print("Saindo do programa. Até a próxima!")
                break
            else:
                print("\nOpção inválida. Por favor, tente novamente.\n")

if __name__ == "__main__":
    gerenciador = GerenciadorManutencao()
    gerenciador.exibir_menu()