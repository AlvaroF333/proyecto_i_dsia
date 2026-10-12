import argparse
from pathlib import Path
from .loader import cargar_ufc, MmaLoadError
from .validator import validar_ufc
from .metrics import victorias_por_esquina, peleadores_mas_activos

def parse_args():
    parser = argparse.ArgumentParser(description="Pipeline de análisis UFC.")
    parser.add_argument("--input", required=True, help="Ruta al CSV de entrada")
    parser.add_argument("--output", required=True, help="Ruta de salida")
    return parser.parse_args()

def main():
    args = parse_args()
    try:
        raw = cargar_ufc(Path(args.input))
        validos, errores = validar_ufc(raw)
        
        print(f"🥊 Combates Válidos: {len(validos)} | ❌ Descartados: {len(errores)}")
        print("\n📈 Victorias por esquina:")
        print(victorias_por_esquina(validos))
        print("\n🔥 Peleadores más activos (Esquina Roja):")
        print(peleadores_mas_activos(validos))
        
        validos.to_csv(Path(args.output), index=False)
        print(f"\n💾 Archivo procesado guardado en: {args.output}")
        
    except MmaLoadError as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    main()