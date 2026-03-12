from src.data_loader import load_pede_excel
from src.preprocess import unify_pede

dfs = load_pede_excel("data/BASE DE DADOS PEDE 2024 - DATATHON.xlsx")
df = unify_pede({
    2022: dfs["PEDE2022"],
    2023: dfs["PEDE2023"],
    2024: dfs["PEDE2024"]
})

print(df.shape)
print(df.head())
