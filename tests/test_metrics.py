import pandas as pd
from ventas_app.metrics import importe_total_por_region

def test_importe_total_por_region_suma_correctamente():
    df_valido = pd.DataFrame({
        "region": ["Norte", "Norte", "Sur"],
        "importe": [100.0, 50.0, 200.0]
    })
    
    resultado = importe_total_por_region(df_valido)
    
    # Norte debería tener 150.0 y Sur 200.0
    importe_norte = resultado.loc[resultado["region"] == "Norte", "importe"].iloc[0]
    importe_sur = resultado.loc[resultado["region"] == "Sur", "importe"].iloc[0]
    
    assert importe_norte == 150.0
    assert importe_sur == 200.0