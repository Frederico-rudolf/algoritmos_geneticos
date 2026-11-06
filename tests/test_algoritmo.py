import unittest
from unittest.mock import patch

import random
import tempfile
from pathlib import Path
from xml.etree import ElementTree as ET

from main import (calcular_distancias, crossover_cycle, aplicar_mutacao,
                  criar_populacao, criar_nova_geracao, verificar_populacao,
                  executar, carregar_cidades, desenhar_caminho)


class TestAlgoritmo(unittest.TestCase):
    def test_distancia_inclui_retorno(self):
        self.assertEqual(calcular_distancias([[1, 2]], [0, 3], [0, 4]), [10])

    def test_cycle_exemplo_pdf(self):
        pai1 = [4, 1, 5, 3, 2, 6]
        pai2 = [3, 4, 6, 2, 1, 5]
        with patch('main.random.randrange', return_value=3):
            filho1, filho2 = crossover_cycle(pai1, pai2)
        self.assertEqual(filho1, [3, 4, 5, 2, 1, 6])
        self.assertEqual(filho2, [4, 1, 6, 3, 2, 5])
        self.assertEqual(pai1, [4, 1, 5, 3, 2, 6])

    def test_mutacao_troca_exatamente_duas_posicoes(self):
        rota = list(range(1, 21))
        mutada = aplicar_mutacao(rota)
        self.assertEqual(sum(a != b for a, b in zip(mutada, rota)), 2)
        self.assertEqual(sorted(mutada), rota)
        self.assertEqual(rota, list(range(1, 21)))

    def test_geracoes_preservam_permutacoes(self):
        random.seed(10)
        populacao = criar_populacao(20, 20)
        x, y = [i / 19 for i in range(20)], [0] * 20
        for _ in range(20):
            custos = calcular_distancias(populacao, x, y)
            populacao = criar_nova_geracao(populacao, custos)
            verificar_populacao(populacao, 20, 20)

    def test_melhor_historico_coerente(self):
        random.seed(42)
        x, y = [0, 1, 1, 0], [0, 0, 1, 1]
        inicial, final, solucao, custo = executar(x, y, 30)
        self.assertAlmostEqual(custo, calcular_distancias([solucao], x, y)[0])
        self.assertLessEqual(custo, min(calcular_distancias(inicial, x, y)))
        self.assertLessEqual(custo, min(calcular_distancias(final, x, y)))
        self.assertAlmostEqual(custo, 4)

    def test_dados_e_svg_com_caminho_fechado(self):
        x, y = carregar_cidades(Path(__file__).resolve().parents[1] / 'cidades.mat')
        self.assertEqual(len(x), 20)
        self.assertAlmostEqual(calcular_distancias([list(range(1, 21))], x, y)[0],
                               9.902727150795021)
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / 'grafico.svg'
            desenhar_caminho(x, y, list(range(1, 21)), 9.9, arquivo, mostrar=False)
            raiz = ET.parse(arquivo).getroot()
            ns = {'s': 'http://www.w3.org/2000/svg'}
            pontos = raiz.find('s:polyline', ns).attrib['points'].split()
            self.assertEqual(len(pontos), 21)
            self.assertEqual(pontos[0], pontos[-1])
            self.assertEqual(len(raiz.findall('s:circle', ns)), 21)

    def test_detecta_rota_invalida(self):
        with self.assertRaises(ValueError):
            verificar_populacao([[1, 1, 3]], 1, 3)


if __name__ == '__main__':
    unittest.main()
