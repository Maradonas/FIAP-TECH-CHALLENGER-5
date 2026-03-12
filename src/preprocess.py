import re
import numpy as np
import pandas as pd

# Palavras-chave que indicam colunas numéricas
NUMERIC_HINTS = (
    "IDA", "IAN", "IEG", "IAA", "IPS", "IPP", "IPV", "INDE",
    "DEFASAGEM", "PONTO", "NOTA", "SCORE", "INDICE", "ÍNDICE"
)

def _to_snake(text: str) -> str:
    """
    Normaliza nomes de colunas para snake_case simples.
    """
    text = str(text).strip()
    text = re.sub(r"\s+", "_", text)
    text = text.replace("ç", "c").replace("Ç", "C")
    text = re.sub(r"[^0-9a-zA-Z_]+", "", text)
    return text.lower()

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte todas as colunas para snake_case.
    """
    df = df.copy()
    df.columns = [_to_snake(c) for c in df.columns]
    return df

def coerce_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte colunas numéricas que vêm como texto,
    tratando vírgula decimal.
    """
    df = df.copy()

    for col in df.columns:
        col_upper = col.upper()
        if any(key in col_upper for key in NUMERIC_HINTS):
            if df[col].dtype == "object":
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace(".", "", regex=False)   # remove milhar
                    .str.replace(",", ".", regex=False) # vírgula → ponto
                )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def add_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """
    Adiciona coluna 'ano' ao dataframe.
    """
    df = df.copy()
    df["ano"] = year
    return df

def unify_pede(dfs_by_year: dict[int, pd.DataFrame]) -> pd.DataFrame:
    """
    Une dataframes de anos diferentes em um único dataframe.
    """
    frames = []
    for year, df in dfs_by_year.items():
        df = normalize_columns(df)
        df = coerce_numeric_columns(df)
        df = add_year(df, year)
        frames.append(df)

    return pd.concat(frames, ignore_index=True, sort=False)

def detect_key_columns(df: pd.DataFrame) -> dict:
    """
    Detecta automaticamente colunas principais.
    Ajuste manualmente se necessário.
    """
    cols = set(df.columns)

    def pick(candidates):
        for c in candidates:
            if c in cols:
                return c
        return None

    return {
        "id_aluno": pick(["ra", "id_aluno", "aluno_id", "codigo_aluno", "matricula"]),
        "fase": pick(["fase", "fase_aluno", "fase_programa"]),
        "pedra": pick(["pedra", "classificacao_pedra", "pedra_atual"]),
        "ian": pick(["ian"]),
        "ida": pick(["ida"]),
        "ieg": pick(["ieg"]),
        "iaa": pick(["iaa"]),
        "ips": pick(["ips"]),
        "ipp": pick(["ipp"]),
        "ipv": pick(["ipv"]),
        "inde": pick(["inde"]),
        "defasagem": pick(["defasagem", "defasagem_nivel"])
    }

def build_risk_target(
    df: pd.DataFrame,
    defasagem_col: str,
    threshold: float = -1.0
) -> pd.Series:
    """
    Define risco de defasagem:
    defasagem <= threshold → risco = 1
    """
    if defasagem_col not in df.columns:
        raise ValueError(f"Coluna '{defasagem_col}' não encontrada.")

    return (df[defasagem_col] <= threshold).astype(int)
