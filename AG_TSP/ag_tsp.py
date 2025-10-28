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

# === Execução principal ===
if __name__ == "__main__":
    populacao = gerar_populacao(tamanho_populacao=50)
    for individuo in populacao:
        print(individuo, "\n")
        print(calculate_distance(individuo), "\n")
