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

# === Execução principal ===
if __name__ == "__main__":
    populacao = gerar_populacao(tamanho_populacao=50)
    for individuo in populacao:
        print(individuo, "\n")
        print(calculate_distance(individuo), "\n")
