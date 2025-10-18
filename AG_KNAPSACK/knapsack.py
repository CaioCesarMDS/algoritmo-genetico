# Atividade Hill Climbing
# Aluno: Alrykemes Gomes Cavalcanti
# Discente: Rodrigo Lira

# Import das constants
from constants import A_20, C_20, S_20

def _knapsack_constants(dim):
    GANHOS = []
    PESOS = []
    CAPACIDADE_MAXIMA = 0

    if dim == 20:
        GANHOS = A_20
        PESOS = C_20
        CAPACIDADE_MAXIMA = S_20

    return GANHOS, PESOS, CAPACIDADE_MAXIMA

# FUNCAO KNAPSACK
def knapsack(solution, dim=20):
    """
    Avalia uma seleção de itens para o problema da mochila com 20 dimensões.
    https://en.wikipedia.org/wiki/Knapsack_problem

    Args:
        solution: lista binária [0,1,0,1,...] indicando quais itens foram selecionados

    Returns:
        tuple: (valor_total, peso_total, é_válido)
    """

    # A instância implementada considera 20 dimensões
    assert len(solution) == dim, "A solução deve ter exatamente 20 dimensões."

    # Valores dos itens (benefícios)
    GANHOS, PESOS, CAPACIDADE_MAXIMA = _knapsack_constants(dim)

    # Calcula valor total e peso total dos itens selecionados
    ganho_total = 0
    peso_total = 0

    for i in range(len(solution)):
        if solution[i] == 1:  # Item foi selecionado
            ganho_total += GANHOS[i]
            peso_total += PESOS[i]

    # Verifica se a solução é válida (não excede a capacidade)
    eh_valido = peso_total <= CAPACIDADE_MAXIMA

    if not eh_valido:
        ganho_total = 0

    return ganho_total, peso_total, eh_valido

# FUNCAO GERAR VIZINHOS

def gerar_vizinhos_knapsack(solucao, n_vizinhos=20):
    """
    Gera vizinhos para o problema knapsack
    Estratégia: flip de um bit aleatório

    Args:
        solucao: solução binária atual
        n_vizinhos: número de vizinhos

    Returns:
        list: lista de vizinhos
    """
    vizinhos = []
    n_itens = len(solucao)

    # Gerar vizinhos por flip de bit
    sorted_pos = []
    for i in range(n_vizinhos):
        # Escolher posição aleatória para flip
        pos = random.randint(0, n_itens - 1)
        if pos in sorted_pos:
            continue

        vizinho = solucao.copy()
        vizinho[pos] = 1 - vizinho[pos]  # Flip do bit
        vizinhos.append(vizinho)
        sorted_pos.append(pos)

    return vizinhos

# 1 - Knapsack com 20 dimensões:

if __name__ == "__main__":

    print("=== RESOLUÇÃO APENAS KNAPSACK ===\n")

    # Exemplo 1: Selecionar apenas o item 1 (índice 1)
    selecao1 = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    valor, peso, valido = knapsack(selecao1)
    print(f"Seleção: {selecao1}")
    print(f"Valor: {valor}, Peso: {peso}, Válido: {valido}\n")

    # Exemplo 2: Selecionar itens leves (índices 1, 4, 6)
    selecao2 = [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0]
    valor, peso, valido = knapsack(selecao2)
    print(f"Seleção: {selecao2}")
    print(f"Valor: {valor}, Peso: {peso}, Válido: {valido}\n")

    # Exemplo 3: Tentar selecionar muitos itens (pode exceder capacidade)
    selecao3 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    valor, peso, valido = knapsack(selecao3)
    print(f"Seleção: {selecao3}")
    print(f"Valor: {valor}, Peso: {peso}, Válido: {valido}\n")

    # Mostra informações dos itens
    print("=== INFORMAÇÕES DOS ITENS ===")
    ganhos = A_20
    pesos = C_20

    print("Item | Valor | Peso | Razão Valor/Peso")
    print("-" * 35)
    for i in range(20):
        razao = ganhos[i] / pesos[i]
        print(f"{i:4d} | {ganhos[i]:5d} | {pesos[i]:4d} | {razao:.3f}")

    print("\nCapacidade máxima da mochila: ", S_20, "\n\n\n\n\n")


# 2 - Resolvendo Knapsack com 20 dimensões utilizando o algoritmo Hill Climbing:
import copy
import random
import matplotlib.pyplot as plt
import numpy as np


class HillClimbing:
    def __init__(self, funcao_fitness, gerar_vizinhos, maximizar=True):
        """
        Inicializa o algoritmo Hill Climbing

        Args:
            funcao_fitness: função que avalia soluções
            gerar_vizinhos: função que gera vizinhos de uma solução
            maximizar: True para maximização, False para minimização
        """
        self.funcao_fitness = funcao_fitness
        self.gerar_vizinhos = gerar_vizinhos
        self.maximizar = maximizar
        self.historico = []

    def executar(self, solucao_inicial, max_iteracoes=1000, verbose=False):
        """
        Executa o algoritmo Hill Climbing

        Args:
            solucao_inicial: solução inicial
            max_iteracoes: número máximo de iterações
            verbose: imprimir progresso

        Returns:
            tuple: (melhor_solucao, melhor_fitness, historico)
        """
        solucao_atual = copy.deepcopy(solucao_inicial)
        fitness_atual = self.funcao_fitness(solucao_atual)

        self.historico = [fitness_atual]
        iteracao = 0
        melhorias = 0

        if verbose:
            print(f"Iteração {iteracao}: Fitness = {fitness_atual:.4f}")

        while iteracao < max_iteracoes:
            iteracao += 1

            # Gerar vizinhos
            vizinhos = self.gerar_vizinhos(solucao_atual)

            # Avaliar vizinhos e encontrar o melhor
            melhor_vizinho = None
            melhor_fitness_vizinho = fitness_atual

            for vizinho in vizinhos:
                fitness_vizinho = self.funcao_fitness(vizinho)

                # Verificar se é melhor
                eh_melhor = (
                    fitness_vizinho > melhor_fitness_vizinho
                    if self.maximizar
                    else fitness_vizinho < melhor_fitness_vizinho
                )

                if eh_melhor:
                    melhor_vizinho = vizinho
                    melhor_fitness_vizinho = fitness_vizinho

            # Se encontrou vizinho melhor, move para ele
            if melhor_vizinho is not None:
                solucao_atual = copy.deepcopy(melhor_vizinho)
                fitness_atual = melhor_fitness_vizinho
                melhorias += 1

                if verbose:
                    print(f"Iteração {iteracao}: Fitness = {fitness_atual:.4f}")
            else:
                # Nenhum vizinho melhor encontrado - parar
                if verbose:
                    print(f"Convergiu na iteração {iteracao}")
                break

            self.historico.append(fitness_atual)

        if verbose:
            print(f"Melhorias realizadas: {melhorias}")
            print(f"Fitness final: {fitness_atual:.4f}")

        return solucao_atual, fitness_atual, self.historico


def loop_das_execucoes(
    n_execucoes=30, dim=20, max_iteracoes=200, algoritmo="tradicional"
):
    resultados = []

    for _ in range(n_execucoes):
        solucao = [int(random.random() > 0.8) for _ in range(dim)]

        hill_climbing = HillClimbing(
            funcao_fitness=lambda sol: knapsack(sol, dim=dim)[0],
            gerar_vizinhos=gerar_vizinhos_knapsack,
            maximizar=True,
        )

        melhor_solucao, melhor_fitness, historico = hill_climbing.executar(
            solucao_inicial=solucao, max_iteracoes=max_iteracoes, verbose=False
        )

        resultados.append(melhor_fitness)

    return resultados


if __name__ == "__main__":

    N_EXECUCOES = 30
    resultados = loop_das_execucoes(n_execucoes=N_EXECUCOES)

    media = np.mean(resultados)
    desvio = np.std(resultados)

    print("\n=== RESULTADOS FINAIS DO HILL CLIMBING ===")
    print(f"Número de execuções: {N_EXECUCOES}")
    print(f"Média do fitness final: {media:.2f}")
    print(f"Desvio padrão do fitness final: {desvio:.2f}")
    print(f"Melhor fitness obtido: {max(resultados)}")
    print(f"Pior fitness obtido: {min(resultados)}")

    ## Gráficos de BoxPlot com todos os fitness

    plt.figure(figsize=(8, 6))
    plt.boxplot(resultados, patch_artist=True, boxprops=dict(facecolor="lightblue"))
    plt.title("Distribuição do Fitness Final (Hill Climbing)")
    plt.ylabel("Fitness (valor total da mochila)")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.show()

# 3 - Resolvendo Knapsack com 20 dimensões com 30 interações utilizando o Stocastic Hill Climbing.


class HillClimbingStochastic:
    def __init__(self, funcao_fitness, gerar_vizinhos, maximizar=True):
        """
        Inicializa o algoritmo Hill Climbing Stochastic

        Args:
            funcao_fitness: função que avalia soluções
            gerar_vizinhos: função que gera vizinhos de uma solução
            maximizar: True para maximização, False para minimização
        """
        self.funcao_fitness = funcao_fitness
        self.gerar_vizinhos = gerar_vizinhos
        self.maximizar = maximizar
        self.historico = []

    def executar(self, solucao_inicial, max_iteracoes=1000, verbose=False):
        """
        Executa o algoritmo Hill Climbing Stochastic

        Args:
            solucao_inicial: solução inicial
            max_iteracoes: número máximo de iterações
            verbose: imprimir progresso

        Returns:
            tuple: (melhor_solucao, melhor_fitness, historico)
        """
        solucao_atual = copy.deepcopy(solucao_inicial)
        fitness_atual = self.funcao_fitness(solucao_atual)

        self.historico = [fitness_atual]
        iteracao = 0
        melhorias = 0

        if verbose:
            print(f"Iteração {iteracao}: Fitness = {fitness_atual:.4f}")

        while iteracao < max_iteracoes:
            iteracao += 1

            # Gerar vizinhos
            vizinhos = self.gerar_vizinhos(solucao_atual)

            vizinhos_melhores = []

            for vizinho in vizinhos:
                fitness_vizinho = self.funcao_fitness(vizinho)

                # Verificar se é melhor
                eh_melhor = (
                    fitness_vizinho > fitness_atual
                    if self.maximizar
                    else fitness_vizinho < fitness_atual
                )

                if eh_melhor:
                    vizinhos_melhores.append((vizinho, fitness_vizinho))

            # Se encontrou vizinho melhor, move para ele
            if vizinhos_melhores:
                vizinho, fitness_vizinho = random.choice(vizinhos_melhores)
                solucao_atual = copy.deepcopy(vizinho)
                fitness_atual = fitness_vizinho
                melhorias += 1

                if verbose:
                    print(f"Iteração {iteracao}: Fitness = {fitness_atual:.4f}")
            else:
                # Nenhum vizinho melhor encontrado - parar
                if verbose:
                    print(f"Convergiu na iteração {iteracao}")
                break

            self.historico.append(fitness_atual)

        if verbose:
            print(f"Melhorias realizadas: {melhorias}")
            print(f"Fitness final: {fitness_atual:.4f}")

        return solucao_atual, fitness_atual, self.historico


if __name__ == "__main__":
    # Configuração do problema knapsack
    DIM = 20
    MAX_ITERACOES = 200

    # Gerar solução inicial aleatória
    solucao_inicial = [int(random.random() > 0.8) for _ in range(DIM)]

    # Inicializar e executar Hill Climbing
    hill_climbing = HillClimbing(
        funcao_fitness=lambda sol: knapsack(sol, dim=DIM)[0],  # Maximizar valor total
        gerar_vizinhos=gerar_vizinhos_knapsack,
        maximizar=True,
    )

    melhor_solucao, melhor_fitness, historico = hill_climbing.executar(
        solucao_inicial, max_iteracoes=MAX_ITERACOES, verbose=True
    )

    print("\n=== RESULTADOS FINAIS ===")
    print(f"Solução inicial: {solucao_inicial}")
    print(f"Melhor solução: {melhor_solucao}")
    print(f"Melhor valor total: {melhor_fitness}")
    peso_total = knapsack(melhor_solucao, dim=DIM)[1]
    print(f"Peso total da melhor solução: {peso_total}")

    print("\nHistórico de fitness ao longo das iterações:")
    print(historico)

    resultados_tradicional = loop_das_execucoes(
        n_execucoes=30, dim=20, max_iteracoes=200
    )
    resultados_stochastic = loop_das_execucoes(
        n_execucoes=30, dim=20, max_iteracoes=200, algoritmo="stochastic"
    )

    plt.figure(figsize=(10, 6))
    plt.boxplot(
        [resultados_tradicional, resultados_stochastic],
        labels=["Tradicional", "Stochastic"],
        patch_artist=True,
    )
    plt.title("Comparação: Hill Climbing Tradicional vs Stochastic")
    plt.ylabel("Fitness final")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()
