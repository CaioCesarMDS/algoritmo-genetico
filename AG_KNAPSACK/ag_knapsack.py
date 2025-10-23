import random
from knapsack import knapsack
import numpy
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from hill_climbing import HillClimbing
from stochaist_hill_climbing import StocasticHillClimbing
from hill_climbing import gerar_vizinhos_knapsack


def gerar_populacao(tamanho_populacao, n_itens):
    # Gera uma população inicial aleatória
    populacao = []
    for _ in range(tamanho_populacao):
        individuo = [int(random.random() > 0.8) for _ in range(n_itens)]
        populacao.append(individuo)
    return populacao


def avaliar_populacao(populacao):
    fitness = []

    for solucao in populacao:
        fitness.append(knapsack(solucao, 20))

    return fitness


def selecao_torneio(avaliacao, populacao, tamanho_torneio=3):
    """
    Seleciona um indivíduo usando torneio de tamanho definido (padrão: 3).
    Retorna apenas o indivíduo vencedor.
    """
    # Escolhe aleatoriamente 'tamanho_torneio'(3) indivíduos da lista [0,...,19]
    indices = random.sample(range(len(populacao)), tamanho_torneio)

    # Cria uma lista com (fitness, indivíduo) para os competidores
    competidores = [(avaliacao[i], populacao[i]) for i in indices]

    # Seleciona o indivíduo com o maior fitness
    vencedor = max(competidores, key=lambda x: x[0])[1]

    return vencedor


def aplicar_crossover(pai1, pai2, tipo="um_ponto", taxa_crossover=0.8):
    """
    Aplica crossover entre dois pais conforme o tipo especificado.
    Tipos: "um_ponto", "dois_pontos", "uniforme"
    """
    # Verifica se o crossover deve ser aplicado com base na taxa (0.8)
    if random.random() >= taxa_crossover:
        return pai1.copy(), pai2.copy()

    n = len(pai1)

    if tipo == "um_ponto":
        # pega um ponto de corte aleatório entre 1 e n-1 (entre 1 e 19)
        ponto = random.randint(1, n - 1)

        # cria o filho com a primeira parte do pai1 até o ponto de corte e a segunda parte do pai2 a partir do ponto de corte
        filho1 = pai1[:ponto] + pai2[ponto:]

        # cria o filho com a primeira parte do pai2 até o ponto de corte e a segunda parte do pai1 a partir do ponto de corte
        filho2 = pai2[:ponto] + pai1[ponto:]

    elif tipo == "dois_pontos":
        # pega dois pontos de corte aleatórios entre 1 e n-1 (entre 1 e 19) e ordena-os, ponto1 < ponto2
        ponto1, ponto2 = sorted(random.sample(range(1, n - 1), 2))

        # cria o filho com a primeira parte do pai1 até o ponto1, a parte do pai2 entre ponto1 e ponto2, e a parte do pai1 a partir do ponto2
        filho1 = pai1[:ponto1] + pai2[ponto1:ponto2] + pai1[ponto2:]

        # cria o filho com a primeira parte do pai2 até o ponto1, a parte do pai1 entre ponto1 e ponto2, e a parte do pai2 a partir do ponto2
        filho2 = pai2[:ponto1] + pai1[ponto1:ponto2] + pai2[ponto2:]

    elif tipo == "uniforme":
        filho1, filho2 = [], []
        # junta os genes de mesmo índice dos dois pais. Para cada par de genes, escolhe aleatoriamente qual gene vai para qual filho
        for g1, g2 in zip(pai1, pai2):
            if random.random() < 0.5:
                filho1.append(g1)
                filho2.append(g2)
            else:
                filho1.append(g2)
                filho2.append(g1)

    else:
        raise ValueError("Tipo de crossover inválido.")

    return filho1, filho2


def aplicar_mutacao(individuo, taxa_mutacao=0.02):
    """
    Aplica mutação bit-flip a um indivíduo.
    Cada bit tem chance 'taxa_mutacao' de ser invertido (0 → 1 ou 1 → 0).
    """
    novo_individuo = individuo.copy()
    for i in range(len(novo_individuo)):
        if random.random() < taxa_mutacao:
            novo_individuo[i] = 1 - novo_individuo[i]  # inverte o bit

    return novo_individuo


def elitismo(populacao, fitness, nova_populacao, fitness_nova_populacao, n_elite=2):
    """
    Substitui os piores indivíduos da nova população pelos melhores da antiga.
    """
    # Encontra os índices(n_elite = 2) dos melhores da população antiga, cada indivíduo é representado por seu índice na lista
    elite_indices = sorted(range(len(fitness)), key=lambda i: fitness[i], reverse=True)[
        :n_elite
    ]

    # pega os melhores indivíduos
    elite = [populacao[i] for i in elite_indices]
    elite_fitness = [fitness[i] for i in elite_indices]

    # Encontra os índices dos piores da nova população
    piores_indices = sorted(
        range(len(fitness_nova_populacao)), key=lambda i: fitness_nova_populacao[i]
    )[:n_elite]

    # Substitui os piores da nova população pelos melhores da antiga
    for idx_pior, elite_ind, elite_fit in zip(piores_indices, elite, elite_fitness):
        nova_populacao[idx_pior] = elite_ind
        fitness_nova_populacao[idx_pior] = elite_fit

    return nova_populacao, fitness_nova_populacao


def rodar_algoritmo_genetico(tamanho_populacao, n_itens, tipo_crossover, taxa_crossover, taxa_mutacao, n_geracoes):
    populacao = gerar_populacao(tamanho_populacao, n_itens)
    historico_melhor = []  # Armazena o melhor fitness por geração

    for _ in range(n_geracoes):
        fitness = avaliar_populacao(populacao)
        historico_melhor.append(max(fitness))

        nova_populacao = []
        while len(nova_populacao) < tamanho_populacao:
            pai1 = selecao_torneio(fitness, populacao)
            pai2 = selecao_torneio(fitness, populacao)
            filho1, filho2 = aplicar_crossover(pai1, pai2, tipo=tipo_crossover, taxa_crossover=taxa_crossover)
            filho1 = aplicar_mutacao(filho1, taxa_mutacao)
            filho2 = aplicar_mutacao(filho2, taxa_mutacao)
            nova_populacao.extend([filho1, filho2])

        nova_populacao = nova_populacao[:tamanho_populacao]
        fitness_nova_populacao = avaliar_populacao(nova_populacao)
        nova_populacao, fitness_nova_populacao = elitismo(populacao, fitness, nova_populacao, fitness_nova_populacao, 2)
        populacao = nova_populacao

    fitness_final = avaliar_populacao(populacao)
    melhor_final = max(fitness_final)
    return melhor_final, historico_melhor


# === Executa todas as configurações e gera gráficos ===
def experimento(tamanho_populacao=50, n_itens=20, n_geracoes=500, n_execucoes=10, taxa_crossover=0.8, taxa_mutacao=0.02):
    tipos = ["um_ponto", "dois_pontos", "uniforme"]
    resultados = []
    dados_convergencia = []
    dados_boxplot = []

    for tipo in tipos:
        melhores = []
        print(f"\nExecutando configuração: {tipo}")
        for _ in range(n_execucoes):
            
            melhor_final, historico = rodar_algoritmo_genetico(
                tamanho_populacao, n_itens, tipo, taxa_crossover, taxa_mutacao, n_geracoes
            )
            
            melhores.append(melhor_final)

            # Armazena para o gráfico de convergência
            for g, fit in enumerate(historico):
                dados_convergencia.append({"config": tipo, "geracao": g, "melhor_fitness": fit})

            # Armazena para o boxplot
            dados_boxplot.append({"config": tipo, "melhor_fitness_final": melhor_final})
        resultados.append({tipo: { "melhor": max(melhores), "média": sum(melhores) / len(melhores), "desvio de padrão": numpy.std(melhores) }})

    return dados_convergencia, dados_boxplot, resultados


# === Execução principal ===
if __name__ == "__main__":
    
    dados_boxplot = []
    
    dados_convergencia, dados_boxplot, res = experimento(
        tamanho_populacao=50,
        n_itens=20,
        n_geracoes=500,
        n_execucoes=30,
        taxa_crossover=0.8,
        taxa_mutacao=0.02,
    )
        
    # Printa resultados
    for res in res:
        print(res, "\n")   
                            
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
            funcao_fitness=lambda sol: knapsack(sol, dim=DIM),  # Maximizar valor total
            gerar_vizinhos=gerar_vizinhos_knapsack,
            maximizar=True,
        )

        _, melhor_fitness, _ = hill_climbing.executar(
            solucao_inicial, max_iteracoes=MAX_ITERACOES, verbose=False
        )
        lista_fitness_simulacoes.append(melhor_fitness)
    
    dados_boxplot.append({"config": "Hill Climbing", "melhor_fitness_final": max(lista_fitness_simulacoes)})
            
    # Configuração do problema knapsack
    DIM = 20
    MAX_ITERACOES = 200
    N_SIMULACOES = 30
    lista_fitness_simulacoes = []

    for i in range(N_SIMULACOES):
        # Gerar solução inicial aleatória
        solucao_inicial = [int(random.random() > 0.8) for _ in range(DIM)]

        # Inicializar e executar Hill Climbing
        hill_climbing = StocasticHillClimbing(
            funcao_fitness=lambda sol: knapsack(sol, dim=DIM),  # Maximizar valor total
            gerar_vizinhos=gerar_vizinhos_knapsack,
            maximizar=True,
        )

        _, melhor_fitness, _ = hill_climbing.executar(
            solucao_inicial, max_iteracoes=MAX_ITERACOES, verbose=False
        )
        lista_fitness_simulacoes.append(melhor_fitness)
        
    dados_boxplot.append({"config": "Stocastic Hill Climbing", "melhor_fitness_final": max(lista_fitness_simulacoes)})
        
    # Cria DataFrames
    df_conv = pd.DataFrame(dados_convergencia)
    df_box = pd.DataFrame(dados_boxplot)

    # === Gráfico de convergência ===
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_conv, x="geracao", y="melhor_fitness", hue="config")
    plt.title("Convergência do Algoritmo Genético")
    plt.xlabel("Geração")
    plt.ylabel("Melhor Fitness")
    plt.grid(True)
    plt.show()

    # === Boxplot comparando configurações ===
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df_box, x="config", y="melhor_fitness_final")
    plt.title("Comparação das Configurações do AG")
    plt.xlabel("Configuração")
    plt.ylabel("Melhor Fitness Final")
    plt.grid(True)
    plt.show()
