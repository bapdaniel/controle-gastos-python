import tempfile
import unittest
from pathlib import Path

from financas import (
    adicionar_lancamento,
    carregar_lancamentos,
    despesas_por_categoria,
    exportar_csv,
    resumo,
)


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

    def test_agrupa_despesas_por_categoria(self):
        itens = [
            {"tipo": "despesa", "categoria": "Estudos", "valor": 20},
            {"tipo": "despesa", "categoria": "Estudos", "valor": 30},
            {"tipo": "receita", "categoria": "Renda", "valor": 100},
        ]
        self.assertEqual(despesas_por_categoria(itens), {"Estudos": 50})

    def test_exporta_csv(self):
        destino = Path(self.pasta.name) / "relatorio.csv"
        itens = [{
            "id": 1,
            "data": "2026-10-29",
            "tipo": "receita",
            "descricao": "Bolsa",
            "categoria": "Renda",
            "valor": 500,
        }]
        exportar_csv(destino, itens)
        self.assertIn("Bolsa", destino.read_text(encoding="utf-8-sig"))


if __name__ == "__main__":
    unittest.main()

