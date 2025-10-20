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


def selecao_torneio(avaliacao, populacao):
    vencedores = []
    combinacoes = []
    for i in range(len(avaliacao)):
        competidores = random.sample(avaliacao, 3)

        if combinacoes.__contains__(competidores):
            while True:
                competidores = random.sample(avaliacao, 3)
                if not combinacoes.__contains__(competidores):
                    break
        
        competidor1 = competidores[0]
        competidor2 = competidores[1]
        competidor3 = competidores[2]
        
        if competidor1 >= competidor2 and competidor1 >= competidor3:
            vencedores.append({"individuo": populacao[avaliacao.index(competidor1)], "fitness": competidor1})

        if competidor2 >= competidor1 and competidor2 >= competidor3:
            vencedores.append({"individuo": populacao[avaliacao.index(competidor2)], "fitness": competidor1})

        if competidor3 > competidor1 and competidor3 > competidor2:
            vencedores.append({"individuo": populacao[avaliacao.index(competidor3)], "fitness": competidor1})
    
    return vencedores


if __name__ == "__main__":
    tamanho_populacao = 50
    n_itens = 20

    populacao = gerar_populacao(tamanho_populacao, n_itens)
    fitness = avaliar_populacao(populacao)
    print("=== AVALIAÇÃO (FITNESS) DA POPULAÇÃO INICIAL ===\n")
    print(fitness)
    print("\n==TORNEIRO DE 3==\n")
    vencedores = selecao_torneio(fitness, populacao)
    
    for vencedor in vencedores:
        print(vencedor, "\n")

