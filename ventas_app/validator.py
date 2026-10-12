import pandas as pd

def validar_ventas(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Separa las filas válidas de las inválidas aplicando reglas de negocio.
    Calcula el importe solo para las válidas.
    """
    work = frame.copy()
    
    # Forzamos los tipos numéricos; los errores se convierten en nulos (NaN)
    work["unidades"] = pd.to_numeric(work["unidades"], errors="coerce")
    work["precio_unitario"] = pd.to_numeric(work["precio_unitario"], errors="coerce")

    # Reglas vectorizadas: numérico y mayor que cero
    ok = (
        work["unidades"].notna()
        & (work["unidades"] > 0)
        & work["precio_unitario"].notna()
        & (work["precio_unitario"] > 0)
    )

    validos = work.loc[ok].copy()
    errores = work.loc[~ok].copy()
    
    # Columna derivada solo en el dataset limpio
    validos["importe"] = validos["unidades"] * validos["precio_unitario"]
    
    return validos, errores