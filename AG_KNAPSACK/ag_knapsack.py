import random
from knapsack import knapsack

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
        fitness.append(knapsack(solucao))

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


if __name__ == "__main__":
    tamanho_populacao = 50
    n_itens = 20

    populacao = gerar_populacao(tamanho_populacao, n_itens)
    fitness = avaliar_populacao(populacao)

    print("População Inicial:")
    for individuo, fit in zip(populacao, fitness):
        print(f"Indivíduo: {individuo}, Fitness: {fit}")

    print("\nCrossover na População...\n")

    nova_populacao = []
    while len(nova_populacao) < tamanho_populacao:
        pai1 = selecao_torneio(fitness, populacao)
        pai2 = selecao_torneio(fitness, populacao)
        filho1, filho2 = aplicar_crossover(pai1, pai2, tipo="dois_pontos", taxa_crossover=0.8)
        nova_populacao.extend([filho1, filho2])

    fitness_nova_populacao = avaliar_populacao(nova_populacao)

    print("População Nova:")
    for individuo, fit in zip(nova_populacao, fitness_nova_populacao):
        print(f"Indivíduo: {individuo}, Fitness: {fit}")
