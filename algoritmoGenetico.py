import random


# Função para converter um indivíduo binário para a representação do tabuleiro
def binario_para_tabuleiro(individuo_binario):
    tabuleiro = []
    for i in range(0, len(individuo_binario), 3):
        # Converte cada grupo de 3 bits em um número de 0 a 7 (posição da rainha em cada coluna)
        posicao_rainha = int(''.join(map(str, individuo_binario[i:i + 3])), 2)
        tabuleiro.append(posicao_rainha)
    return tabuleiro


# Função para calcular o fitness (quantidade de conflitos entre rainhas)
def calcular_fitness(tabuleiro):
    conflitos = 0
    n = len(tabuleiro)

    # Verifica conflitos entre pares de rainhas
    for i in range(n):
        for j in range(i + 1, n):
            if tabuleiro[i] == tabuleiro[j] or abs(tabuleiro[i] - tabuleiro[j]) == abs(i - j):
                conflitos += 1
    return conflitos


# Função para criar um indivíduo aleatório (24 bits)
def gerar_individuo():
    return [random.randint(0, 1) for _ in range(24)]


# Função para gerar a população inicial
def gerar_populacao(tamanho_populacao):
    return [gerar_individuo() for _ in range(tamanho_populacao)]


# Função de seleção por roleta
def selecionar_pais(populacao, fitnesses):
    total_fitness = sum(fitnesses)
    selecao = []
    for _ in range(2):  # Seleciona dois pais
        limite = random.uniform(0, total_fitness)
        acumulado = 0
        for i, fitness in enumerate(fitnesses):
            acumulado += fitness
            if acumulado >= limite:
                selecao.append(populacao[i])
                break
    return selecao


# Função de cruzamento por ponto de corte
def cruzamento(pai1, pai2):
    ponto_de_corte = random.randint(1, len(pai1) - 1)
    filho1 = pai1[:ponto_de_corte] + pai2[ponto_de_corte:]
    filho2 = pai2[:ponto_de_corte] + pai1[ponto_de_corte:]
    return filho1, filho2


# Função de mutação por bit flip
def mutacao(individuo, taxa_mutacao=0.03):
    for i in range(len(individuo)):
        if random.random() < taxa_mutacao:
            individuo[i] = 1 if individuo[i] == 0 else 0
    return individuo


# Função para encontrar o melhor indivíduo da população (com o menor número de conflitos)
def encontrar_melhor_individuo(populacao):
    melhor_individuo = populacao[0]
    melhor_fitness = calcular_fitness(binario_para_tabuleiro(melhor_individuo))
    for individuo in populacao[1:]:
        fitness_atual = calcular_fitness(binario_para_tabuleiro(individuo))
        if fitness_atual < melhor_fitness:
            melhor_fitness = fitness_atual
            melhor_individuo = individuo
    return melhor_individuo, melhor_fitness


# Função principal do algoritmo genético
def algoritmo_genetico():
    tamanho_populacao = 20
    taxa_cruzamento = 0.8
    taxa_mutacao = 0.03
    max_geracoes = 1000
    populacao = gerar_populacao(tamanho_populacao)

    for geracao in range(max_geracoes):
        # Avalia o fitness de cada indivíduo
        fitnesses = [1 / (1 + calcular_fitness(binario_para_tabuleiro(individuo))) for individuo in populacao]

        # Verifica se algum indivíduo tem fitness ótimo (solução encontrada)
        melhor_individuo, melhor_fitness = encontrar_melhor_individuo(populacao)
        if melhor_fitness == 0:
            print(f"Solução encontrada na geração {geracao}: {binario_para_tabuleiro(melhor_individuo)}")
            return binario_para_tabuleiro(melhor_individuo)

        # Nova população para a próxima geração
        nova_populacao = []

        # Elitismo: mantém o melhor indivíduo da geração anterior
        nova_populacao.append(melhor_individuo)

        # Realiza a seleção, cruzamento e mutação
        while len(nova_populacao) < tamanho_populacao:
            # Seleciona os pais usando a estratégia de roleta
            pai1, pai2 = selecionar_pais(populacao, fitnesses)

            # Executa o cruzamento com uma taxa de 80%
            if random.random() < taxa_cruzamento:
                filho1, filho2 = cruzamento(pai1, pai2)
            else:
                filho1, filho2 = pai1[:], pai2[:]

            # Aplica mutação nos filhos
            filho1 = mutacao(filho1, taxa_mutacao)
            filho2 = mutacao(filho2, taxa_mutacao)

            # Adiciona os filhos na nova população
            nova_populacao.extend([filho1, filho2])

        # Atualiza a população
        populacao = nova_populacao[:tamanho_populacao]

    # Se o critério de número máximo de gerações for atingido
    melhor_individuo, melhor_fitness = encontrar_melhor_individuo(populacao)
    print(
        f"Melhor solução encontrada após {max_geracoes} gerações: {binario_para_tabuleiro(melhor_individuo)} com {melhor_fitness} conflitos")
    return binario_para_tabuleiro(melhor_individuo)


# Executa o algoritmo genético
solucao = algoritmo_genetico()
for i in range(8):
    linha = ""
    for j in range(8):
        if solucao[j] == i:
            linha += "♛ "
        else:
            linha += ". "
    print(linha)
