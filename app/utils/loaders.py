from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import joblib
import numpy as np
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "processed" / "base_unificada.csv"
MODEL_PATH = BASE_DIR / "models" / "modelo_risco_defasagem.joblib"
METRICS_PATH = BASE_DIR / "models" / "metricas_modelo.json"

ALIASES = {
    "ipv": ["ianv"],
    "ianv": ["ipv"],
    "pedra": ["fase_programa", "nome_fase"],
    "fase": ["pedra", "nome_fase"],
}

DISPLAY_LABELS = {
    "ida": "IDA",
    "ieg": "IEG",
    "iaa": "IAA",
    "ips": "IPS",
    "ipp": "IPP",
    "ipv": "IPV",
    "ianv": "IANV",
    "ian": "IAN",
    "inde": "INDE",
    "ano": "Ano",
    "pedra": "Fase / Pedra",
}


def _strip_accents(text: str) -> str:
    import unicodedata

    if text is None:
        return ""
    text = unicodedata.normalize("NFKD", str(text))
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def normalize_column_name(name: str) -> str:
    name = _strip_accents(name).strip().lower()
    for old, new in {
        " ": "_",
        "/": "_",
        "-": "_",
        "%": "pct",
        "º": "",
        "°": "",
        "(": "",
        ")": "",
        ".": "_",
    }.items():
        name = name.replace(old, new)
    while "__" in name:
        name = name.replace("__", "_")
    return name.strip("_")


@st.cache_data(show_spinner=False)
def load_metrics(path: Path = METRICS_PATH) -> dict:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_resource(show_spinner=False)
def load_model(path: Path = MODEL_PATH):
    if not path.exists():
        raise FileNotFoundError(f"Modelo não encontrado em: {path}")
    return joblib.load(path)


def _coerce_numeric(df: pd.DataFrame, candidates: Iterable[str]) -> pd.DataFrame:
    for col in candidates:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", ".", regex=False)
                .str.replace("%", "", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def _resolver_inde(row: pd.Series) -> float | None:
    ano = row.get("ano")
    if ano == 2022:
        return row.get("inde_22")
    if ano == 2023:
        return row.get("inde_23") if pd.notna(row.get("inde_23")) else row.get("inde_2023")
    if ano == 2024:
        return row.get("inde_2024")
    return row.get("inde")


def _resolver_pedra(row: pd.Series) -> str | None:
    ano = row.get("ano")
    if ano == 2022:
        return row.get("pedra_22")
    if ano == 2023:
        return row.get("pedra_23") if pd.notna(row.get("pedra_23")) else row.get("pedra_2023")
    if ano == 2024:
        return row.get("pedra_2024")
    return row.get("pedra")


def classificar_faixa_ian(valor: float) -> str | None:
    if pd.isna(valor):
        return None
    if valor <= 2.5:
        return "Severa"
    if valor <= 5:
        return "Moderada"
    if valor < 10:
        return "Leve"
    return "Adequada"


@st.cache_data(show_spinner=False)
def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()

    df = pd.read_csv(path)
    df.columns = [normalize_column_name(c) for c in df.columns]

    numeric_candidates = [
        "ano", "ian", "ida", "ieg", "iaa", "ips", "ipp", "ipv", "ianv",
        "inde", "defasagem", "defas", "inde_22", "inde_23", "inde_2023", "inde_2024"
    ]
    df = _coerce_numeric(df, numeric_candidates)

    if "inde" not in df.columns:
        df["inde"] = np.nan
    df["inde"] = df.apply(_resolver_inde, axis=1)
    df["inde"] = pd.to_numeric(df["inde"], errors="coerce")

    if "pedra" not in df.columns:
        df["pedra"] = None
    df["pedra"] = df.apply(_resolver_pedra, axis=1)
    df["pedra"] = (
        df["pedra"]
        .replace(
            {
                "Agata": "Ágata",
                "AMETISTA": "Ametista",
                "QUARTZO": "Quartzo",
                "TOPAZIO": "Topázio",
            }
        )
        .astype("object")
    )

    if "fase" not in df.columns:
        df["fase"] = df["pedra"]

    if "faixa_ian" not in df.columns and "ian" in df.columns:
        df["faixa_ian"] = df["ian"].apply(classificar_faixa_ian)

    if "defasagem" in df.columns:
        defasagem = pd.to_numeric(df["defasagem"], errors="coerce")
        df["risco_defasagem"] = np.where(defasagem.notna(), (defasagem < 0).astype(int), np.nan)
    elif "defas" in df.columns:
        defas = pd.to_numeric(df["defas"], errors="coerce")
        df["risco_defasagem"] = np.where(defas.notna(), (defas < 0).astype(int), np.nan)
    elif "ian" in df.columns:
        df["risco_defasagem"] = np.where(df["ian"].notna(), (df["ian"] <= 5).astype(int), np.nan)

    for col in ["risco_defasagem", "ano"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    core_cols = [c for c in ["ida", "ieg", "iaa", "ips", "ipp", "ipv", "ian", "inde"] if c in df.columns]
    if core_cols:
        df = df.loc[df[core_cols].notna().any(axis=1)].copy()

    return df


def load_base(path: Path = DATA_PATH) -> pd.DataFrame:
    return load_data(path)


def get_model_features(model=None, metrics: dict | None = None) -> list[str]:
    if model is not None and hasattr(model, "feature_names_in_"):
        return list(model.feature_names_in_)

    if model is not None and hasattr(model, "named_steps"):
        pre = model.named_steps.get("preprocessor")
        if pre is not None:
            try:
                cols = pre.transformers_[0][2]
                return list(cols)
            except Exception:
                pass

    if metrics:
        if metrics.get("features_modelo"):
            return list(metrics["features_modelo"])
        if metrics.get("features"):
            return list(metrics["features"])

    return ["ida", "ieg", "ips", "ipp", "iaa"]


def get_feature_series(df: pd.DataFrame, feature_name: str) -> pd.Series:
    if feature_name in df.columns:
        return pd.to_numeric(df[feature_name], errors="coerce")
    for alias in ALIASES.get(feature_name, []):
        if alias in df.columns:
            return pd.to_numeric(df[alias], errors="coerce")
    return pd.Series(dtype=float)


def infer_slider_bounds(df: pd.DataFrame, feature_name: str) -> tuple[float, float, float, float]:
    serie = get_feature_series(df, feature_name).dropna()
    if serie.empty:
        return 0.0, 10.0, 5.0, 0.1

    low = float(np.floor(serie.quantile(0.05)))
    high = float(np.ceil(serie.quantile(0.95)))

    if low == high:
        low, high = float(serie.min()), float(serie.max())
    if low == high:
        low, high = 0.0, max(10.0, high)

    low = min(low, float(serie.min()))
    high = max(high, float(serie.max()))
    default = float(np.clip(serie.median(), low, high))

    return round(low, 2), round(high, 2), round(default, 2), 0.1


def build_model_input(modelo, valores: dict[str, float]) -> pd.DataFrame:
    features = get_model_features(modelo)
    ordered = {feature: float(valores.get(feature, np.nan)) for feature in features}
    return pd.DataFrame([ordered], columns=features)


def summarize_dataset_quality(df: pd.DataFrame) -> dict:
    summary = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_risk": None,
        "risk_rate": None,
        "ian_distribution": {},
    }

    if "risco_defasagem" in df.columns:
        summary["missing_risk"] = int(df["risco_defasagem"].isna().sum())
        valid = df["risco_defasagem"].dropna()
        if not valid.empty:
            summary["risk_rate"] = float(valid.mean())

    if "faixa_ian" in df.columns:
        vc = df["faixa_ian"].fillna("Não informado").value_counts(dropna=False)
        summary["ian_distribution"] = vc.to_dict()

    return summary