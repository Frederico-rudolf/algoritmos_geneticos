"""Testes da versão opcional: execute com suas dependências instaladas."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree as ET

try:
    import numpy as np
    import matplotlib
except ImportError:
    np = None
else:
    matplotlib.use('Agg')
    from versao_numpy import main as algoritmo


@unittest.skipIf(np is None, 'Instale versao_numpy/requirements.txt para validar esta versão.')
class TestVersaoNumpy(unittest.TestCase):
    def test_distancia_retorno_e_cycle_pdf(self):
        self.assertEqual(algoritmo.calcular_distancias([[1, 2]], [0, 3], [0, 4]), [10])
        pai1, pai2 = np.array([4, 1, 5, 3, 2, 6]), np.array([3, 4, 6, 2, 1, 5])
        with patch('numpy.random.randint', return_value=3):
            filho1, filho2 = algoritmo.crossover_cycle(pai1, pai2)
        np.testing.assert_array_equal(filho1, [3, 4, 5, 2, 1, 6])
        np.testing.assert_array_equal(filho2, [4, 1, 6, 3, 2, 5])
        np.testing.assert_array_equal(pai1, [4, 1, 5, 3, 2, 6])

    def test_busca_e_dois_graficos_com_plot(self):
        import matplotlib.pyplot as plt
        np.random.seed(42)
        x, y = np.array([0, 1, 1, 0]), np.array([0, 0, 1, 1])
        historico = []
        inicial, final, solucao, custo = algoritmo.executar(x, y, 30, historico=historico)
        algoritmo.verificar_populacao(final, 20, 4)
        self.assertEqual(len(historico), 31)
        self.assertEqual(historico[-1], custo)
        self.assertTrue(all(a >= b for a, b in zip(historico, historico[1:])))
        self.assertAlmostEqual(custo, algoritmo.calcular_distancias([solucao], x, y)[0])
        self.assertLessEqual(custo, min(algoritmo.calcular_distancias(inicial, x, y)))
        with tempfile.TemporaryDirectory() as pasta:
            with patch.object(plt, 'plot', wraps=plt.plot) as plot:
                algoritmo.desenhar_graficos(x, y, solucao, custo, historico, pasta, mostrar=False)
            self.assertEqual(plot.call_count, 2)
            caminho_x = plot.call_args_list[0].args[0]
            self.assertEqual(len(caminho_x), 5)
            self.assertEqual(caminho_x[0], caminho_x[-1])
            self.assertEqual(len(plot.call_args_list[1].args[0]), 31)
            for nome in ('melhor_caminho.svg', 'melhor_custo.svg'):
                self.assertEqual(ET.parse(Path(pasta) / nome).getroot().tag,
                                 '{http://www.w3.org/2000/svg}svg')
