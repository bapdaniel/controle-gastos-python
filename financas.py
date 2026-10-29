import json
from datetime import date
from pathlib import Path


def carregar_lancamentos(caminho: Path) -> list[dict]:
    if not caminho.exists():
        return []
    try:
        return json.loads(caminho.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def salvar_lancamentos(caminho: Path, lancamentos: list[dict]) -> None:
    caminho.write_text(
        json.dumps(lancamentos, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def adicionar_lancamento(
    caminho: Path,
    tipo: str,
    descricao: str,
    categoria: str,
    valor: float,
) -> dict:
    if tipo not in {"receita", "despesa"}:
        raise ValueError("Tipo deve ser receita ou despesa.")
    if not descricao.strip() or valor <= 0:
        raise ValueError("Descrição e valor positivo são obrigatórios.")

    lancamentos = carregar_lancamentos(caminho)
    novo = {
        "id": max((item["id"] for item in lancamentos), default=0) + 1,
        "data": date.today().isoformat(),
        "tipo": tipo,
        "descricao": descricao.strip(),
        "categoria": categoria.strip() or "Outros",
        "valor": round(valor, 2),
    }
    lancamentos.append(novo)
    salvar_lancamentos(caminho, lancamentos)
    return novo


def resumo(lancamentos: list[dict]) -> dict[str, float]:
    receitas = sum(item["valor"] for item in lancamentos if item["tipo"] == "receita")
    despesas = sum(item["valor"] for item in lancamentos if item["tipo"] == "despesa")
    return {
        "receitas": round(receitas, 2),
        "despesas": round(despesas, 2),
        "saldo": round(receitas - despesas, 2),
    }
