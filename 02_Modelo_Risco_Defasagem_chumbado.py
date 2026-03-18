from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier


PROJECT_ROOT = Path(__file__).resolve().parent
INPUT_CSV = PROJECT_ROOT / "data" / "processed" / "base_unificada.csv"
OUTPUT_MODEL = PROJECT_ROOT / "models" / "modelo_risco_defasagem.joblib"
OUTPUT_METRICS = PROJECT_ROOT / "models" / "metricas_modelo.json"

FEATURES = ["ida", "ieg", "ips", "ipp", "iaa"]
TARGET = "risco_defasagem"


def main() -> None:
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Base não encontrada: {INPUT_CSV}")

    OUTPUT_MODEL.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_METRICS.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_CSV)
    df.columns = [str(c).strip().lower() for c in df.columns]

    missing_features = [c for c in FEATURES + [TARGET] if c not in df.columns]
    if missing_features:
        raise ValueError(f"Colunas ausentes para treino: {missing_features}")

    train_df = df[FEATURES + [TARGET]].copy().dropna(subset=[TARGET])
    train_df[TARGET] = pd.to_numeric(train_df[TARGET], errors="coerce")
    train_df = train_df.dropna(subset=[TARGET])
    train_df[TARGET] = train_df[TARGET].astype(int)

    X = train_df[FEATURES].copy()
    for col in FEATURES:
        X[col] = pd.to_numeric(X[col], errors="coerce")
    y = train_df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y if y.nunique() > 1 else None
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median")),
            ]), FEATURES)
        ],
        remainder="drop"
    )

    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(
            n_estimators=300,
            max_depth=8,
            min_samples_leaf=3,
            random_state=42
        ))
    ])

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    try:
        y_prob = model.predict_proba(X_test)[:, 1]
        roc_auc = float(roc_auc_score(y_test, y_prob))
    except Exception:
        roc_auc = None

    metrics = {
        "features_modelo": FEATURES,
        "target": TARGET,
        "amostras_treino": int(len(X_train)),
        "amostras_teste": int(len(X_test)),
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "f1": float(f1_score(y_test, y_pred, zero_division=0)),
        "roc_auc": roc_auc,
        "class_report": classification_report(y_test, y_pred, output_dict=True, zero_division=0),
    }

    joblib.dump(model, OUTPUT_MODEL)
    OUTPUT_METRICS.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Modelo salvo em: {OUTPUT_MODEL}")
    print(f"Métricas salvas em: {OUTPUT_METRICS}")
    print(f"Features: {FEATURES}")


if __name__ == "__main__":
    main()
