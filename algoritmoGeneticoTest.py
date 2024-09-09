import random
import time
import statistics
import algoritmoGenetico as ag

# Função principal do algoritmo genético
def algoritmo_genetico():
    tamanho_populacao = 20
    taxa_cruzamento = 0.8
    taxa_mutacao = 0.03
    max_geracoes = 1000
    populacao = ag.gerar_populacao(tamanho_populacao)

    for geracao in range(max_geracoes):
        fitnesses = [1 / (1 + ag.calcular_fitness(ag.binario_para_tabuleiro(individuo))) for individuo in populacao]
        melhor_individuo, melhor_fitness = ag.encontrar_melhor_individuo(populacao)
        if melhor_fitness == 0:
            return geracao  # Retorna o número de gerações quando a solução é encontrada

        nova_populacao = []
        nova_populacao.append(melhor_individuo)
        while len(nova_populacao) < tamanho_populacao:
            pai1, pai2 = ag.selecionar_pais(populacao, fitnesses)
            if random.random() < taxa_cruzamento:
                filho1, filho2 = ag.cruzamento(pai1, pai2)
            else:
                filho1, filho2 = pai1[:], pai2[:]
            filho1 = ag.mutacao(filho1, taxa_mutacao)
            filho2 = ag.mutacao(filho2, taxa_mutacao)
            nova_populacao.extend([filho1, filho2])
        populacao = nova_populacao[:tamanho_populacao]

    return max_geracoes  # Se a solução não for encontrada, retorna o número máximo de gerações


# Executa o algoritmo genético 50 vezes
num_execucoes = 50
geracoes_lista = []
tempos_lista = []

for _ in range(num_execucoes):
    inicio = time.time()  # Marca o tempo de início
    geracoes = algoritmo_genetico()
    fim = time.time()  # Marca o tempo de término
    tempo_execucao = fim - inicio

    geracoes_lista.append(geracoes)
    tempos_lista.append(tempo_execucao)

# Calcula a média e o desvio padrão do número de gerações
media_geracoes = statistics.mean(geracoes_lista)
desvio_padrao_geracoes = statistics.stdev(geracoes_lista)

# Calcula a média e o desvio padrão do tempo de execução
media_tempo = statistics.mean(tempos_lista)
desvio_padrao_tempo = statistics.stdev(tempos_lista)

print(f"Média de gerações: {media_geracoes}")
print(f"Desvio padrão de gerações: {desvio_padrao_geracoes}")
print(f"Média de tempo de execução: {media_tempo:.4f} segundos")
print(f"Desvio padrão de tempo de execução: {desvio_padrao_tempo:.4f} segundos")
