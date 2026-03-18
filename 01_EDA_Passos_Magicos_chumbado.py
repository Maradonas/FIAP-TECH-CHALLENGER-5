from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent
INPUT_XLSX = PROJECT_ROOT / "data" / "BASE DE DADOS PEDE 2024 - DATATHON.xlsx"
OUTPUT_CSV = PROJECT_ROOT / "data" / "processed" / "base_unificada.csv"
OUTPUT_DIAGNOSTICS = PROJECT_ROOT / "data" / "processed" / "diagnostico_base.json"


def normalize_col(col: str) -> str:
    col = str(col).strip().lower()
    repl = {
        "á": "a", "à": "a", "ã": "a", "â": "a",
        "é": "e", "ê": "e",
        "í": "i",
        "ó": "o", "õ": "o", "ô": "o",
        "ú": "u",
        "ç": "c",
        " ": "_", "-": "_", "/": "_", ".": "_",
        "(": "", ")": "", "%": "pct"
    }
    for k, v in repl.items():
        col = col.replace(k, v)
    while "__" in col:
        col = col.replace("__", "_")
    return col.strip("_")


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [normalize_col(c) for c in df.columns]

    aliases = {
        "nome_fase": "fase",
        "fase_do_programa": "fase",
        "fase_programa": "fase",
        "fase_atual": "fase",
        "ano_base": "ano",
        "ano_referencia": "ano",
        "indice_de_autoavaliacao": "iaa",
        "indice_autoavaliacao": "iaa",
        "indice_de_engajamento": "ieg",
        "indice_engajamento": "ieg",
        "indice_de_aprendizagem": "ida",
        "indice_aprendizagem": "ida",
        "indice_de_psicossocial": "ips",
        "indice_psicossocial": "ips",
        "indice_de_protagonismo": "ipp",
        "indice_protagonismo": "ipp",
        "indice_de_adequacao_de_nivel": "ian",
        "indice_adequacao_de_nivel": "ian",
        "nivel_ian": "ian",
        "def": "defasagem",
        "defas": "defasagem",
        "indicador_inde": "inde",
        "pedra_2022": "pedra",
        "pedra_2023": "pedra",
        "pedra_2024": "pedra",
    }

    rename_map = {c: aliases[c] for c in df.columns if c in aliases}
    df = df.rename(columns=rename_map)
    return df


def coerce_numeric(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    df = df.copy()
    for col in cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", ".", regex=False)
                .str.replace("%", "", regex=False)
                .replace({"nan": np.nan, "None": np.nan, "": np.nan})
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def infer_year_from_sheet(sheet_name: str) -> int | None:
    digits = "".join(ch for ch in str(sheet_name) if ch.isdigit())
    if len(digits) >= 4:
        year = int(digits[-4:])
        if 2000 <= year <= 2100:
            return year
    return None


def compute_faixa_ian(series: pd.Series) -> pd.Series:
    def classify(x):
        if pd.isna(x):
            return np.nan
        if x <= 2.5:
            return "Severa"
        if x <= 5:
            return "Moderada"
        if x < 10:
            return "Leve"
        return "Adequada"

    return series.apply(classify)


def enrich_base(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_columns(df)

    numeric_cols = [
        "ano", "ida", "ieg", "iaa", "ips", "ipp", "ian", "inde", "defasagem"
    ]
    df = coerce_numeric(df, numeric_cols)

    if "pedra" not in df.columns and "inde" in df.columns:
        df["pedra"] = pd.cut(
            df["inde"],
            bins=[-np.inf, 5, 6.5, 8, np.inf],
            labels=["Quartzo", "Agata", "Ametista", "Topazio"]
        ).astype("object")

    if "faixa_ian" not in df.columns and "ian" in df.columns:
        df["faixa_ian"] = compute_faixa_ian(df["ian"])

    if "risco_defasagem" not in df.columns:
        if "defasagem" in df.columns and df["defasagem"].notna().any():
            df["risco_defasagem"] = (df["defasagem"] < 0).astype(int)
        elif "ian" in df.columns and df["ian"].notna().any():
            df["risco_defasagem"] = (df["ian"] <= 5).astype(int)
        else:
            df["risco_defasagem"] = np.nan

    if "fase" in df.columns:
        df["fase"] = df["fase"].astype(str).str.strip()

    return df


def load_all_sheets(path: Path) -> pd.DataFrame:
    xls = pd.ExcelFile(path)
    frames = []

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(path, sheet_name=sheet_name)
        df = enrich_base(df)

        if "ano" not in df.columns or df["ano"].isna().all():
            inferred = infer_year_from_sheet(sheet_name)
            if inferred is not None:
                df["ano"] = inferred

        df["origem_aba"] = sheet_name
        frames.append(df)

    base = pd.concat(frames, ignore_index=True, sort=False)

    preferred = [
        "ano", "fase", "pedra", "inde", "ian", "faixa_ian", "ida", "ieg", "iaa",
        "ips", "ipp", "defasagem", "risco_defasagem", "origem_aba"
    ]
    final_cols = [c for c in preferred if c in base.columns] + [c for c in base.columns if c not in preferred]
    return base[final_cols]


def build_diagnostics(df: pd.DataFrame) -> dict:
    return {
        "linhas": int(len(df)),
        "colunas": df.columns.tolist(),
        "anos": sorted([int(x) for x in df["ano"].dropna().unique().tolist()]) if "ano" in df.columns else [],
        "risco_defasagem_distribuicao": df["risco_defasagem"].value_counts(dropna=False).to_dict() if "risco_defasagem" in df.columns else {},
        "faixa_ian_distribuicao": df["faixa_ian"].value_counts(dropna=False).to_dict() if "faixa_ian" in df.columns else {},
        "missing_por_coluna": {k: int(v) for k, v in df.isna().sum().to_dict().items()},
    }


def main() -> None:
    if not INPUT_XLSX.exists():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {INPUT_XLSX}")

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIAGNOSTICS.parent.mkdir(parents=True, exist_ok=True)

    df = load_all_sheets(INPUT_XLSX)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    diagnostics = build_diagnostics(df)
    OUTPUT_DIAGNOSTICS.write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Base salva em: {OUTPUT_CSV}")
    print(f"Diagnóstico salvo em: {OUTPUT_DIAGNOSTICS}")
    print(f"Linhas: {len(df)} | Colunas: {len(df.columns)}")


if __name__ == "__main__":
    main()
