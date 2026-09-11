"""Primeros códigos Python para la sesión inicial de capacitación.

Este archivo muestra cuatro operaciones: leer, limpiar, calcular y comparar.
Usa solamente el archivo sintético empresae.xlsx para que aparezca un descuadre.

Uso desde la raíz:
    py -3 ejemplos/primeros_codigos.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parent
ARCHIVO = ROOT / "empresae.xlsx"
REPORTES = ROOT.parent / "reportes"


def main() -> None:
    print("\n=== 1. Leer el Excel ===")
    crudo = pd.read_excel(ARCHIVO, header=None, nrows=8)
    print(crudo.head(6).to_string(index=False, header=False))

    print("\n=== 2. Limpiar el encabezado Sofland ===")
    limpio = pd.read_excel(ARCHIVO, skiprows=4).dropna(how="all")
    print(f"Filas utiles: {len(limpio)}")
    print(f"Columnas: {list(limpio.columns)}")

    print("\n=== 3. Calcular Debe y Haber ===")
    total_debe = limpio["Debe"].sum()
    total_haber = limpio["Haber"].sum()
    diferencia = total_debe - total_haber
    print(f"Debe: ${total_debe:,.0f}")
    print(f"Haber: ${total_haber:,.0f}")
    print(f"Diferencia: ${diferencia:,.0f}")

    print("\n=== 4. Comparar por cuenta ===")
    resumen = (
        limpio.groupby("Cuenta", as_index=False)
        .agg(Debe=("Debe", "sum"), Haber=("Haber", "sum"))
    )
    resumen["Diferencia"] = resumen["Debe"] - resumen["Haber"]
    print(resumen.to_string(index=False))

    REPORTES.mkdir(exist_ok=True)
    salida_excel = REPORTES / "primeros_codigos_empresae.xlsx"
    salida_png = REPORTES / "primeros_codigos_empresae.png"
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
    print("Interpretacion: EmpresaE requiere revision humana antes de continuar.")


if __name__ == "__main__":
    main()
