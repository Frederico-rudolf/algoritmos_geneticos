# Versão com NumPy e Matplotlib

Esta versão é independente da versão `main.py` na raiz. Usa NumPy nas populações, na seleção, no crossover e na leitura das coordenadas. Usa **`plt.plot`** nos gráficos do caminho e da evolução do custo, atendendo ao pedido de usar plotagem do enunciado.

## Executar a partir da raiz do repositório

Requer Python 3.11 ou superior (recomendado: Python 3.12).

```bash
python -m pip install -r versao_numpy/requirements.txt
python versao_numpy/main.py
```

No Windows, instale o Python e marque **Add python.exe to PATH** caso o comando não seja encontrado. A instalação de pacotes usa o mesmo interpretador que executa o programa.

O programa abre as duas figuras e salva os arquivos em:

- `versao_numpy/resultados/melhor_caminho.svg`
- `versao_numpy/resultados/melhor_custo.svg`

O arquivo de cidades é o `cidades.mat` na raiz do repositório, encontrado automaticamente, independentemente da pasta de onde você executar o script. Para entregar esta versão, inclua esse arquivo junto com a pasta `versao_numpy`, preservando essa estrutura.

## Experimento reproduzível sem abrir janelas

```bash
python versao_numpy/main.py --seed 42 --sem-janela
```

O padrão é população 20 e 10.000 gerações. Para teste rápido, acrescente `--geracoes 100`. Para mudar a pasta dos gráficos, use `--saida outra_pasta`.

As funções são comentadas por etapas, como na versão sem dependências. A roleta usa pesos por ranking de 10 a 1; a mutação afeta todos os indivíduos; uma cópia separada guarda o melhor resultado histórico. O custo inclui o retorno à origem. O gráfico de custo inclui a geração zero. A semente do NumPy produz uma sequência diferente daquela do módulo `random` na outra versão.

Nenhum dos métodos garante encontrar o ótimo global. Preencha os nomes dos integrantes antes da entrega.
