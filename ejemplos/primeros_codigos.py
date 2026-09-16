"""Primeros códigos Python para la sesión inicial de capacitación.

Este archivo muestra cuatro operaciones: leer, limpiar, calcular y comparar.
Usa solamente el archivo sintético empresae.xlsx para que aparezca un descuadre.

Uso desde la raíz:
    py -3 ejemplos/primeros_codigos.py
"""

from argparse import ArgumentParser
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parent
REPORTES = ROOT.parent / "reportes"


def crear_parser() -> ArgumentParser:
    """Define las opciones para explorar el ejemplo sin editar el codigo."""
    parser = ArgumentParser(
        description=(
            "Recorrido guiado para leer, limpiar, calcular y graficar "
            "un comprobante sintetico de Sofland."
        ),
        epilog=(
            "Ejemplos: py -3 primeros_codigos.py --empresa empresaa.xlsx\n"
            "          py -3 primeros_codigos.py --empresa empresae.xlsx --tolerancia 1000"
        ),
        formatter_class=lambda prog: __import__("argparse").RawDescriptionHelpFormatter(prog),
    )
    parser.add_argument(
        "--empresa",
        default="empresae.xlsx",
        help="Nombre del Excel dentro de ejemplos/ (por defecto: empresae.xlsx).",
    )
    parser.add_argument(
        "--tolerancia",
        type=float,
        default=1.0,
        help="Diferencia maxima considerada dentro de tolerancia (por defecto: 1).",
    )
    parser.add_argument(
        "--salida",
        default="primeros_codigos",
        help="Prefijo de los archivos generados en reportes/.",
    )
    return parser


def main(argumentos=None) -> None:
    args = crear_parser().parse_args(argumentos)
    archivo = ROOT / args.empresa
    if not archivo.exists():
        raise SystemExit(
            f"No se encontro {archivo.name} en {ROOT}. "
            "Ejecuta antes: py -3 generar_ejemplos.py"
        )

    print("\n=== RECORRIDO GUIADO: DE EXCEL A REPORTE ===")
    print(f"Archivo seleccionado: {archivo.name}")
    print("Objetivo: observar que hace cada instruccion antes de usar un pipeline grande.")

    print("\n=== 1. Leer el Excel sin interpretar el encabezado ===")
    print("Estamos mostrando las primeras filas tal como llegan desde Sofland.")
    crudo = pd.read_excel(archivo, header=None, nrows=8)
    print(crudo.head(6).to_string(index=False, header=False))

    print("\n=== 2. Limpiar el encabezado Sofland ===")
    print("Saltamos las cuatro filas de metadata y quitamos filas completamente vacias.")
    limpio = pd.read_excel(archivo, skiprows=4).dropna(how="all")
    print(f"Filas utiles: {len(limpio)}")
    print(f"Columnas: {list(limpio.columns)}")

    print("\n=== 3. Calcular Debe y Haber ===")
    print("Sumamos las columnas para obtener el control global del comprobante.")
    total_debe = limpio["Debe"].sum()
    total_haber = limpio["Haber"].sum()
    diferencia = total_debe - total_haber
    print(f"Debe: ${total_debe:,.0f}")
    print(f"Haber: ${total_haber:,.0f}")
    print(f"Diferencia: ${diferencia:,.0f}")
    estado = "CUADRA" if abs(diferencia) <= args.tolerancia else "REVISAR"
    print(f"Estado con tolerancia {args.tolerancia:,.0f}: {estado}")

    print("\n=== 4. Comparar por cuenta ===")
    print("Agrupamos para localizar donde se concentra la diferencia.")
    resumen = (
        limpio.groupby("Cuenta", as_index=False)
        .agg(Debe=("Debe", "sum"), Haber=("Haber", "sum"))
    )
    resumen["Diferencia"] = resumen["Debe"] - resumen["Haber"]
    print(resumen.to_string(index=False))

    REPORTES.mkdir(exist_ok=True)
    salida_excel = REPORTES / f"{args.salida}_{Path(args.empresa).stem}.xlsx"
    salida_png = REPORTES / f"{args.salida}_{Path(args.empresa).stem}.png"
    with pd.ExcelWriter(salida_excel, engine="openpyxl") as writer:
        limpio.to_excel(writer, sheet_name="Datos_limpios", index=False)
        resumen.to_excel(writer, sheet_name="Resumen_cuentas", index=False)

    resumen.set_index("Cuenta")[['Debe', 'Haber']].plot(
        kind="bar", figsize=(10, 5), title="Debe y Haber por cuenta - EmpresaE"
    )
    plt.ylabel("Monto")
    plt.tight_layout()
    plt.savefig(salida_png, dpi=140)
    plt.close()

    print("\n=== 5. Salidas ===")
    print(f"Excel: {salida_excel}")
    print(f"Grafico: {salida_png}")
    print("Siguiente paso: abre el Excel y compara Datos_limpios con Resumen_cuentas.")
    print("Importante: un estado CUADRA no reemplaza la revision contable humana.")


if __name__ == "__main__":
    main()
