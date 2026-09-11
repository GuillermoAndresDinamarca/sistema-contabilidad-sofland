"""
validar_datos_contables.py
==========================
Módulo de validación avanzada de datos contables.

Proporciona:
  - Detección de duplicados exactos
  - Detección de caracteres especiales problemáticos
  - Validación de rangos de cuentas
  - Detección de tolerancias (redondeo)
  - Sugerencias de corrección
  - Reporte Excel con anomalías

Uso:
    python validar_datos_contables.py <archivo.xlsx>
"""

import sys
import re
import pandas as pd
import numpy as np
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows


class ValidadorContable:
    """Valida datos contables contra reglas de negocio y formato."""

    def __init__(self, ruta_archivo: str, skiprows: int = 4, tolerancia_pesos: float = 1000.0):
        """
        Inicializa validador.

        Args:
            ruta_archivo: Path al archivo Excel
            skiprows: Filas de encabezado a saltarse (default: 4 de Sofland)
            tolerancia_pesos: Diferencia máxima permitida por redondeo (default: 1000)
        """
        self.ruta = Path(ruta_archivo)
        self.skiprows = skiprows
        self.tolerancia = tolerancia_pesos
        self.df = None
        self.anomalias = []
        self._cargar_datos()

    def _cargar_datos(self):
        """Carga el archivo Excel saltándose encabezados."""
        try:
            self.df = pd.read_excel(self.ruta, skiprows=self.skiprows)
            # Normalizar nombres de columna
            self.df.columns = [c.strip().lower() for c in self.df.columns]
        except Exception as e:
            raise ValueError(f"Error al cargar {self.ruta}: {e}")

    def _agregar_anomalia(self, tipo: str, fila: int = None, columna: str = None, 
                          detalle: str = "", severidad: str = "AVISO"):
        """Registra una anomalía encontrada."""
        self.anomalias.append({
            "tipo": tipo,
            "fila": fila,
            "columna": columna,
            "detalle": detalle,
            "severidad": severidad,
        })

    # ──────────────────────────────────────────────────────────

    def detectar_duplicados_exactos(self):
        """Detecta filas idénticas (error común en importación)."""
        duplicados = self.df.duplicated(keep=False)
        if duplicados.any():
            grupos_dup = self.df[duplicados].groupby(list(self.df.columns)).size()
            for idx, (grupo, count) in enumerate(grupos_dup.items()):
                if count > 1:
                    self._agregar_anomalia(
                        tipo="DUPLICADO_EXACTO",
                        fila=idx,
                        columna="*",
                        detalle=f"Fila idéntica repetida {count} veces",
                        severidad="ERROR"
                    )

    def detectar_valores_faltantes(self):
        """Detecta celdas vacías en columnas críticas."""
        criticas = ["cuenta", "debe", "haber"]
        for col in criticas:
            if col not in self.df.columns:
                continue
            vacios = self.df[self.df[col].isna()]
            for idx, row in vacios.iterrows():
                self._agregar_anomalia(
                    tipo="VALOR_FALTANTE",
                    fila=int(idx) + self.skiprows,
                    columna=col.upper(),
                    detalle=f"Valor {col} vacío en fila {idx}",
                    severidad="ERROR"
                )

    def detectar_caracteres_problematicos(self):
        """Detecta caracteres especiales que Sofland rechaza."""
        # Patrón: tildes y caracteres no ASCII en ciertos campos
        patron_problematico = re.compile(r"[^\x00-\x7F]|[<>\"'\\/:?*|]")
        
        campos_verificar = ["glosa", "descripcion"]
        for col in campos_verificar:
            if col not in self.df.columns:
                continue
            for idx, valor in enumerate(self.df[col]):
                if pd.notna(valor) and patron_problematico.search(str(valor)):
                    self._agregar_anomalia(
                        tipo="CARACTER_ESPECIAL",
                        fila=int(idx) + self.skiprows,
                        columna=col.upper(),
                        detalle=f"Detectado: {repr(str(valor)[:50])}",
                        severidad="AVISO"
                    )

    def detectar_descuadres_tolerancia(self):
        """Detecta descuadres dentro de tolerancia de redondeo."""
        if "debe" not in self.df.columns or "haber" not in self.df.columns:
            return

        total_debe = self.df["debe"].sum()
        total_haber = self.df["haber"].sum()
        diferencia = abs(total_debe - total_haber)

        if 0 < diferencia <= self.tolerancia:
            self._agregar_anomalia(
                tipo="DESCUADRE_TOLERANCIA",
                fila=None,
                columna="*",
                detalle=f"Diferencia {diferencia:.0f} dentro de tolerancia ±{self.tolerancia:.0f}",
                severidad="AVISO"
            )
        elif diferencia > self.tolerancia:
            self._agregar_anomalia(
                tipo="DESCUADRE_SIGNIFICATIVO",
                fila=None,
                columna="*",
                detalle=f"Diferencia {diferencia:.0f} SUPERA tolerancia",
                severidad="ERROR"
            )

    def detectar_cuentas_invalidas(self, cuenta_pattern: str = r"^\d{7}$"):
        """Detecta códigos de cuenta que no siguen el patrón esperado."""
        if "cuenta" not in self.df.columns:
            return

        for idx, valor in enumerate(self.df["cuenta"]):
            if pd.isna(valor):
                continue
            if not re.match(cuenta_pattern, str(valor)):
                self._agregar_anomalia(
                    tipo="CUENTA_INVALIDA",
                    fila=int(idx) + self.skiprows,
                    columna="CUENTA",
                    detalle=f"Formato inesperado: {valor}",
                    severidad="AVISO"
                )

    # ──────────────────────────────────────────────────────────

    def sanitizar_texto(self, texto: str) -> str:
        """
        Sanitiza texto eliminando caracteres problemáticos.
        
        Reemplaza:
          - Tildes (á→a, é→e, etc.)
          - Caracteres especiales problemáticos (→-_)
        """
        if not isinstance(texto, str):
            return texto
        
        # Mapeo de caracteres acentuados a ASCII
        mapa_acentos = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
            'ñ': 'n', 'Ñ': 'N',
        }
        
        # Aplicar mapeo
        for char, reemplazo in mapa_acentos.items():
            texto = texto.replace(char, reemplazo)
        
        # Reemplazar caracteres especiales problemáticos
        texto = re.sub(r'[<>\"\'\\/:?*|]', '-', texto)
        
        return texto

    def obtener_reporte(self) -> dict:
        """Retorna reporte estructurado de anomalías."""
        return {
            "archivo": str(self.ruta.name),
            "filas_totales": len(self.df),
            "anomalias": len(self.anomalias),
            "errores": sum(1 for a in self.anomalias if a["severidad"] == "ERROR"),
            "avisos": sum(1 for a in self.anomalias if a["severidad"] == "AVISO"),
            "detalle": self.anomalias,
        }

    def generar_excel_anomalias(self, ruta_salida: str = None):
        """Genera Excel con lista de anomalías y sugerencias."""
        if not ruta_salida:
            ruta_salida = self.ruta.parent.parent / "reportes" / f"validacion_{self.ruta.stem}.xlsx"

        ruta_salida = Path(ruta_salida)
        ruta_salida.parent.mkdir(exist_ok=True)

        wb = Workbook()
        ws = wb.active
        ws.title = "Anomalías"

        # Encabezados
        encabezados = ["Tipo", "Fila", "Columna", "Severidad", "Detalle"]
        ws.append(encabezados)

        # Estilos
        for col_num, encabezado in enumerate(encabezados, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            cell.alignment = Alignment(horizontal="center", vertical="center")

        # Datos
        for anom in self.anomalias:
            fila_num = anom.get("fila", "—")
            ws.append([
                anom["tipo"],
                fila_num,
                anom.get("columna", "—"),
                anom["severidad"],
                anom["detalle"]
            ])

        # Ancho de columnas
        ws.column_dimensions['A'].width = 25
        ws.column_dimensions['B'].width = 8
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 12
        ws.column_dimensions['E'].width = 50

        # Hoja: Resumen
        ws_resumen = wb.create_sheet("Resumen")
        reporte = self.obtener_reporte()
        ws_resumen.append(["Métrica", "Valor"])
        ws_resumen.append(["Archivo", reporte["archivo"]])
        ws_resumen.append(["Filas Totales", reporte["filas_totales"]])
        ws_resumen.append(["Anomalías Detectadas", reporte["anomalias"]])
        ws_resumen.append(["Errores", reporte["errores"]])
        ws_resumen.append(["Avisos", reporte["avisos"]])

        wb.save(ruta_salida)
        return Path(ruta_salida)


# ────────────────────────────────────────────────────────────

def validar_archivo(ruta: str):
    """Función principal para validar un archivo."""
    print(f"\n📋 Validando: {ruta}")
    print("=" * 60)

    try:
        validador = ValidadorContable(ruta)

        # Ejecutar todas las validaciones
        validador.detectar_duplicados_exactos()
        validador.detectar_valores_faltantes()
        validador.detectar_caracteres_problematicos()
        validador.detectar_descuadres_tolerancia()
        validador.detectar_cuentas_invalidas()

        # Mostrar resultados
        reporte = validador.obtener_reporte()
        print(f"\n  Filas totales: {reporte['filas_totales']}")
        print(f"  Anomalías detectadas: {reporte['anomalias']}")
        print(f"    • Errores: {reporte['errores']}")
        print(f"    • Avisos: {reporte['avisos']}")

        if reporte['anomalias'] > 0:
            print("\n  Anomalías encontradas:")
            for anom in reporte['detalle']:
                simbolo = "❌" if anom['severidad'] == "ERROR" else "⚠️"
                fila_str = f"L{anom['fila']}" if anom['fila'] else "Global"
                print(f"    {simbolo} {anom['tipo']} ({fila_str}) — {anom['detalle']}")

        # Generar Excel
        ruta_salida = validador.generar_excel_anomalias()
        print(f"\n  💾 Reporte guardado: {ruta_salida.name}")

    except Exception as e:
        print(f"  ❌ Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        validar_archivo(sys.argv[1])
    else:
        # Validar casos especiales
        print("=" * 60)
        print("  VALIDADOR DE DATOS CONTABLES")
        print("=" * 60)

        ejemplos = [
            "caso_duplicados.xlsx",
            "caso_valores_faltantes.xlsx",
            "caso_tolerancia.xlsx",
            "caso_conciliacion.xlsx",
        ]

        for ejemplo in ejemplos:
            ruta = Path(__file__).parent / ejemplo
            if ruta.exists():
                validar_archivo(str(ruta))
            else:
                print(f"\n⚠️ No encontrado: {ejemplo}")

        print("\n" + "=" * 60)
