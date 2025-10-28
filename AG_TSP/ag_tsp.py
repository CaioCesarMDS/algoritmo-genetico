import random
from TSP_13_cities.tsp_utils import calculate_distance

def gerar_populacao(tamanho_populacao):
    # Gera uma população inicial aleatória
    populacao = []
    ex_route = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    for _ in range(tamanho_populacao):
        individuo = random.sample(ex_route, len(ex_route))
        populacao.append(individuo)
    return populacao

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

    return populacao[vencedor], competidores

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

# === Execução principal ===
if __name__ == "__main__":
    populacao = gerar_populacao(tamanho_populacao=50)

    avaliacao = [calculate_distance(individuo) for individuo in populacao]

    vencedor = selecao_torneio(avaliacao, populacao, tamanho_torneio=3)

    print("Indivíduo vencedor do torneio:", vencedor)
    print("Distância do vencedor:", calculate_distance(vencedor))
