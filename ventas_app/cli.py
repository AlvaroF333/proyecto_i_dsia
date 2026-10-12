import argparse
import json
from pathlib import Path
from .loader import cargar_ventas, DataLoadError
from .validator import validar_ventas
from .metrics import importe_total_por_region

def parse_args():
    parser = argparse.ArgumentParser(description="Pipeline de procesamiento de ventas.")
    parser.add_argument("--input", type=str, required=True, help="Ruta al CSV de entrada")
    parser.add_argument("--output", type=str, required=True, help="Ruta al CSV limpio de salida")
    return parser.parse_args()

def main():
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    try:
        # 1. Cargar
        raw = cargar_ventas(input_path)

        # 2. Validar
        validos, errores = validar_ventas(raw)
        print(f"✅ Válidas: {len(validos)} | ❌ Inválidas: {len(errores)}")

        # 3. Métricas
        region_metrics = importe_total_por_region(validos)
        print("\nImporte por región:")
        print(region_metrics.head())

        # 4. Exportar
        validos.to_csv(output_path, index=False)
        print(f"\nDatos limpios exportados a: {output_path}")

    except DataLoadError as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    main()