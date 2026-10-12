import pandas as pd
from pathlib import Path

class MmaLoadError(Exception):
    """Excepción de dominio para errores de lectura en MMA."""

def cargar_ufc(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise MmaLoadError(f"Dataset de UFC no encontrado en: {path}")
    
    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise MmaLoadError(f"Error al leer el CSV: {e}")
        
    # Estandarizamos solo las columnas que vamos a usar
    columnas_base = {
        "R_fighter": "fighter_red",
        "B_fighter": "fighter_blue",
        "Referee": "referee",
        "Winner": "winner",
        "no_of_rounds": "rounds",
        "R_avg_SIG_STR_landed": "strikes_red",
        "B_avg_SIG_STR_landed": "strikes_blue"
    }
    
    # Filtramos para no romper la ejecución si una columna falta en la muestra
    cols_presentes = [c for c in columnas_base.keys() if c in df.columns]
    return df[cols_presentes].rename(columns=columnas_base)