"""
pipeline_contable_completo.py
=============================
Pipeline integrado: genera, valida, analiza y reporta en una ejecución.

Flujo:
  1. Carga casos de ejemplo (empresa_*.xlsx o archivos especiales)
  2. Valida cada uno (detecta anomalías)
  3. Analiza (cuadratura, consolidación)
  4. Genera reporte Excel con 3 hojas:
     - Validación: anomalías detectadas
     - Análisis: resumen de cuadratura
     - Recomendaciones: próximos pasos

Ejecutar con:
    python pipeline_contable_completo.py
"""

import pandas as pd
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

from analizar_casos_contables import (
    detectar_fila_encabezado,
    leer_comprobante,
    revisar_comprobante,
)
from validar_datos_contables import ValidadorContable


class PipelineContable:
    """Orquesta la validación y análisis completo de casos contables."""

    def __init__(self, directorio: str = "."):
        self.directorio = Path(directorio)
        self.resultados = []
        self.validaciones = {}

    def procesar_archivo(self, ruta: Path) -> dict:
        """
        Procesa un archivo a través del pipeline completo.
        
        Retorna dict con:
          - nombre: nombre del archivo
          - validacion: anomalías encontradas
          - analisis: métricas de cuadratura
          - estado: "LISTO" / "REVISAR" / "ERROR"
        """
        resultado = {
            "nombre": ruta.name,
            "ruta": str(ruta),
            "validacion": None,
            "analisis": None,
            "estado": "REVISAR",
            "mensaje": "",
        }

        try:
            # PASO 1: VALIDACIÓN
            validador = ValidadorContable(str(ruta))
            validador.detectar_duplicados_exactos()
            validador.detectar_valores_faltantes()
            validador.detectar_caracteres_problematicos()
            validador.detectar_descuadres_tolerancia()
            validador.detectar_cuentas_invalidas()

            reporte_val = validador.obtener_reporte()
            resultado["validacion"] = reporte_val

            # PASO 2: ANÁLISIS DE CUADRATURA
            try:
                df = leer_comprobante(ruta)
                control = revisar_comprobante(df)
                resultado["analisis"] = control

                # Determinar estado
                si_cuadra = control.get("cuadrado", False)
                si_tiene_anomalias = reporte_val["anomalias"] > 0

                if si_cuadra and not si_tiene_anomalias:
                    resultado["estado"] = "LISTO"
                    resultado["mensaje"] = "✅ Sin anomalías detectadas"
                elif si_cuadra and si_tiene_anomalias:
                    resultado["estado"] = "REVISAR"
                    resultado["mensaje"] = f"⚠️ Cuadra pero tiene {reporte_val['anomalias']} anomalías"
                else:
                    resultado["estado"] = "ERROR"
                    resultado["mensaje"] = f"❌ Descuadre: {control.get('diferencia', 0):.0f}"

            except Exception as e:
                resultado["analisis"] = {"error": str(e)}
                resultado["estado"] = "ERROR"
                resultado["mensaje"] = f"❌ Error en análisis: {e}"

        except Exception as e:
            resultado["estado"] = "ERROR"
            resultado["mensaje"] = f"❌ Error al procesar: {e}"

        self.resultados.append(resultado)
        return resultado

    def ejecutar(self, patrones: list = None) -> list:
        """
        Ejecuta pipeline sobre archivos del directorio.
        
        Args:
            patrones: lista de patrones de glob (default: ["empresa*.xlsx", "caso_*.xlsx"])
        
        Returns:
            Lista de resultados procesados
        """
        if not patrones:
            patrones = [
                "empresa*.xlsx",
                "caso_duplicados.xlsx",
                "caso_valores_faltantes.xlsx",
                "caso_tolerancia.xlsx",
                "caso_conciliacion.xlsx",
            ]

        archivos = []
        for patron in patrones:
            archivos.extend(self.directorio.glob(patron))

        if not archivos:
            print(f"⚠️ No se encontraron archivos en {self.directorio}")
            return []

        print(f"📁 Procesando {len(archivos)} archivos...")
        print("=" * 70)

        for archivo in sorted(archivos):
            print(f"\n📄 {archivo.name}")
            resultado = self.procesar_archivo(archivo)
            estado = resultado["estado"]
            simbolo = "✅" if estado == "LISTO" else "⚠️" if estado == "REVISAR" else "❌"
            print(f"   {simbolo} {resultado['mensaje']}")

            if resultado["validacion"]:
                anoms = resultado["validacion"]["anomalias"]
                if anoms > 0:
                    print(f"      Anomalías: {anoms}")

            if resultado["analisis"] and "error" not in resultado["analisis"]:
                ctrl = resultado["analisis"]
                print(f"      Debe: ${ctrl.get('total_debe', 0):,.0f}")
                print(f"      Haber: ${ctrl.get('total_haber', 0):,.0f}")
                print(f"      Diferencia: ${ctrl.get('diferencia', 0):,.0f}")

        print("\n" + "=" * 70)
        return self.resultados

    def generar_reporte_excel(self, ruta_salida: str = None) -> Path:
        """Genera Excel con resumen del pipeline."""
        if not ruta_salida:
            ruta_salida = self.directorio.parent / "reportes" / "reporte_pipeline_completo.xlsx"

        ruta_salida = Path(ruta_salida)
        ruta_salida.parent.mkdir(exist_ok=True)

        wb = Workbook()

        # ── HOJA 1: RESUMEN ──
        ws_resumen = wb.active
        ws_resumen.title = "Resumen"

        ws_resumen.append(["REPORTE DE PIPELINE CONTABLE COMPLETO"])
        ws_resumen.append([])
        ws_resumen.append(["Métrica", "Valor"])
        ws_resumen.append(["Archivos Procesados", len(self.resultados)])
        ws_resumen.append(["Estado: LISTO", sum(1 for r in self.resultados if r["estado"] == "LISTO")])
        ws_resumen.append(["Estado: REVISAR", sum(1 for r in self.resultados if r["estado"] == "REVISAR")])
        ws_resumen.append(["Estado: ERROR", sum(1 for r in self.resultados if r["estado"] == "ERROR")])

        # Estilos
        for row in ws_resumen.iter_rows(min_row=1, max_row=1):
            for cell in row:
                cell.font = Font(bold=True, size=14)

        for row in ws_resumen.iter_rows(min_row=3, max_row=7):
            row[0].font = Font(bold=True)

        ws_resumen.column_dimensions['A'].width = 30
        ws_resumen.column_dimensions['B'].width = 15

        # ── HOJA 2: DETALLE DE ARCHIVOS ──
        ws_detalle = wb.create_sheet("Detalle")
        ws_detalle.append(["Archivo", "Estado", "Anomalías", "Cuadrado", "Diferencia", "Mensaje"])

        for resultado in self.resultados:
            anoms = resultado["validacion"]["anomalias"] if resultado["validacion"] else 0
            cuadrado = resultado["analisis"].get("cuadrado", "N/A") if resultado["analisis"] else "N/A"
            diferencia = resultado["analisis"].get("diferencia", 0) if resultado["analisis"] else 0

            ws_detalle.append([
                resultado["nombre"],
                resultado["estado"],
                anoms,
                cuadrado,
                f"${diferencia:,.0f}",
                resultado["mensaje"],
            ])

        # Estilos
        for row in ws_detalle.iter_rows(min_row=1, max_row=1):
            for cell in row:
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")

        ws_detalle.column_dimensions['A'].width = 25
        ws_detalle.column_dimensions['B'].width = 12
        ws_detalle.column_dimensions['C'].width = 12
        ws_detalle.column_dimensions['D'].width = 12
        ws_detalle.column_dimensions['E'].width = 15
        ws_detalle.column_dimensions['F'].width = 40

        # ── HOJA 3: RECOMENDACIONES ──
        ws_recom = wb.create_sheet("Recomendaciones")

        recomendaciones = [
            ("Verificación Manual Requerida", 
             "Los archivos en estado ERROR o REVISAR requieren revisión manual antes de procesamiento."),
            ("Duplicados", 
             "Eliminar filas duplicadas. Usar: df.drop_duplicates()"),
            ("Valores Faltantes", 
             "Rellenar o marcar. Campo 'cuenta' es crítico. Glosa puede tener valor por defecto."),
            ("Caracteres Especiales", 
             "Sanitizar usando sanitizar_texto(). Reemplaza ñ→n, á→a, etc."),
            ("Descuadres", 
             "Si < ±1000: tolerancia de redondeo (revisar). Si > ±1000: error de cálculo."),
            ("Centros de Costo", 
             "Si está vacío, usar valor por defecto según empresa. Documentar elección."),
            ("Próximo Paso Recomendado", 
             "1. Revisar ERROR. 2. Aprobar LISTO. 3. Resolver REVISAR manualmente."),
        ]

        for titulo, descripcion in recomendaciones:
            ws_recom.append([titulo, descripcion])
            ws_recom.row_dimensions[ws_recom.max_row].height = 40

        for row in ws_recom.iter_rows():
            row[0].font = Font(bold=True)
            row[0].alignment = Alignment(wrap_text=True, vertical="top")
            row[1].alignment = Alignment(wrap_text=True, vertical="top")

        ws_recom.column_dimensions['A'].width = 25
        ws_recom.column_dimensions['B'].width = 60

        wb.save(ruta_salida)
        return Path(ruta_salida)


if __name__ == "__main__":
    import sys

    directorio = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent

    print()
    print("=" * 70)
    print("  PIPELINE CONTABLE COMPLETO")
    print("=" * 70)

    pipeline = PipelineContable(directorio)
    resultados = pipeline.ejecutar()

    if resultados:
        ruta_reporte = pipeline.generar_reporte_excel()
        print(f"\n💾 Reporte guardado: {ruta_reporte.name}")
        print()
