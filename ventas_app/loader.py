import pandas as pd
from pathlib import Path

class DataLoadError(Exception):
    """Error al cargar datos de origen."""

def cargar_ventas(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise DataLoadError(f"No existe el fichero: {path}")
    return pd.read_csv(path)