import unittest
from unittest.mock import patch

import numpy as np

from main import (calcular_distancias, crossover_cycle, aplicar_mutacao,
                  criar_populacao, criar_nova_geracao, verificar_populacao,
                  executar)


class TestAlgoritmo(unittest.TestCase):
    def test_distancia_inclui_retorno(self):
        self.assertEqual(calcular_distancias([[1, 2]], [0, 3], [0, 4]), [10])

    def test_cycle_exemplo_pdf(self):
        pai1 = np.array([4, 1, 5, 3, 2, 6])
        pai2 = np.array([3, 4, 6, 2, 1, 5])
        with patch('numpy.random.randint', return_value=3):
            filho1, filho2 = crossover_cycle(pai1, pai2)
        np.testing.assert_array_equal(filho1, [3, 4, 5, 2, 1, 6])
        np.testing.assert_array_equal(filho2, [4, 1, 6, 3, 2, 5])
        np.testing.assert_array_equal(pai1, [4, 1, 5, 3, 2, 6])

    def test_mutacao_troca_exatamente_duas_posicoes(self):
        rota = np.arange(1, 21)
        mutada = aplicar_mutacao(rota)
        self.assertEqual(np.count_nonzero(mutada != rota), 2)
        np.testing.assert_array_equal(np.sort(mutada), rota)
        np.testing.assert_array_equal(rota, np.arange(1, 21))

    def test_geracoes_preservam_permutacoes(self):
        np.random.seed(10)
        populacao = criar_populacao(20, 20)
        x, y = np.linspace(0, 1, 20), np.zeros(20)
        for _ in range(20):
            custos = calcular_distancias(populacao, x, y)
            populacao = criar_nova_geracao(populacao, custos)
            verificar_populacao(populacao, 20, 20)

    def test_melhor_historico_coerente(self):
        np.random.seed(42)
        x, y = np.array([0, 1, 1, 0]), np.array([0, 0, 1, 1])
        inicial, final, solucao, custo = executar(x, y, 30)
        self.assertAlmostEqual(custo, calcular_distancias([solucao], x, y)[0])
        self.assertLessEqual(custo, min(calcular_distancias(inicial, x, y)))
        self.assertLessEqual(custo, min(calcular_distancias(final, x, y)))
        self.assertAlmostEqual(custo, 4)

    def test_detecta_rota_invalida(self):
        with self.assertRaises(ValueError):
            verificar_populacao([[1, 1, 3]], 1, 3)


if __name__ == '__main__':
    unittest.main()
