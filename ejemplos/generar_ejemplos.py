"""
generar_ejemplos.py
====================
Genera archivos Excel sintéticos coherentes para practicar con el sistema.

Crea:
  - empresa_A.xlsx  (EmpresaA - Rol General)
  - empresa_B.xlsx  (EmpresaB - Rol Privado)
  - empresa_C.xlsx  (EmpresaC - Mixta)
  - empresa_D.xlsx  (EmpresaD - Solo Honorarios)
  - empresa_E.xlsx  (EmpresaE - Con descuadre intencional para practicar)
  - cartola_banco.xlsx  (Extracto bancario del período)

Ejecutar con:
    python generar_ejemplos.py
"""

import os
import random
import argparse
import pandas as pd
import numpy as np
from datetime import date, timedelta

# Semilla para reproducibilidad
np.random.seed(42)
random.seed(42)

# ── Configuración ─────────────────────────────────────────────
PERIODO = "2024-08"
DIRECTORIO = os.path.dirname(os.path.abspath(__file__))

# Cuentas contables de remuneraciones (Plan de cuentas simplificado)
CUENTAS = {
    "5100001": "Remuneraciones Sueldo Base",
    "5100002": "Remuneraciones Horas Extras",
    "5100003": "Remuneraciones Bonos",
    "4105001": "Aguinaldo Fiestas Patrias",
    "4105002": "Aguinaldo Navidad",
    "4108001": "Finiquito Rol General",
    "4108002": "Finiquito Rol Privado",
    "2300001": "Vacaciones Devengadas",
    "2300002": "Gastos Anticipados RRHH",
    "1101001": "Banco Estado CTA CTE",
    "2105001": "AFP por Pagar",
    "2105002": "Isapre/Fonasa por Pagar",
    "2105003": "Impuesto Único por Pagar",
}

CENTROS_COSTO = ["CC001-Admin", "CC002-Operaciones", "CC003-Ventas", "CC004-RRHH", "CC005-TI"]

GLOSAS_TIPO = {
    "5100001": "Sueldo base {mes} colaboradores",
    "5100002": "Horas extras {mes}",
    "5100003": "Bono asistencia {mes}",
    "4105001": "Aguinaldo Fiestas Patrias {mes}",
    "4105002": "Aguinaldo Navidad {mes}",
    "4108001": "Finiquito Rol General {mes}",
    "4108002": "Finiquito Rol Privado {mes}",
    "2300001": "Provisión vacaciones {mes}",
    "2300002": "Gastos anticipados RRHH {mes}",
    "1101001": "Pago nómina masiva {mes}",
    "2105001": "AFP retenida {mes}",
    "2105002": "Previsión salud retenida {mes}",
    "2105003": "Impuesto único trabajadores {mes}",
}

EMPRESAS = {
    "EmpresaA": {"colaboradores": 3200, "rol": "General", "tiene_aguinaldo": True,  "tiene_finiquito": False},
    "EmpresaB": {"colaboradores": 2800, "rol": "Privado",  "tiene_aguinaldo": True,  "tiene_finiquito": True},
    "EmpresaC": {"colaboradores": 2500, "rol": "Mixto",    "tiene_aguinaldo": False, "tiene_finiquito": True},
    "EmpresaD": {"colaboradores": 1800, "rol": "Honorarios","tiene_aguinaldo": False, "tiene_finiquito": False},
    "EmpresaE": {"colaboradores": 2700, "rol": "General",  "tiene_aguinaldo": True,  "tiene_finiquito": False,
                 "descuadre_intencional": True},  # ← Para practicar detección de errores
}


def generar_encabezado_sofland(ws, empresa: str):
    """Agrega las 4 filas de encabezado basura que Sofland exporta."""
    from openpyxl.styles import Font, PatternFill, Alignment
    ws["A1"] = "SISTEMA SOFLAND S.A."
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = f"Fecha Impresión: {date.today().strftime('%d/%m/%Y')}"
    ws["A3"] = f"Usuario: JOCELYN.CONTABILIDAD"
    ws["A4"] = "-" * 50
    return ws


def generar_comprobante(empresa: str, config: dict) -> pd.DataFrame:
    """Genera un libro de remuneraciones sintético para una empresa."""
    n_col = config["colaboradores"]
    mes = PERIODO

    registros = []
    sueldo_base_total = round(n_col * np.random.uniform(600_000, 900_000), 0)
    horas_extra_total = round(n_col * np.random.uniform(10_000, 50_000), 0)
    bono_total        = round(n_col * np.random.uniform(20_000, 80_000), 0)
    afp_total         = round(sueldo_base_total * 0.10, 0)
    isapre_total      = round(sueldo_base_total * 0.07, 0)
    iut_total         = round(sueldo_base_total * 0.04, 0)
    banco_total       = sueldo_base_total + horas_extra_total + bono_total - afp_total - isapre_total - iut_total

    cuentas_base = [
        # (cuenta, debe, haber, glosa_key)
        ("5100001", sueldo_base_total, 0,              "5100001"),
        ("5100002", horas_extra_total, 0,              "5100002"),
        ("5100003", bono_total,        0,              "5100003"),
        ("2105001", 0,                 afp_total,      "2105001"),
        ("2105002", 0,                 isapre_total,   "2105002"),
        ("2105003", 0,                 iut_total,      "2105003"),
        ("1101001", 0,                 banco_total,    "1101001"),
    ]

    if config.get("tiene_aguinaldo"):
        aguinaldo = round(n_col * 45_000, 0)
        cuentas_base.append(("4105001", aguinaldo, 0, "4105001"))
        cuentas_base.append(("1101001", 0, aguinaldo, "1101001"))

    if config.get("tiene_finiquito"):
        finiquito = round(np.random.randint(5, 25) * np.random.uniform(800_000, 2_500_000), 0)
        clave = "4108001" if config["rol"] == "General" else "4108002"
        cuentas_base.append((clave, finiquito, 0, clave))
        cuentas_base.append(("1101001", 0, finiquito, "1101001"))

    # Descuadre intencional en EmpresaE para que Jocelyn practique detectarlo
    if config.get("descuadre_intencional"):
        cuentas_base.append(("5100001", 1_500_000, 0, "5100001"))  # Falta el Haber correspondiente

    for i, (cuenta, debe, haber, glosa_key) in enumerate(cuentas_base):
        registros.append({
            "Cuenta":       cuenta,
            "Glosa_Cuenta": CUENTAS[cuenta],
            "Glosa":        GLOSAS_TIPO[glosa_key].format(mes=mes),
            "Clase_Doc":    "RE" if cuenta.startswith("5") else ("PA" if cuenta.startswith("1") else "PV"),
            "Centro_Costo": random.choice(CENTROS_COSTO),
            "Empresa":      empresa,
            "Periodo":      mes,
            "Debe":         debe,
            "Haber":        haber,
        })

    return pd.DataFrame(registros)


def guardar_con_encabezado_sofland(df: pd.DataFrame, ruta: str, empresa: str):
    """Guarda el DataFrame con las 4 filas de encabezado basura (como Sofland lo exporta)."""
    try:
        import openpyxl
        from openpyxl.utils.dataframe import dataframe_to_rows
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Comprobante"

        # Filas de encabezado basura (las 4 que hay que eliminar)
        ws.append(["SISTEMA SOFLAND S.A."])
        ws.append([f"Fecha Impresión: {date.today().strftime('%d/%m/%Y')}"])
        ws.append(["Usuario: JOCELYN.CONTABILIDAD"])
        ws.append(["-" * 60])

        # Headers y datos reales
        ws.append(list(df.columns))
        for row in df.itertuples(index=False):
            ws.append(list(row))

        wb.save(ruta)
        print(f"  ✅ {os.path.basename(ruta)} ({len(df)} registros, encabezado Sofland incluido)")
    except ImportError:
        # Fallback sin openpyxl fancy
        df.to_excel(ruta, index=False)
        print(f"  ✅ {os.path.basename(ruta)} ({len(df)} registros, sin encabezado)")


def generar_cartola_banco() -> pd.DataFrame:
    """Genera una cartola bancaria sintética del período."""
    fechas = pd.date_range(f"{PERIODO}-01", periods=31, freq="D")
    tipos  = ["Transferencia Nómina", "Pago AFP", "Pago Isapre", "Pago Impuesto",
              "Pago Aguinaldo", "Pago Finiquito", "Cargo Comisión"]
    registros = []
    for _ in range(80):
        registros.append({
            "Fecha":       random.choice(fechas).date(),
            "Descripcion": random.choice(tipos),
            "Referencia":  f"REF-{random.randint(100000, 999999)}",
            "Monto_Banco": round(np.random.uniform(500_000, 50_000_000), 0),
            "Banco":       "Banco Estado",
        })
    df = pd.DataFrame(registros).sort_values("Fecha").reset_index(drop=True)
    return df


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Genera Excel sinteticos para practicar lectura, limpieza, "
            "cuadratura y consolidacion contable."
        ),
        epilog=(
            "Despues de generar: py -3 analizar_casos_contables.py\n"
            "Para practicar errores: py -3 generar_casos_especiales.py"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--periodo",
        default=PERIODO,
        help="Periodo de los ejemplos, formato AAAA-MM (por defecto: %(default)s).",
    )
    parser.add_argument(
        "--empresas",
        type=int,
        default=len(EMPRESAS),
        choices=range(1, len(EMPRESAS) + 1),
        help="Cantidad de empresas a generar, de 1 a 5 (por defecto: 5).",
    )
    parser.add_argument(
        "--sin-desbalance",
        action="store_true",
        help="No agrega el descuadre intencional de EmpresaE.",
    )
    parser.add_argument(
        "--salida",
        type=str,
        default=DIRECTORIO,
        help="Carpeta donde guardar los Excel, sin borrar archivos existentes.",
    )
    return parser


if __name__ == "__main__":
    args = crear_parser().parse_args()
    DIRECTORIO = os.path.abspath(args.salida)
    os.makedirs(DIRECTORIO, exist_ok=True)
    PERIODO = args.periodo
    empresas = list(EMPRESAS.items())[:args.empresas]
    if args.sin_desbalance:
        for _, config in empresas:
            config.pop("descuadre_intencional", None)

    print("=" * 55)
    print("  GENERADOR GUIADO DE DATOS DE EJEMPLO")
    print(f"  Período: {PERIODO}")
    print(f"  Empresas: {len(empresas)}")
    print("  Objetivo: crear archivos seguros para practicar sin datos reales")
    print("=" * 55)
    print()

    # Generar comprobantes de cada empresa
    for nombre, config in empresas:
        df = generar_comprobante(nombre, config)
        ruta = os.path.join(DIRECTORIO, f"{nombre.lower()}.xlsx")
        guardar_con_encabezado_sofland(df, ruta, nombre)

    # Generar cartola bancaria
    df_cartola = generar_cartola_banco()
    ruta_cartola = os.path.join(DIRECTORIO, "cartola_banco.xlsx")
    df_cartola.to_excel(ruta_cartola, index=False)
    print(f"  ✅ cartola_banco.xlsx ({len(df_cartola)} movimientos)")

    print()
    print(f"  📁 Archivos creados en: {os.path.abspath(DIRECTORIO)}")
    print()
    print("  GUÍA PARA PRACTICAR:")
    print("  1. Revisa primero las filas de encabezado de cualquier empresa.")
    print("  2. Sube empresa_A.xlsx, empresa_B.xlsx, empresa_C.xlsx,")
    print("     empresa_D.xlsx al módulo 'Limpiar Comprobantes'.")
    print("  3. Nota que empresa_E.xlsx tiene un DESCUADRE INTENCIONAL.")
    print("     Úsalo para practicar la detección de errores.")
    print("  4. Sube cartola_banco.xlsx al módulo 'Cuadratura Bancaria'.")
    print("  5. Siguiente comando: py -3 primeros_codigos.py --empresa empresae.xlsx")
    print()
