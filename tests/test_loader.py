import pytest
from pathlib import Path
from ventas_app.loader import cargar_ventas, DataLoadError

def test_cargar_ventas_lanza_error_si_no_existe():
    ruta_falsa = Path("ruta_inventada.csv")
    with pytest.raises(DataLoadError):
        cargar_ventas(ruta_falsa)