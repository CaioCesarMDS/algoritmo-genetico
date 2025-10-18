import random
from knapsack import knapsack

def gerar_populacao(tamanho_populacao, n_itens):
    # Gera uma população inicial aleatória
    populacao = []
    for _ in range(tamanho_populacao):
        individuo = [int(random.random() > 0.8) for _ in range(n_itens)]
        populacao.append(individuo)
    return populacao

def gerar_vizinhos(solucao, n_vizinhos=50, flips_por_vizinho=2):
    vizinhos = []
    n_itens = len(solucao)

    for _ in range(n_vizinhos):
        vizinho = solucao.copy()
        posicoes = random.sample(range(n_itens), flips_por_vizinho)
        for pos in posicoes:
            vizinho[pos] = 1 - vizinho[pos]
        vizinhos.append(vizinho)

    return vizinhos

def avaliar_populacao(populacao):
    fitness = []

    for solucao in populacao:
        fitness.append(knapsack(solucao))

    return fitness

def selecao_torneio(avaliacao):
    for competidor in avaliacao:
        print(competidor, "\n")

if __name__ == "__main__":
    tamanho_populacao = 50
    n_itens = 20

    populacao = gerar_populacao(tamanho_populacao, n_itens)
    fitness = avaliar_populacao(populacao)
    print("=== AVALIAÇÃO (FITNESS) DA POPULAÇÃO INICIAL ===\n")
    print(fitness)
    print("\n===============================================\n")

    # torneio(avaliacao_populacao)
    # fitness = lambda solucao_inicial: knapsack(solucao_inicial, 20)

