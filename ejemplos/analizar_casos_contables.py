"""Ejemplos didacticos de analisis contable sobre los archivos Sofland.

Este script trabaja solo con los Excel sinteticos de ejemplos/. No decide reglas
contables: reporta controles para revision humana.

Uso desde la raiz del proyecto:
    python ejemplos/analizar_casos_contables.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
REPORTES = ROOT.parent / "reportes"
EMPRESAS = sorted(ROOT.glob("empresa*.xlsx"))
COLUMNAS_MINIMAS = {"Cuenta", "Debe", "Haber"}


def detectar_fila_encabezado(path: Path, max_rows: int = 12) -> int:
    preview = pd.read_excel(path, header=None, nrows=max_rows)
    for index, row in preview.iterrows():
        values = {str(value).strip() for value in row.dropna().tolist()}
        if COLUMNAS_MINIMAS.issubset(values):
            return int(index)
    raise ValueError(f"No se encontro encabezado contable en {path.name}")


def leer_comprobante(path: Path) -> pd.DataFrame:
    header = detectar_fila_encabezado(path)
    frame = pd.read_excel(path, skiprows=header)
    frame = frame.loc[:, ~frame.columns.astype(str).str.startswith("Unnamed")]
    frame = frame.dropna(how="all").copy()
    frame.columns = [str(column).strip() for column in frame.columns]
    for column in ("Debe", "Haber"):
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0)
    frame["_archivo_origen"] = path.name
    frame["_diferencia_fila"] = frame["Debe"] - frame["Haber"]
    return frame


def revisar_comprobante(frame: pd.DataFrame) -> dict:
    missing_columns = sorted(COLUMNAS_MINIMAS - set(frame.columns))
    duplicate_rows = int(frame.duplicated().sum())
    missing_accounts = int(frame["Cuenta"].isna().sum()) if "Cuenta" in frame else 0
    total_debe = float(frame["Debe"].sum())
    total_haber = float(frame["Haber"].sum())
    difference = total_debe - total_haber
    return {
        "archivo": frame["_archivo_origen"].iloc[0],
        "filas": len(frame),
        "columnas_faltantes": missing_columns,
        "filas_duplicadas": duplicate_rows,
        "cuentas_vacias": missing_accounts,
        "total_debe": total_debe,
        "total_haber": total_haber,
        "diferencia": difference,
        "cuadrado": abs(difference) < 1,
    }


def resumen_por_cuenta(frame: pd.DataFrame) -> pd.DataFrame:
    return (
        frame.groupby(["Cuenta", "Glosa_Cuenta"], dropna=False, as_index=False)
        .agg(
            registros=("Cuenta", "size"),
            total_debe=("Debe", "sum"),
            total_haber=("Haber", "sum"),
        )
        .assign(diferencia=lambda data: data["total_debe"] - data["total_haber"])
        .sort_values("diferencia", key=lambda values: values.abs(), ascending=False)
    )


def resumen_por_centro_de_costo(frame: pd.DataFrame) -> pd.DataFrame:
    if "Centro_Costo" not in frame.columns:
        return pd.DataFrame()
    return (
        frame.groupby("Centro_Costo", dropna=False, as_index=False)
        .agg(total_debe=("Debe", "sum"), total_haber=("Haber", "sum"), registros=("Cuenta", "size"))
        .assign(diferencia=lambda data: data["total_debe"] - data["total_haber"])
    )


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Lee comprobantes Sofland, calcula controles y genera un Excel explicativo.",
        epilog=(
            "Ejemplo: py -3 analizar_casos_contables.py --entrada . --salida ../reportes/analisis.xlsx"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--entrada", type=Path, default=ROOT, help="Carpeta con empresa*.xlsx.")
    parser.add_argument("--salida", type=Path, default=REPORTES / "reporte_analisis_contable.xlsx", help="Excel de salida.")
    return parser


def main(argumentos=None) -> None:
    args = crear_parser().parse_args(argumentos)
    empresas = sorted(args.entrada.glob("empresa*.xlsx"))
    if not empresas:
        raise SystemExit(
            f"No hay empresa*.xlsx en {args.entrada}. "
            "Ejecuta primero generar_ejemplos.py."
        )

    print("\n=== ANALISIS GUIADO DE COMPROBANTES ===")
    print(f"Entrada: {args.entrada.resolve()}")
    print(f"Archivos encontrados: {len(empresas)}")
    print("En cada archivo buscamos Cuenta, Debe y Haber antes de leer los datos.")

    frames = []
    for path in empresas:
        print(f"  -> leyendo {path.name}")
        frames.append(leer_comprobante(path))
    report = pd.DataFrame([revisar_comprobante(frame) for frame in frames])
    consolidado = pd.concat(frames, ignore_index=True)
    por_cuenta = resumen_por_cuenta(consolidado)
    por_centro = resumen_por_centro_de_costo(consolidado)

    args.salida.parent.mkdir(exist_ok=True)
    output = args.salida
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        report.to_excel(writer, sheet_name="Control_empresas", index=False)
        consolidado.to_excel(writer, sheet_name="Consolidado", index=False)
        por_cuenta.to_excel(writer, sheet_name="Resumen_cuentas", index=False)
        por_centro.to_excel(writer, sheet_name="Resumen_centros", index=False)

    print(report.to_string(index=False))
    print(f"\nReporte generado: {output}")
    print("Recomendacion: abrir Control_empresas y revisar toda diferencia distinta de cero.")
    print("Las filas, cuentas y tolerancias requieren aprobacion humana antes de importar.")


if __name__ == "__main__":
    main()
