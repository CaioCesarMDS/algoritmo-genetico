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

# === Execução principal ===
if __name__ == "__main__":
    populacao = gerar_populacao(tamanho_populacao=50)

    avaliacao = [calculate_distance(individuo) for individuo in populacao]

    vencedor = selecao_torneio(avaliacao, populacao, tamanho_torneio=3)

    print("Indivíduo vencedor do torneio:", vencedor)
    print("Distância do vencedor:", calculate_distance(vencedor))
    print("swap mutation aplicado:", aplicar_mutacao_swap(vencedor, taxa_mutacao=0.05))
