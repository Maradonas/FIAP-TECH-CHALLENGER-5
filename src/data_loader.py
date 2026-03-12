import pandas as pd

SHEETS_DEFAULT = ["PEDE2022", "PEDE2023", "PEDE2024"]

def load_pede_excel(path: str, sheets=None) -> dict[str, pd.DataFrame]:
    """
    Carrega o Excel do Datathon (múltiplas abas por ano).
    Retorna um dict {sheet_name: df}.
    """
    if sheets is None:
        sheets = SHEETS_DEFAULT

    xls = pd.ExcelFile(path)
    out: dict[str, pd.DataFrame] = {}

    for sh in sheets:
        if sh in xls.sheet_names:
            out[sh] = pd.read_excel(path, sheet_name=sh)
        else:
            # tenta variações comuns de nome (diferença de maiúsc/minúsc e espaços)
            cand = [s for s in xls.sheet_names if s.strip().lower() == sh.strip().lower()]
            if cand:
                out[sh] = pd.read_excel(path, sheet_name=cand[0])

    if not out:
        raise ValueError(f"Nenhuma aba esperada encontrada. Abas disponíveis: {xls.sheet_names}")

    return out
