import copy
import random

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
            melhores_vizinhos = []

            for vizinho in vizinhos:
                fitness_vizinho = self.funcao_fitness(vizinho)

                # Verificar se é melhor
                eh_melhor = (
                    fitness_vizinho > fitness_atual
                    if self.maximizar
                    else fitness_vizinho < fitness_atual
                )

                if eh_melhor:
                    melhores_vizinhos.append((vizinho, fitness_vizinho))

            # Se encontrou vizinhos melhores, escolhe um aleatoriamente
            if melhores_vizinhos:
                vizinho_escolhido, fitness_escolhido = random.choice(melhores_vizinhos)
                solucao_atual = vizinho_escolhido
                fitness_atual = fitness_escolhido
                melhorias += 1

                if verbose:
                    print(f"Iteração {iteracao}: Fitness = {fitness_atual:.4f}")
            else:
                if verbose:
                    print(f"Convergiu na iteração {iteracao}")
                break

            self.historico.append(fitness_atual)

        if verbose:
            print(f"Melhorias realizadas: {melhorias}")
            print(f"Fitness final: {fitness_atual:.4f}")

        return solucao_atual, fitness_atual, self.historico

if __name__ == "__main__":
    import sys
    from knapsack import knapsack
    import random
    import numpy as np
    import matplotlib.pyplot as plt

    # Configuração do problema knapsack
    DIM = 20
    MAX_ITERACOES = 200
    N_SIMULACOES = 30
    lista_fitness_simulacoes = []

    for i in range(N_SIMULACOES):
        # Gerar solução inicial aleatória
        solucao_inicial = [int(random.random() > 0.8) for _ in range(DIM)]

        # Inicializar e executar Hill Climbing
        hill_climbing = HillClimbing(
            funcao_fitness=lambda sol: knapsack(sol, dim=DIM)[0],  # Maximizar valor total
            gerar_vizinhos=gerar_vizinhos_knapsack,
            maximizar=True,
        )

        _, melhor_fitness, _ = hill_climbing.executar(
            solucao_inicial, max_iteracoes=MAX_ITERACOES, verbose=False
        )
        lista_fitness_simulacoes.append(melhor_fitness)

# Analisar resultados após todas as simulações
media = np.mean(lista_fitness_simulacoes)
desvio_padrao = np.std(lista_fitness_simulacoes)
print(f"\n--- RESULTADOS FINAIS APÓS {N_SIMULACOES} SIMULAÇÕES ---")
print(f"Fitness médio: {media:.2f}")
print(f"Desvio padrão: {desvio_padrao:.2f}")

# Plotar boxplot dos resultados
plt.boxplot(lista_fitness_simulacoes)
plt.title(f"\n--- Distribuição do Fitness após {N_SIMULACOES} simulações ---")
plt.ylabel("Fitness (Valor Total da Mochila)")
plt.show()
