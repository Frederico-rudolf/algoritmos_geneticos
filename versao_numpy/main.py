"""Versão separada do Trabalho 2 com NumPy e gráficos usando plt.plot."""

import argparse
from pathlib import Path

import numpy as np


# Etapa 1: calcular o custo, incluindo o retorno à primeira cidade.
def calcular_distancias(populacao, x, y):
    distancias = []
    for rota in populacao:
        distancia_total = 0.0
        for i in range(len(rota)):
            atual = rota[i] - 1
            proxima = rota[(i + 1) % len(rota)] - 1
            distancia_total += (
                (x[atual] - x[proxima]) ** 2
                + (y[atual] - y[proxima]) ** 2
            ) ** 0.5
        distancias.append(distancia_total)
    return distancias


# Etapa 2: cada indivíduo é uma permutação das cidades.
def criar_populacao(tamanho_populacao, numero_cidades):
    return [
        np.random.permutation(np.arange(1, numero_cidades + 1))
        for _ in range(tamanho_populacao)
    ]


# Etapa 3: preservar a melhor metade e sortear pais por roleta.
def selecionar_melhores(populacao, custos):
    indices = np.argsort(custos)[:len(populacao) // 2]
    melhores = [populacao[i].copy() for i in indices]
    return melhores, [custos[i] for i in indices]


def selecionar_pais(melhores):
    # Pesos inversos à posição: 10, 9, ..., 1 para dez sobreviventes.
    pesos = np.arange(len(melhores), 0, -1)
    probabilidades = pesos / pesos.sum()
    indices = np.random.choice(len(melhores), size=2, p=probabilidades)
    return melhores[indices[0]].copy(), melhores[indices[1]].copy()


# Etapa 4: trocar um ciclo de posições mantém os filhos como permutações.
def crossover_cycle(pai1, pai2):
    filho1, filho2 = pai1.copy(), pai2.copy()
    inicio = np.random.randint(len(pai1))
    posicao = inicio
    while True:
        filho1[posicao] = pai2[posicao]
        filho2[posicao] = pai1[posicao]
        cidade = pai2[posicao]
        posicao = np.where(pai1 == cidade)[0][0]
        if posicao == inicio:
            break
    return filho1, filho2


# Etapa 5: trocar duas posições distintas sem repetir cidades.
def aplicar_mutacao(rota):
    nova_rota = rota.copy()
    a, b = np.random.choice(len(nova_rota), size=2, replace=False)
    nova_rota[a], nova_rota[b] = nova_rota[b], nova_rota[a]
    return nova_rota


def criar_nova_geracao(populacao, custos):
    melhores, _ = selecionar_melhores(populacao, custos)
    nova_populacao = [rota.copy() for rota in melhores]
    while len(nova_populacao) < len(populacao):
        pai1, pai2 = selecionar_pais(melhores)
        filho1, filho2 = crossover_cycle(pai1, pai2)
        nova_populacao.append(filho1)
        if len(nova_populacao) < len(populacao):
            nova_populacao.append(filho2)
    # O enunciado pede mutação em todos, inclusive os sobreviventes.
    return [aplicar_mutacao(rota) for rota in nova_populacao]


# Etapa 8: verificar se todas as cidades aparecem exatamente uma vez.
def verificar_populacao(populacao, tamanho_esperado, numero_cidades):
    if len(populacao) != tamanho_esperado:
        raise ValueError('A população está com tamanho incorreto.')
    esperadas = list(range(1, numero_cidades + 1))
    for i, rota in enumerate(populacao):
        if sorted(rota) != esperadas:
            raise ValueError(f'A rota {i + 1} tem cidades repetidas ou ausentes.')


# Etapa 6: repetir as gerações e guardar o melhor resultado de toda a busca.
def executar(x, y, numero_geracoes=10000, tamanho_populacao=20, historico=None):
    populacao = criar_populacao(tamanho_populacao, len(x))
    verificar_populacao(populacao, tamanho_populacao, len(x))
    inicial = [rota.copy() for rota in populacao]
    custos = calcular_distancias(populacao, x, y)
    indice = np.argmin(custos)
    melhor_solucao, melhor_custo = populacao[indice].copy(), custos[indice]
    # Inclui o melhor custo da população inicial, na geração zero.
    if historico is not None:
        historico.clear()
        historico.append(melhor_custo)
    for geracao in range(numero_geracoes):
        populacao = criar_nova_geracao(populacao, custos)
        verificar_populacao(populacao, tamanho_populacao, len(x))
        custos = calcular_distancias(populacao, x, y)
        indice = np.argmin(custos)
        if custos[indice] < melhor_custo:
            melhor_solucao = populacao[indice].copy()
            melhor_custo = custos[indice]
        if historico is not None:
            historico.append(melhor_custo)
        if (geracao + 1) % 1000 == 0:
            print(f'Geração {geracao + 1}: melhor custo = {melhor_custo:.6f}')
    return inicial, populacao, melhor_solucao, melhor_custo


# Etapa 7: usar literalmente plt.plot nos dois gráficos.
def desenhar_graficos(x, y, solucao, custo, historico, pasta, mostrar=True):
    import matplotlib.pyplot as plt

    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    # O último ponto repete a primeira cidade para fechar o percurso.
    indices = np.append(solucao - 1, solucao[0] - 1)
    figura_caminho = plt.figure(figsize=(8, 8))
    plt.plot(x[indices], y[indices], color='blue', linewidth=1,
             label='Melhor caminho')
    plt.scatter(x, y, color='red', s=50, label='Cidades')
    for i in range(len(x)):
        plt.annotate(str(i + 1), (x[i], y[i]), xytext=(5, 5),
                     textcoords='offset points')
    inicio = solucao[0] - 1
    plt.scatter(x[inicio], y[inicio], color='green', s=120, marker='*',
                label='Início e fim', zorder=3)
    plt.title(f'Melhor caminho encontrado — custo: {custo:.6f}')
    plt.xlabel('Coordenada x')
    plt.ylabel('Coordenada y')
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    figura_caminho.savefig(pasta / 'melhor_caminho.svg')

    figura_custo = plt.figure(figsize=(9, 5))
    geracoes = np.arange(len(historico))
    plt.plot(geracoes, historico, color='blue', label='Melhor custo histórico')
    plt.scatter(geracoes[-1], historico[-1], color='green', zorder=3)
    plt.title(f'Evolução do melhor custo — final: {custo:.6f}')
    plt.xlabel('Geração')
    plt.ylabel('Melhor distância total encontrada')
    plt.ylim(bottom=0)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    figura_custo.savefig(pasta / 'melhor_custo.svg')
    if mostrar:
        plt.show()
    plt.close(figura_caminho)
    plt.close(figura_custo)


def main(argumentos=None):
    pasta = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cidades', type=Path, default=pasta.parent / 'cidades.mat')
    parser.add_argument('--geracoes', type=int, default=10000)
    parser.add_argument('--seed', type=int, help='Semente opcional para repetir o experimento.')
    parser.add_argument('--sem-janela', action='store_true', help='Salva o gráfico sem abrir janela.')
    parser.add_argument('--saida', type=Path, default=pasta / 'resultados',
                        help='Pasta onde serão salvos os dois gráficos SVG.')
    args = parser.parse_args(argumentos)
    if args.geracoes < 1:
        parser.error('--geracoes deve ser positivo.')
    if args.seed is not None:
        np.random.seed(args.seed)
    # O arquivo fornecido é texto do Octave; comentários começam com #.
    try:
        coordenadas = np.loadtxt(args.cidades)
    except (OSError, ValueError) as erro:
        parser.error(str(erro))
    if (coordenadas.shape != (2, 20) or not np.isfinite(coordenadas).all()
            or np.any(coordenadas < 0) or np.any(coordenadas > 1)):
        parser.error('O arquivo deve conter duas linhas com 20 coordenadas entre 0 e 1.')
    x, y = coordenadas
    historico = []
    inicial, final, solucao, custo = executar(x, y, args.geracoes, historico=historico)
    print('\nTamanho da população:', len(inicial))
    print('Número de cidades:', len(x))
    for titulo, populacao in [('População inicial', inicial), ('População final', final)]:
        print(f'\n{titulo}:')
        for i, rota in enumerate(populacao, start=1):
            print(f'Indivíduo {i}: {rota.tolist()}')
    print(f'\nMelhor custo: {custo:.6f}')
    print('Melhor solução:', solucao.tolist())
    desenhar_graficos(x, y, solucao, custo, historico, args.saida,
                      mostrar=not args.sem_janela)
    print('Gráfico do caminho:', args.saida / 'melhor_caminho.svg')
    print('Gráfico do custo:', args.saida / 'melhor_custo.svg')


if __name__ == '__main__':
    main()
