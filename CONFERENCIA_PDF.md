# Conferência do Trabalho 2

| Requisito do PDF | Implementação |
| --- | --- |
| 20 cidades em um plano de 0 a 1 | `cidades.mat`, com as coordenadas fornecidas; não são sorteadas novamente |
| Cromossomos com inteiros de 1 a 20, sem repetições | `criar_populacao` e `verificar_populacao` |
| Visitar cada cidade uma vez e retornar à origem | `calcular_distancias`, com índice circular |
| Distância euclidiana simétrica e minimização do custo | `calcular_distancias` |
| População com 20 indivíduos | Padrão de `executar` e execução principal |
| 10.000 iterações | Padrão da linha de comando e do notebook |
| Manter metade e gerar a outra metade | `criar_nova_geracao`: 10 sobreviventes e 10 filhos |
| Ordenar do mais apto ao menos apto | `selecionar_melhores`, por custo crescente |
| Probabilidades inversamente distribuídas e roleta | `selecionar_pais`: pesos por ranking, de 10 a 1 |
| Recombinação cycle iniciada em posição aleatória | `crossover_cycle`, validado com a figura do PDF |
| Mutação por troca de dois números em cada membro da nova geração | `aplicar_mutacao`, incluindo os sobreviventes |
| Mostrar tamanho da população, população inicial e final, número de cidades, melhor custo e solução | Saída do programa e célula de resultados do notebook |
| Plotar cidades e melhor caminho | `desenhar_caminho`, com retorno desenhado e cidades numeradas em SVG; substitui a biblioteca de plotagem conforme solicitado pelo usuário |
| Código com comentários simples | Funções organizadas e comentadas por etapas em `main.py` |
| Entrega em ZIP ou notebook e identificação dos integrantes | `Trabalho_2.ipynb`; preencher os nomes antes de entregar |

## Interpretação adotada

O enunciado não apresenta uma fórmula explícita das probabilidades da roleta. Foi mantida a interpretação explicada durante o desenvolvimento: pesos inversos à posição no ranking, com probabilidade 10/55 para o melhor sobrevivente e 1/55 para o último. Se a disciplina exigir especificamente o inverso da distância, essa fórmula precisa ser ajustada.

A mutação afeta todos os membros, como solicitado. Por isso, guardamos uma cópia separada do melhor resultado histórico. As cidades não precisam começar em 1 na lista: cada rota é um ciclo e retorna à própria origem.

## Validação realizada

- Sete testes automatizados passaram: leitura das coordenadas e validação do SVG com caminho fechado, retorno à origem, exemplo de crossover do PDF, troca de duas posições, preservação das permutações, coerência do melhor histórico e rejeição de rota inválida.
- Execução de 10.000 gerações com semente 42 concluída: melhor custo **4.147863**.
- As quatro células de código do notebook foram executadas em ordem em um namespace novo, salvando resultados e gráfico no arquivo. Essa validação não utilizou um servidor Jupyter.
- Todas as gerações tiveram as 20 rotas verificadas quanto a cidades ausentes ou repetidas.
- O resultado é heurístico; não há comprovação de ótimo global.

A única informação de entrega que depende do aluno é o preenchimento dos nomes dos integrantes e, se necessário, a renomeação do arquivo conforme a turma.

## Versão sem dependências externas

NumPy e Matplotlib foram removidos a pedido do usuário. Listas e `random` implementam o algoritmo; o gráfico SVG é gerado com a biblioteca padrão e pode ser aberto no navegador. Testes, execução completa e células do notebook foram executados com `python -S`, que desativa o carregamento de pacotes de terceiros. A semente 42 agora usa o gerador da biblioteca padrão e produz resultados diferentes da versão anterior. A interface Jupyter é opcional, não é necessária para executar `main.py`.
