# 🧬 Como funciona o ciclo de gerações (estrutura correta do AG)

- Inicialização

    - Gera a população inicial aleatória (50 indivíduos binários com 20 genes cada).

- Avaliação (Fitness)

    - Calcula o valor (fitness) de cada indivíduo com base no problema da mochila:

    - Soma dos valores dos itens escolhidos;

    - Penaliza ou invalida soluções que ultrapassem o peso limite.

- Seleção

  - Aplica o torneio de tamanho 3:

  - Escolhe 3 indivíduos aleatórios;

  - O que tiver maior fitness vence e é selecionado como pai/mãe.

- Crossover

    - Aplica o tipo de crossover definido (um ponto, dois pontos ou uniforme) em 80% dos pares selecionados.

    - Isso gera novos filhos (novos indivíduos).

- Mutação

    - Aplica a mutação bit-flip (2%) aos filhos — inverte aleatoriamente alguns bits (0→1 ou 1→0).

- Elitismo

    - Copia os 2 melhores indivíduos da geração anterior diretamente para a nova geração (sem alterações).

- Substituição

    - A nova população (com filhos + elite) substitui a anterior.

- Repetição

    - Esse ciclo se repete até completar 500 gerações.
