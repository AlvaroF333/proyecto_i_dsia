import pandas as pd

def importe_total_por_region(validos: pd.DataFrame) -> pd.DataFrame:
    return (
        validos.groupby("region", as_index=False)["importe"]
        .sum()
        .sort_values("importe", ascending=False)
    )

# Crea funciones similares para 'top_productos' y 'clientes_recurrentes'