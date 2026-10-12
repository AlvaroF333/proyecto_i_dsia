import sys
from pathlib import Path
from ventas_app.cli import main

def test_cli_ejecucion_completa_smoke_test(tmp_path, monkeypatch):
    # 1. Arrange: Creamos un CSV de entrada temporal válido
    input_csv = tmp_path / "entrada_test.csv"
    input_csv.write_text("region,producto,unidades,precio_unitario,cliente_id\nNorte,A,2,10.0,C1\n", encoding="utf-8")
    output_csv = tmp_path / "salida_test.csv"
    
    # Simulamos lo que escribiría el usuario en la terminal
    argumentos_simulados = ["cli.py", "--input", str(input_csv), "--output", str(output_csv)]
    monkeypatch.setattr(sys, "argv", argumentos_simulados)
    
    # 2. Act: Llamamos a la función principal del CLI
    main()
    
    # 3. Assert: Comprobamos que el flujo se completó y se generó el archivo de salida
    assert output_csv.exists()
    
    # Opcional: leer el output y comprobar que se ha procesado
    salida_texto = output_csv.read_text(encoding="utf-8")
    assert "Norte" in salida_texto