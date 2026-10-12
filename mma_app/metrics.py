import pandas as pd

def victorias_por_esquina(validos: pd.DataFrame) -> pd.DataFrame:
    return validos["winner"].value_counts().reset_index()

def peleadores_mas_activos(validos: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Retorna los peleadores que más veces han peleado desde la esquina roja."""
    return validos["fighter_red"].value_counts().head(n).reset_index()