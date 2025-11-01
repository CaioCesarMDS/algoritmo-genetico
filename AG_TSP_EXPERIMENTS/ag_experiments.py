from AG_TSP.ag_tsp import experimento
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#  Experimento 1: Tamanho da População

dados_convergencia_20indv, res_20indv, melhores_20indv, execucao = experimento(
    tamanho_populacao=20,
    tamanho_torneio=3,
    n_geracoes=400,
    n_execucoes=30,
    taxa_crossover=0.9,
    taxa_mutacao=0.05,
    n_elite=5
)

dados_convergencia_50indv, res_50indv, melhores_50indv, execucao = experimento(
    tamanho_populacao=50,
    tamanho_torneio=3,
    n_geracoes=400,
    n_execucoes=30,
    taxa_crossover=0.9,
    taxa_mutacao=0.05,
    n_elite=5
)

dados_convergencia_100indv, res_100indv, melhores_100indv, execucao = experimento(
    tamanho_populacao=100,
    tamanho_torneio=3,
    n_geracoes=400,
    n_execucoes=30,
    taxa_crossover=0.9,
    taxa_mutacao=0.05,
    n_elite=5
)
        
# Fazer blotplox comparativo    



# Experimento 2: Taxa de Mutação

dados_convergencia_mut1, res_mut1, melhores_mut1 = experimento(
    tamanho_populacao=50,
    tamanho_torneio=3,
    n_geracoes=400,
    n_execucoes=30,
    taxa_crossover=0.9,
    taxa_mutacao=0.01,
    n_elite=5
)

dados_convergencia_mut5, res_mut5, melhores_mut5 = experimento(
    tamanho_populacao=50,
    tamanho_torneio=3,
    n_geracoes=400,
    n_execucoes=30,
    taxa_crossover=0.9,
    taxa_mutacao=0.05,
    n_elite=5
)

dados_convergencia_mut10, res_mut10, melhores_mut10 = experimento(
    tamanho_populacao=50,
    tamanho_torneio=3,
    n_geracoes=400,
    n_execucoes=30,
    taxa_crossover=0.9,
    taxa_mutacao=0.1,
    n_elite=5
)

dados_convergencia_mut20, res_mut20, melhores_mut20 = experimento(
    tamanho_populacao=50,
    tamanho_torneio=3,
    n_geracoes=400,
    n_execucoes=30,
    taxa_crossover=0.9,
    taxa_mutacao=0.2,
    n_elite=5
)

# Fazer blotplox comparativo    



# Experimento 3: Tamanho do Torneio

dados_convergencia_torneio2, res_torneio2, melhores_torneio2 = experimento(
    tamanho_populacao=50,
    tamanho_torneio=2,
    n_geracoes=400,
    n_execucoes=30,
    taxa_crossover=0.9,
    taxa_mutacao=0.05,
    n_elite=5
)

dados_convergencia_torneio3, res_torneio3, melhores_torneio3 = experimento(
    tamanho_populacao=50,
    tamanho_torneio=3,
    n_geracoes=400,
    n_execucoes=30,
    taxa_crossover=0.9,
    taxa_mutacao=0.05,
    n_elite=5
)

dados_convergencia_torneio5, res_torneio5, melhores_torneio5 = experimento(
    tamanho_populacao=50,
    tamanho_torneio=5,
    n_geracoes=400,
    n_execucoes=30,
    taxa_crossover=0.9,
    taxa_mutacao=0.05,
    n_elite=5
)

dados_convergencia_torneio7, res_torneio7, melhores_torneio7 = experimento(
    tamanho_populacao=50,
    tamanho_torneio=7,
    n_geracoes=400,
    n_execucoes=30,
    taxa_crossover=0.9,
    taxa_mutacao=0.05,
    n_elite=5
)

# Fazer blotplox comparativo    



# Experimento 4: Elitismo

dados_convergencia_elite0, res_elite0, melhores_elite0 = experimento(
    tamanho_populacao=50,
    tamanho_torneio=3,
    n_geracoes=400,
    n_execucoes=30,
    taxa_crossover=0.9,
    taxa_mutacao=0.05,
    n_elite=0
)

dados_convergencia_elite0, res_elite0, melhores_elite0 = experimento(
    tamanho_populacao=50,
    tamanho_torneio=3,
    n_geracoes=400,
    n_execucoes=30,
    taxa_crossover=0.9,
    taxa_mutacao=0.05,
    n_elite=1
)

dados_convergencia_elite0, res_elite0, melhores_elite0 = experimento(
    tamanho_populacao=50,
    tamanho_torneio=3,
    n_geracoes=400,
    n_execucoes=30,
    taxa_crossover=0.9,
    taxa_mutacao=0.05,
    n_elite=5
)

dados_convergencia_elite0, res_elite0, melhores_elite0 = experimento(
    tamanho_populacao=50,
    tamanho_torneio=3,
    n_geracoes=400,
    n_execucoes=30,
    taxa_crossover=0.9,
    taxa_mutacao=0.05,
    n_elite=10
)


# Fazer blotplox comparativo    