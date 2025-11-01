import random
from TSP_13_cities.tsp_utils import calculate_distance
import numpy
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import time

def gerar_populacao(tamanho_populacao):
    # Gera uma população inicial aleatória
    populacao = []
    ex_route = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    for _ in range(tamanho_populacao):
        individuo = random.sample(ex_route, len(ex_route))
        populacao.append(individuo)
    return populacao

def avaliar_populacao(populacao):
    fitness = []
    for individuo in populacao:
        fitness.append(calculate_distance(individuo))
    return fitness

def order_crossover(pai1, pai2, taxa_crossover=0.9):
    if random.random() >= taxa_crossover:
        return pai1.copy(), pai2.copy()

    n = len(pai1)
    ponto1, ponto2 = sorted(random.sample(range(n), 2))

    # inicializa filhos vazios
    filho1 = [None] * n
    filho2 = [None] * n

    # copia segmento entre os pontos de corte
    filho1[ponto1:ponto2] = pai1[ponto1:ponto2]
    filho2[ponto1:ponto2] = pai2[ponto1:ponto2]

    # preenche restante com cidades do outro pai
    preencher(filho1, pai2, ponto2)
    preencher(filho2, pai1, ponto2)

    return filho1, filho2

def preencher(filho, pai, inicio):
    n = len(pai)
    pos = inicio
    for cidade in pai:
        if cidade not in filho:
            filho[pos % n] = cidade
            pos += 1

def selecao_torneio(avaliacao, populacao, tamanho_torneio=3):
    """
    Seleciona um indivíduo usando torneio de tamanho definido (padrão: 3).
    Retorna apenas o indivíduo vencedor.
    """
    # Seleciona aleatoriamente 3 indivíduos
    competidores = random.sample(range(len(populacao)), tamanho_torneio)
    # Retorna o melhor (menor valor de fitness)
    vencedor = min(competidores, key=lambda ind: avaliacao[ind])
    
    return populacao[vencedor]

def aplicar_mutacao_swap(individuo, taxa_mutacao=0.05):
    """
    Aplica mutação swap a um indivíduo.
    Cada par de cidades tem chance 'taxa_mutacao' de ter suas posições trocadas.
    """
    novo_individuo = individuo.copy()
    for i in range(len(novo_individuo)):
        if random.random() < taxa_mutacao:
            # Escolhe duas posições diferentes
            i, j = random.sample(range(len(novo_individuo)), 2)
            # Troca os valores
            novo_individuo[i], novo_individuo[j] = novo_individuo[j], novo_individuo[i]

    return novo_individuo

def elitismo(populacao, fitness, nova_populacao, fitness_nova_populacao, n_elite=5):
    """
    Mantém os n_elite melhores indivíduos (menor distância) da população antiga
    substituindo os piores da nova.
    """
    # índices dos melhores da população antiga (menores distâncias)
    elite_indices = sorted(range(len(fitness)), key=lambda i: fitness[i])[:n_elite]

    elite = [populacao[i] for i in elite_indices]
    elite_fitness = [fitness[i] for i in elite_indices]

    # índices dos piores da nova população (maiores distâncias)
    piores_indices = sorted(
        range(len(fitness_nova_populacao)),
        key=lambda i: fitness_nova_populacao[i],
        reverse=True,
    )[:n_elite]

    for idx_pior, elite_ind, elite_fit in zip(piores_indices, elite, elite_fitness):
        nova_populacao[idx_pior] = elite_ind
        fitness_nova_populacao[idx_pior] = elite_fit

    return nova_populacao, fitness_nova_populacao

def rodar_algoritmo_genetico(tamanho_populacao, tamanho_torneio, taxa_crossover, taxa_mutacao, n_geracoes, n_elite):
    populacao = gerar_populacao(tamanho_populacao)
    historico_melhor = []  # Armazena o melhor fitness por geração

    for _ in range(n_geracoes):
        fitness = avaliar_populacao(populacao)
        historico_melhor.append(min(fitness))

        nova_populacao = []
        while len(nova_populacao) < tamanho_populacao:
            pai1 = selecao_torneio(fitness, populacao, tamanho_torneio)
            pai2 = selecao_torneio(fitness, populacao, tamanho_torneio)
            filho1, filho2 = order_crossover(pai1, pai2, taxa_crossover=taxa_crossover)
            filho1 = aplicar_mutacao_swap(filho1, taxa_mutacao)
            filho2 = aplicar_mutacao_swap(filho2, taxa_mutacao)
            nova_populacao.extend([filho1, filho2])

        nova_populacao = nova_populacao[:tamanho_populacao]
        fitness_nova_populacao = avaliar_populacao(nova_populacao)
        nova_populacao, fitness_nova_populacao = elitismo(populacao, fitness, nova_populacao, fitness_nova_populacao, n_elite)
        populacao = nova_populacao

    fitness_final = avaliar_populacao(populacao)
    melhor_final = min(fitness_final)
    return melhor_final, historico_melhor

def experimento(tamanho_populacao=50, tamanho_torneio=3, n_geracoes=400, n_execucoes=30, taxa_crossover=0.9, taxa_mutacao=0.05, n_elite=5):
    resultados = []
    dados_convergencia = []


    melhores = []
    print(f"\nExecutando Experimento")
    inicio = time.perf_counter()
    for _ in range(n_execucoes):
            
        melhor_final, historico = rodar_algoritmo_genetico(
            tamanho_populacao, tamanho_torneio, taxa_crossover, taxa_mutacao, n_geracoes, n_elite
        )
            
        melhores.append(melhor_final)

        # Armazena para o gráfico de convergência
        for g, fit in enumerate(historico):
            dados_convergencia.append({"geracao": g, "melhor_fitness": fit})

    fim = time.perf_counter()
    execucao = round(fim - inicio, 2)
    resultados.append({ "Tempo de execução": f"{execucao}s", "melhor": min(melhores), "média": sum(melhores) / len(melhores), "desvio de padrão": round(float(numpy.std(melhores)), 2) })

    return dados_convergencia, resultados, melhores, execucao


# === Execução principal ===
if __name__ == "__main__":
    
    dados_convergencia, res, melhores, execucao = experimento(
        tamanho_populacao=50,
        tamanho_torneio=3,
        n_geracoes=400,
        n_execucoes=30,
        taxa_crossover=0.9,
        taxa_mutacao=0.05,
        n_elite=5
    )
        
    # Printa resultados
    for res in res:
        print(res, "\n")
        
    df_conv = pd.DataFrame(dados_convergencia)
    
    # === Gráfico de convergência ===
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_conv, x="geracao", y="melhor_fitness")
    plt.title("Convergência do Algoritmo Genético")
    plt.xlabel("Geração")
    plt.ylabel("Melhor Fitness")
    plt.grid(True)
    plt.show()

    # === Boxplot comparando configurações ===
    plt.figure(figsize=(6, 4))
    plt.boxplot(melhores, vert=True, patch_artist=True,
                boxprops=dict(facecolor='lightblue', color='black'),
                medianprops=dict(color='red', linewidth=2),
                whiskerprops=dict(color='black'),
                capprops=dict(color='black'))

    plt.title("Distribuição dos resultados finais do AG - TSP")
    plt.ylabel("Distância total (menor é melhor)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()