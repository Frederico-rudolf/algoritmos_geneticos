"""Trabalho 2: caixeiro-viajante com algoritmo genético, explicado por etapas."""

import argparse
from pathlib import Path

import math
import random
import webbrowser
from xml.etree import ElementTree as ET


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
        random.sample(range(1, numero_cidades + 1), numero_cidades)
        for _ in range(tamanho_populacao)
    ]


# Etapa 3: preservar a melhor metade e sortear pais por roleta.
def selecionar_melhores(populacao, custos):
    indices = sorted(range(len(custos)), key=lambda i: custos[i])[:len(populacao) // 2]
    melhores = [populacao[i].copy() for i in indices]
    return melhores, [custos[i] for i in indices]


def selecionar_pais(melhores):
    # Pesos inversos à posição: 10, 9, ..., 1 para dez sobreviventes.
    pesos = list(range(len(melhores), 0, -1))
    pai1, pai2 = random.choices(melhores, weights=pesos, k=2)
    return pai1.copy(), pai2.copy()


# Etapa 4: trocar um ciclo de posições mantém os filhos como permutações.
def crossover_cycle(pai1, pai2):
    filho1, filho2 = pai1.copy(), pai2.copy()
    inicio = random.randrange(len(pai1))
    posicao = inicio
    while True:
        filho1[posicao] = pai2[posicao]
        filho2[posicao] = pai1[posicao]
        cidade = pai2[posicao]
        posicao = pai1.index(cidade)
        if posicao == inicio:
            break
    return filho1, filho2


# Etapa 5: trocar duas posições distintas sem repetir cidades.
def aplicar_mutacao(rota):
    nova_rota = rota.copy()
    a, b = random.sample(range(len(nova_rota)), 2)
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
def executar(x, y, numero_geracoes=10000, tamanho_populacao=20):
    populacao = criar_populacao(tamanho_populacao, len(x))
    verificar_populacao(populacao, tamanho_populacao, len(x))
    inicial = [rota.copy() for rota in populacao]
    custos = calcular_distancias(populacao, x, y)
    indice = min(range(len(custos)), key=lambda i: custos[i])
    melhor_solucao, melhor_custo = populacao[indice].copy(), custos[indice]
    for geracao in range(numero_geracoes):
        populacao = criar_nova_geracao(populacao, custos)
        verificar_populacao(populacao, tamanho_populacao, len(x))
        custos = calcular_distancias(populacao, x, y)
        indice = min(range(len(custos)), key=lambda i: custos[i])
        if custos[indice] < melhor_custo:
            melhor_solucao = populacao[indice].copy()
            melhor_custo = custos[indice]
        if (geracao + 1) % 1000 == 0:
            print(f'Geração {geracao + 1}: melhor custo = {melhor_custo:.6f}')
    return inicial, populacao, melhor_solucao, melhor_custo


# Leitura do arquivo de texto do Octave, ignorando comentários e linhas vazias.
def carregar_cidades(arquivo):
    linhas = []
    for linha in Path(arquivo).read_text(encoding='utf-8').splitlines():
        numeros = linha.split('#', 1)[0].strip()
        if numeros:
            linhas.append([float(valor) for valor in numeros.split()])
    if len(linhas) != 2 or any(len(linha) != 20 for linha in linhas):
        raise ValueError('O arquivo deve conter duas linhas com 20 coordenadas.')
    if any(not math.isfinite(valor) or not 0 <= valor <= 1
           for linha in linhas for valor in linha):
        raise ValueError('As coordenadas devem ser finitas e estar entre 0 e 1.')
    return linhas[0], linhas[1]


# Etapa 7: gerar um gráfico SVG usando somente a biblioteca padrão.
def desenhar_caminho(x, y, solucao, custo, arquivo, mostrar=True):
    arquivo = Path(arquivo)
    if arquivo.suffix.lower() != '.svg':
        raise ValueError('O gráfico deve ser salvo com extensão .svg.')
    # Mesma escala nos dois eixos; y é invertido na tela.
    def ponto(cidade):
        indice = cidade - 1
        return 70 + 600 * x[indice], 670 - 600 * y[indice]

    raiz = ET.Element('svg', xmlns='http://www.w3.org/2000/svg',
                      width='760', height='760', viewBox='0 0 760 760')

    def elemento(tipo, **atributos):
        return ET.SubElement(raiz, tipo, {k: str(v) for k, v in atributos.items()})

    elemento('rect', width=760, height=760, fill='white')
    elemento('title').text = f'Melhor caminho encontrado — custo: {custo:.6f}'
    elemento('text', x=70, y=30, **{'font-size': 20}).text = (
        f'Melhor caminho encontrado — custo: {custo:.6f}'
    )
    for i in range(11):
        posicao = 70 + 60 * i
        elemento('line', x1=posicao, y1=70, x2=posicao, y2=670, stroke='#ddd')
        elemento('line', x1=70, y1=posicao, x2=670, y2=posicao, stroke='#ddd')
        elemento('text', x=posicao - 10, y=690).text = f'{i / 10:.1f}'
        elemento('text', x=35, y=posicao + 5).text = f'{1 - i / 10:.1f}'
    elemento('text', x=320, y=720).text = 'Coordenada x'
    elemento('text', x=10, y=55).text = 'y'
    # Repete a primeira cidade para fechar o percurso.
    rota_fechada = solucao + [solucao[0]]
    pontos = ' '.join(f'{px},{py}' for px, py in map(ponto, rota_fechada))
    elemento('polyline', points=pontos, fill='none', stroke='blue',
             **{'stroke-width': 2})
    for cidade in range(1, len(x) + 1):
        px, py = ponto(cidade)
        elemento('circle', cx=px, cy=py, r=5, fill='red')
        elemento('text', x=px + 7, y=py - 7).text = str(cidade)
    px, py = ponto(solucao[0])
    elemento('circle', cx=px, cy=py, r=8, fill='none', stroke='green',
             **{'stroke-width': 3})
    elemento('text', x=70, y=745).text = (
        'Azul: percurso | Vermelho: cidades | Verde: início e fim'
    )
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(raiz).write(arquivo, encoding='utf-8', xml_declaration=True)
    if mostrar:
        # Se o navegador não abrir, o SVG continua disponível na pasta resultados.
        webbrowser.open(arquivo.resolve().as_uri())


def main(argumentos=None):
    pasta = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cidades', type=Path, default=pasta / 'cidades.mat')
    parser.add_argument('--geracoes', type=int, default=10000)
    parser.add_argument('--seed', type=int, help='Semente opcional para repetir o experimento.')
    parser.add_argument('--sem-janela', action='store_true', help='Salva o gráfico sem abrir janela.')
    parser.add_argument('--salvar', type=Path, default=pasta / 'resultados' / 'melhor_caminho.svg')
    args = parser.parse_args(argumentos)
    if args.geracoes < 1:
        parser.error('--geracoes deve ser positivo.')
    if args.seed is not None:
        random.seed(args.seed)
    if args.salvar.suffix.lower() != '.svg':
        parser.error('--salvar deve usar a extensão .svg.')
    try:
        x, y = carregar_cidades(args.cidades)
    except (OSError, ValueError) as erro:
        parser.error(str(erro))
    inicial, final, solucao, custo = executar(x, y, args.geracoes)
    print('\nTamanho da população:', len(inicial))
    print('Número de cidades:', len(x))
    for titulo, populacao in [('População inicial', inicial), ('População final', final)]:
        print(f'\n{titulo}:')
        for i, rota in enumerate(populacao, start=1):
            print(f'Indivíduo {i}: {rota}')
    print(f'\nMelhor custo: {custo:.6f}')
    print('Melhor solução:', solucao)
    desenhar_caminho(x, y, solucao, custo, args.salvar, mostrar=not args.sem_janela)
    print('Gráfico salvo em:', args.salvar)


if __name__ == '__main__':
    main()
