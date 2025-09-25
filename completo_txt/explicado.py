# -*- coding: utf-8 -*-

# Este é o primeiro passo: importar bibliotecas.
# A biblioteca 'datetime' nos ajuda a lidar com datas e horários, como calcular a data da próxima troca.
import datetime
# A biblioteca 'os' nos permite interagir com o sistema operacional, como criar pastas no seu computador.
import os

# Começamos a criar um "molde" ou "receita de bolo" para um item de manutenção.
# Cada vez que você adiciona uma peça, o programa usa este molde para criar um objeto.
class ManutencaoItem:
    # Este método, chamado '__init__', é o "construtor". Ele é a primeira coisa que roda
    # quando criamos um novo item. Ele pega as informações que você digitou (nome, valor, etc.)
    # e as armazena dentro do objeto que acabou de ser criado.
    # 'self' é uma palavra-chave especial que se refere ao próprio objeto que estamos montando.
    def __init__(self, nome, valor, data_troca, km_troca, km_proxima, meses_proxima):
        # Aqui, estamos guardando cada informação que foi passada para o construtor.
        self.nome = nome
        self.valor = valor
        self.data_troca = data_troca
        self.km_troca = km_troca
        self.km_proxima = km_proxima
        self.meses_proxima = meses_proxima

    # Este outro método especial, '__str__', decide como o nosso objeto vai ser exibido
    # quando o imprimimos (por exemplo, usando o comando 'print').
    # Ele formata todas as informações de uma forma fácil de ler para o usuário.
    def __str__(self):
        # A matemática é simples: a próxima troca é a KM atual + a KM recomendada.
        proxima_troca_km = self.km_troca + self.km_proxima
        
        # Para calcular a próxima data, pegamos a data da troca e adicionamos
        # um número de dias. Usamos 30 dias como uma aproximação para um mês.
        proxima_data_troca = self.data_troca + datetime.timedelta(days=self.meses_proxima * 30)
        
        # 'f-string' é uma forma moderna de formatar texto. Tudo que está dentro das chaves {}
        # é substituído pelo valor da variável.
        # Por exemplo, {self.nome} se torna o nome da peça.
        return (
            f"--- {self.nome} ---\n"
            f"Valor: R$ {self.valor:.2f}\n"  # O '.2f' formata o valor com duas casas decimais.
            f"Data da troca: {self.data_troca.strftime('%d/%m/%Y')}\n" # Formata a data para Dia/Mês/Ano.
            f"KM da troca: {self.km_troca} km\n"
            f"Próxima troca recomendada: {proxima_troca_km} km ou {proxima_data_troca.strftime('%d/%m/%Y')}\n"
        )

# Agora, vamos criar o "cérebro" do nosso programa, a classe que vai gerenciar tudo.
# Ela vai ser responsável por adicionar, remover e gerar relatórios.
class GerenciadorManutencao:
    # O construtor desta classe cria a lista que vai guardar todos os itens de manutenção.
    def __init__(self):
        self.itens = [] # Uma lista vazia para começar.
        self.diretorio_relatorios = "relatorios_manutencao"
        # Usamos o 'os' para verificar se a pasta 'relatorios_manutencao' já existe.
        # Se ela não existir ('not os.path.exists'), o código a cria ('os.makedirs').
        if not os.path.exists(self.diretorio_relatorios):
            os.makedirs(self.diretorio_relatorios)

    # Este método é o que permite adicionar um novo item de manutenção.
    def adicionar_item(self):
        # 'try...except' é uma forma de tratar erros. O código dentro do 'try' é executado.
        # Se algo der errado (por exemplo, o usuário digita texto onde deveria ser um número),
        # o 'except ValueError' é acionado e o código mostra uma mensagem de erro em vez de travar.
        try:
            # Pedimos ao usuário para digitar as informações.
            nome = input("Digite o nome da peça ou serviço: ")
            valor = float(input("Digite o valor da peça/item (Ex: 50.00): ")) # Converte o texto para um número com casas decimais.
            data_troca_str = input("Digite a data da troca (DD/MM/AAAA): ")
            # Converte a string de data para um formato que o Python entende como uma data real.
            data_troca = datetime.datetime.strptime(data_troca_str, '%d/%m/%Y').date()
            km_troca = int(input("Digite a KM atual da moto na troca: ")) # Converte o texto para um número inteiro.
            km_proxima = int(input("Com quantos KM a peça deve ser trocada novamente? (Ex: 2000): "))
            meses_proxima = int(input("Em quantos meses a peça deve ser trocada novamente? (Ex: 12): "))

            # Chamamos o molde 'ManutencaoItem' para criar um novo objeto com os dados que o usuário forneceu.
            item = ManutencaoItem(nome, valor, data_troca, km_troca, km_proxima, meses_proxima)
            # Adicionamos o novo objeto à nossa lista de itens.
            self.itens.append(item)
            print("\nItem adicionado com sucesso!\n")
        except ValueError:
            # Esta mensagem aparece se o 'try' falhar.
            print("\nErro: Formato de entrada inválido. Tente novamente.\n")

    # Este método é para remover um item da lista.
    def remover_item(self):
        # Primeiro, verificamos se a lista de itens está vazia. Se estiver, não há o que remover.
        if not self.itens:
            print("\nNenhum item para remover.\n")
            # O 'return' sai do método.
            return

        print("\n--- Itens para Remoção ---")
        # O 'enumerate' nos dá um número (índice) para cada item na lista, o que é útil
        # para o usuário saber qual número digitar para remover o item correto.
        for i, item in enumerate(self.itens):
            print(f"[{i}] {item.nome}")

        try:
            indice = int(input("\nDigite o número do item que deseja remover: "))
            # Verificamos se o número que o usuário digitou é válido (está dentro do alcance da lista).
            if 0 <= indice < len(self.itens):
                # O 'pop(indice)' remove o item da lista usando o número que o usuário forneceu.
                item_removido = self.itens.pop(indice)
                print(f"\nItem '{item_removido.nome}' removido com sucesso!\n")
            else:
                print("\nÍndice inválido.\n")
        except ValueError:
            print("\nErro: Digite um número válido.\n")

    # Este método apenas mostra o relatório na tela do seu computador.
    def gerar_relatorio_tela(self):
        if not self.itens:
            print("\nNenhum item de manutenção registrado.\n")
            return

        print("\n--- Relatório de Manutenção ---\n")
        # 'for' é um loop que passa por cada 'item' dentro da nossa lista 'self.itens'.
        for item in self.itens:
            # 'print(item)' automaticamente chama o método '__str__' que criamos,
            # formatando o texto para ser exibido.
            print(item)
            print("-" * 25)

    # Este método salva o relatório em um arquivo de texto.
    def gerar_relatorio_txt(self):
        if not self.itens:
            print("\nNenhum item para gerar relatório.\n")
            return

        # Pega a data de hoje para nomear o arquivo de forma única.
        data_hoje = datetime.date.today().strftime("%Y-%m-%d")
        # O 'os.path.join' junta o nome da pasta e o nome do arquivo para criar um caminho completo.
        nome_arquivo = os.path.join(self.diretorio_relatorios, f"relatorio_{data_hoje}.txt")
        
        # 'with open(...)' abre o arquivo. A 'w' significa que estamos abrindo para 'write' (escrever).
        # A codificação 'utf-8' garante que caracteres especiais como 'ç' e 'ã' funcionem.
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DE MANUTENÇÃO\n")
            f.write("=" * 25 + "\n\n")
            # Um loop para escrever cada item no arquivo.
            for item in self.itens:
                f.write(str(item) + "\n")
                f.write("-" * 25 + "\n")
        
        print(f"\nRelatório salvo com sucesso em: {nome_arquivo}\n")

    # Este é o método principal que mostra o menu e controla a interação com o usuário.
    def exibir_menu(self):
        # 'while True' cria um loop infinito que só para quando o usuário escolhe a opção '5'.
        while True:
            print("--- Menu de Manutenção Veicular ---")
            print("[1] Adicionar novo item de manutenção")
            print("[2] Remover item de manutenção")
            print("[3] Gerar relatório em tela")
            print("[4] Gerar relatório em arquivo de texto (.txt)")
            print("[5] Sair")
            
            escolha = input("\nEscolha uma opção: ")

            # Verificamos a escolha do usuário e chamamos o método correspondente.
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
                # O 'break' sai do loop 'while True', encerrando o programa.
                break
            else:
                print("\nOpção inválida. Por favor, tente novamente.\n")

# Esta parte do código é o "botão de ligar" do nosso programa.
# O Python só executa o código que está dentro deste bloco quando você executa o arquivo diretamente.
if __name__ == "__main__":
    # Criamos uma instância (um objeto real!) da classe 'GerenciadorManutencao'.
    gerenciador = GerenciadorManutencao()
    # E chamamos o método para mostrar o menu, iniciando a interação com o usuário.
    gerenciador.exibir_menu()
