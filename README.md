# Algoritmos genéticos — Trabalho 2

Implementação comentada do caixeiro-viajante com as 20 cidades fornecidas no trabalho. **Não precisa de NumPy, Matplotlib ou qualquer pacote externo.**

## Executar

Instale o Python 3.10 ou superior. No Windows, marque **Add python.exe to PATH** durante a instalação e reabra o terminal. Na pasta do projeto:

```bash
python main.py
```

Não é necessário executar `pip install`. O arquivo `requirements.txt` contém apenas um comentário, para compatibilidade com instruções antigas.

O programa imprime a população inicial e final, número de cidades, tamanho da população, melhor custo e melhor solução. Salva `resultados/melhor_caminho.svg` e tenta abri-lo no navegador. Se a abertura automática não funcionar, abra esse arquivo manualmente.

Para executar sem abrir o navegador e repetir o experimento:

```bash
python main.py --seed 42 --sem-janela
```

Para uma verificação rápida, acrescente `--geracoes 100`. A entrega utiliza o padrão de **10.000 gerações**. Para outro destino do gráfico, use `--salvar caminho/grafico.svg`.

## Etapas

1. Ler o texto do Octave em `cidades.mat`, ignorando comentários, e calcular distâncias com retorno à origem.
2. Gerar 20 permutações das 20 cidades com `random.sample`.
3. Manter as 10 melhores e selecionar pais pela roleta com `random.choices` e pesos de ranking 10 a 1.
4. Gerar filhos pelo crossover cycle, conforme o exemplo do enunciado.
5. Completar 20 indivíduos e mutar todos por troca de duas posições distintas.
6. Repetir por 10.000 gerações, verificando as rotas e guardando o melhor resultado histórico.
7. Mostrar os resultados e gerar o gráfico SVG com `xml.etree.ElementTree`, da biblioteca padrão.

Como a mutação inclui os sobreviventes, o melhor resultado histórico pode não estar na população final. O algoritmo é aleatório e não garante o ótimo global. A roleta usa pesos inversos à posição no ranking, não o inverso numérico da distância.

O gerador aleatório mudou em relação à versão NumPy: a mesma semente pode produzir um resultado diferente daquele da versão anterior.

## Notebook e entrega

`Trabalho_2.ipynb` acompanha as etapas e contém os resultados de uma execução. A interface Jupyter é opcional e instalada separadamente; o programa `main.py` funciona diretamente com Python. No notebook, o gráfico é salvo como SVG para abrir no navegador. Mantenha `main.py` e `cidades.mat` na mesma pasta. Preencha os nomes dos integrantes antes de entregar. Para ZIP, inclua notebook, script e dados.

## Testes

```bash
python -m unittest discover -s tests -v
```

Veja `CONFERENCIA_PDF.md` para a correspondência entre o enunciado e a implementação.
