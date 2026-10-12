import pytest
import pandas as pd
from pathlib import Path
from ventas_app.validator import validar_ventas
from ventas_app.loader import cargar_ventas

@pytest.fixture
def ventas_mini():
    return pd.DataFrame({
        "fecha": ["2026-01-01", "2026-01-02", "2026-01-03"],
        "region": ["Norte", "Sur", "Norte"],
        "producto": ["A", "B", "A"],
        "unidades": [2, None, 5],
        "precio_unitario": [10.0, 20.0, -1.0],
        "cliente_id": ["C1", "C2", "C1"],
    })

def test_validar_ventas_separa_validos_e_invalidos(ventas_mini):
    validos, errores = validar_ventas(ventas_mini)
    assert len(validos) == 1
    assert len(errores) == 2

@pytest.mark.parametrize("precio", [0, -1])
def test_precio_no_positivo_va_a_errores(precio):
    df = pd.DataFrame({"unidades": [1], "precio_unitario": [precio]})
    validos, errores = validar_ventas(df)
    assert len(validos) == 0
    assert len(errores) == 1

@pytest.mark.integration
def test_csv_curso_tiene_140_validas_y_10_invalidas():
    # Test de integración real contra el archivo del curso
    ruta = Path("Datos/ventas.csv")
    df = cargar_ventas(ruta)
    validos, errores = validar_ventas(df)
    assert len(validos) == 140
    assert len(errores) == 10