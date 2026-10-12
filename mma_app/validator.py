import pandas as pd

def validar_ufc(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Valida el dataset de UFC aplicando reglas de negocio robustas."""
    work = frame.copy()
    
    # Forzamos valores numéricos de forma segura si las columnas existen
    for col in ["rounds", "strikes_red", "strikes_blue"]:
        if col in work.columns:
            work[col] = pd.to_numeric(work[col], errors="coerce")
            
    # Inicializamos una máscara booleana global en True del tamaño del DataFrame
    ok = pd.Series(True, index=work.index)
    
    # Aplicamos reglas condicionales de forma segura
    if "fighter_red" in work.columns:
        ok = ok & work["fighter_red"].notna()
    if "fighter_blue" in work.columns:
        ok = ok & work["fighter_blue"].notna()
    if "winner" in work.columns:
        ok = ok & work["winner"].notna()
    if "rounds" in work.columns:
        ok = ok & work["rounds"].notna() & (work["rounds"] > 0)
        
    validos = work.loc[ok].copy()
    errores = work.loc[~ok].copy()
    
    # Columna derivada: total de golpes medios significativos
    if "strikes_red" in validos.columns and "strikes_blue" in validos.columns:
        validos["total_strikes"] = validos["strikes_red"] + validos["strikes_blue"]
        
    return validos, errores