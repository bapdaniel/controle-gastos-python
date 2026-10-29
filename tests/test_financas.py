import tempfile
import unittest
from pathlib import Path

from financas import adicionar_lancamento, carregar_lancamentos, resumo


class FinancasTest(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.arquivo = Path(self.pasta.name) / "dados.json"

    def tearDown(self):
        self.pasta.cleanup()

    def test_adiciona_e_carrega_lancamento(self):
        adicionar_lancamento(self.arquivo, "receita", "Bolsa", "Renda", 500)
        itens = carregar_lancamentos(self.arquivo)
        self.assertEqual(len(itens), 1)
        self.assertEqual(itens[0]["descricao"], "Bolsa")

    def test_calcula_resumo(self):
        itens = [
            {"tipo": "receita", "valor": 1000},
            {"tipo": "despesa", "valor": 250.50},
        ]
        self.assertEqual(resumo(itens)["saldo"], 749.50)


if __name__ == "__main__":
    unittest.main()
