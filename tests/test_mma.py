import pytest
import pandas as pd
from pathlib import Path
import sys
from mma_app.loader import cargar_ufc, MmaLoadError
from mma_app.validator import validar_ufc
from mma_app.metrics import victorias_por_esquina
from mma_app.cli import main

def test_loader_falla_sin_csv():
    with pytest.raises(MmaLoadError):
        cargar_ufc(Path("archivo_inexistente.csv"))

@pytest.fixture
def ufc_mini():
    return pd.DataFrame({
        "R_fighter": ["Jon Jones", "Ilia Topuria", None],
        "B_fighter": ["Ciryl Gane", "Max Holloway", "Fighter C"],
        "Winner": ["Red", "Red", "Blue"],
        "no_of_rounds": [5, 3, 0], # El 0 invalida el tercer combate
        "R_avg_SIG_STR_landed": [10.5, 45.2, 5.0],
        "B_avg_SIG_STR_landed": [2.1, 40.0, 2.0]
    })

def test_validator_reglas_negocio(ufc_mini):
    # Simulamos el estado post-loader
    df = ufc_mini.rename(columns={
        "R_fighter": "fighter_red", "B_fighter": "fighter_blue",
        "Winner": "winner", "no_of_rounds": "rounds",
        "R_avg_SIG_STR_landed": "strikes_red", "B_avg_SIG_STR_landed": "strikes_blue"
    })
    validos, errores = validar_ufc(df)
    assert len(validos) == 2
    assert len(errores) == 1
    assert "total_strikes" in validos.columns

def test_metrics_victorias(ufc_mini):
    df = ufc_mini.rename(columns={"R_fighter": "fighter_red", "B_fighter": "fighter_blue", "Winner": "winner", "no_of_rounds": "rounds"})
    validos, _ = validar_ufc(df)
    res = victorias_por_esquina(validos)
    assert len(res) == 1 # En los válidos, ambas victorias son "Red"

def test_cli_smoke_test(tmp_path, monkeypatch):
    input_csv = tmp_path / "in.csv"
    input_csv.write_text("R_fighter,B_fighter,Winner,no_of_rounds\nJon,Ciryl,Red,5\n", encoding="utf-8")
    out_csv = tmp_path / "out.csv"
    
    monkeypatch.setattr(sys, "argv", ["cli.py", "--input", str(input_csv), "--output", str(out_csv)])
    main()
    assert out_csv.exists()