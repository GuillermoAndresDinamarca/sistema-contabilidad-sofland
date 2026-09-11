"""Genera tres casos pequeños para la primera práctica con la aplicación."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent


def guardar(nombre: str, filas: list[dict]) -> None:
    pd.DataFrame(filas).to_excel(ROOT / nombre, index=False)
    print(f"Creado: {nombre}")


def main() -> None:
    guardar(
        "practica_book_rrhh.xlsx",
        [
            {"Empresa": "Demo Norte", "Periodo": "2026-08", "Cuenta": "5100001", "Debe": 5000000, "Haber": 0, "CentroCosto": "CC001"},
            {"Empresa": "Demo Norte", "Periodo": "2026-08", "Cuenta": "2105001", "Debe": 0, "Haber": 5000000, "CentroCosto": "CC001"},
            {"Empresa": "Demo Sur", "Periodo": "2026-08", "Cuenta": "5100001", "Debe": 3200000, "Haber": 0, "CentroCosto": "CC002"},
        ],
    )
    guardar(
        "practica_conciliacion_banco.xlsx",
        [
            {"Fecha": "2026-08-01", "Referencia": "NOM-001", "Descripcion": "Pago nomina", "Monto_Libro": 5000000, "Monto_Banco": 5000000},
            {"Fecha": "2026-08-05", "Referencia": "AFP-001", "Descripcion": "Pago AFP", "Monto_Libro": 800000, "Monto_Banco": 799500},
            {"Fecha": "2026-08-10", "Referencia": "COM-001", "Descripcion": "Comision bancaria", "Monto_Libro": 0, "Monto_Banco": 12000},
        ],
    )
    guardar(
        "practica_revision_cuentas.xlsx",
        [
            {"Cuenta": "5100001", "Glosa": "Sueldo base", "Debe": 5000000, "Haber": 0, "CentroCosto": "CC001"},
            {"Cuenta": "9999999", "Glosa": "Cuenta por validar", "Debe": 250000, "Haber": 0, "CentroCosto": "CC001"},
            {"Cuenta": "2105001", "Glosa": "AFP retenida", "Debe": 0, "Haber": 5250000, "CentroCosto": ""},
        ],
    )


if __name__ == "__main__":
    main()