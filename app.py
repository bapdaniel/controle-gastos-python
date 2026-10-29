from pathlib import Path

from financas import (
    adicionar_lancamento,
    carregar_lancamentos,
    despesas_por_categoria,
    exportar_csv,
    resumo,
)


ARQUIVO_DADOS = Path("dados.json")


def ler_valor() -> float:
    while True:
        try:
            valor = float(input("Valor: R$ ").replace(",", "."))
            if valor <= 0:
                raise ValueError
            return valor
        except ValueError:
            print("Digite um valor maior que zero.")


def mostrar_menu() -> None:
    print("\n=== Controle de Gastos ===")
    print("1. Registrar receita")
    print("2. Registrar despesa")
    print("3. Listar lançamentos")
    print("4. Ver resumo")
    print("5. Exportar para CSV")
    print("0. Sair")


def main() -> None:
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao in {"1", "2"}:
            descricao = input("Descrição: ").strip()
            categoria = input("Categoria: ").strip()
            valor = ler_valor()
            tipo = "receita" if opcao == "1" else "despesa"
            adicionar_lancamento(ARQUIVO_DADOS, tipo, descricao, categoria, valor)
            print("Lançamento registrado.")
        elif opcao == "3":
            lancamentos = carregar_lancamentos(ARQUIVO_DADOS)
            if not lancamentos:
                print("Nenhum lançamento cadastrado.")
            for item in lancamentos:
                sinal = "+" if item["tipo"] == "receita" else "-"
                print(f'{item["data"]} | {item["descricao"]} | {sinal} R$ {item["valor"]:.2f}')
        elif opcao == "4":
            lancamentos = carregar_lancamentos(ARQUIVO_DADOS)
            dados = resumo(lancamentos)
            print(f'Receitas: R$ {dados["receitas"]:.2f}')
            print(f'Despesas: R$ {dados["despesas"]:.2f}')
            print(f'Saldo: R$ {dados["saldo"]:.2f}')
            categorias = despesas_por_categoria(lancamentos)
            if categorias:
                print("Despesas por categoria:")
                for categoria, total in categorias.items():
                    print(f"- {categoria}: R$ {total:.2f}")
        elif opcao == "5":
            destino = Path("relatorio.csv")
            exportar_csv(destino, carregar_lancamentos(ARQUIVO_DADOS))
            print(f"Relatório criado em {destino.resolve()}")
        elif opcao == "0":
            print("Até mais!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()

