"""
Sistema de Contabilidad - Sofland / Jocelyn
============================================
Módulo de lógica del asistente virtual de diálogo.
Basado en los requerimientos levantados en la reunión con Jocelyn (Área de Remuneraciones).

Problemas reales que resuelve:
  - 12 horas de cierre mensual → objetivo: 4 horas
  - Copy-paste de comprobantes de 5 empresas (13.000 colaboradores)
  - Eliminación manual de 4 filas de encabezado antes de cargar a Sofland
  - Cuadratura de Debe/Haber con errores frecuentes
  - Glosas incorrectas en cuentas de aguinaldo, finiquito y vacaciones
  - Falta de integración automática entre Book (RRHH) y Sofland (Contabilidad)
"""

INTENCIONES = {
    "limpiar": [
        "comprobante", "encabezado", "cabecera", "linea", "limpiar", "titulo",
        "4 filas", "cuatro filas", "sofland", "cargar archivo", "importar"
    ],
    "consolidar": [
        "consolidar", "empresas", "juntar", "unir", "múltiples", "archivos",
        "5 empresas", "cinco empresas", "libro", "centraliz"
    ],
    "cuadratura": [
        "cuadratura", "cuadrar", "descuadre", "descuadrar", "diferencia",
        "debe", "haber", "balance", "saldo", "error contable", "validar"
    ],
    "glosas": [
        "glosa", "aguinaldo", "finiquito", "vacacion", "cuenta incorrecta",
        "imputacion", "clase de documento", "centro de costo"
    ],
    "book_sofland": [
        "book", "integracion", "hrr", "recursos humanos", "plantilla",
        "no comunica", "exportar", "importar a book"
    ],
    "cierre": [
        "cierre", "plazo", "2pm", "14h", "tiempo", "horas", "auditor",
        "auditoria", "reportabilidad", "mes", "agosto", "septiembre"
    ],
    "analisis_cuentas": [
        "analisis de cuenta", "13000", "13.000", "colaboradores", "pivot",
        "tabla dinamica", "reporte", "saldo", "reporte de saldo"
    ],
    "ayuda": [
        "ayuda", "no se", "como", "que hago", "que modulo", "como funciona"
    ]
}

RESPUESTAS = {
    "limpiar": (
        "Para limpiar los comprobantes de Sofland, usa el módulo **🧹 Limpieza de Comprobantes**.\n\n"
        "El sistema detecta automáticamente cuántas filas de encabezado tiene el archivo "
        "(generalmente 4: logo, fecha, usuario y separador) y las elimina antes de procesar. "
        "Solo arrastra tu Excel y haz clic en **Procesar**. El archivo resultante ya estará "
        "listo para importar directamente a Sofland sin error."
    ),
    "consolidar": (
        "Para consolidar los libros de las empresas, usa el módulo **🔗 Consolidación Multiempresa**.\n\n"
        "Puedes subir los 5 archivos de las empresas (A, B, C, D, E) simultáneamente. "
        "El sistema los une, estandariza los formatos y entrega un único Excel consolidado "
        "con una columna `Empresa` que indica el origen de cada fila. "
        "Esto reemplaza el proceso manual de copy-paste que tomaba hasta 3 horas."
    ),
    "cuadratura": (
        "Para verificar la cuadratura, usa el módulo **⚖️ Cuadratura y Balances**.\n\n"
        "El sistema cruza automáticamente el Debe vs. Haber por cuenta y empresa. "
        "Si hay un descuadre, aparecerá marcado en **rojo** con el monto exacto de la diferencia. "
        "También puedes cargar la cartola bancaria para hacer la conciliación banco-libro. "
        "Esto evita el error frecuente de buscar diferencias manualmente en 2.000 líneas."
    ),
    "glosas": (
        "Los problemas de glosas y cuentas incorrectas ocurren frecuentemente con conceptos como "
        "aguinaldo, finiquito y vacaciones, que a veces se imputan a la cuenta general de remuneraciones "
        "en lugar de la cuenta de beneficios correcta.\n\n"
        "El módulo **📊 Análisis de Cuentas** tiene validaciones predefinidas: si una glosa contiene "
        "'aguinaldo' pero la cuenta es de remuneraciones generales (ej. 5100001), el sistema "
        "te alertará antes de que hagas la carga. Esto permite defender el registro ante los auditores."
    ),
    "book_sofland": (
        "La falta de integración entre Book (RRHH) y Sofland (Contabilidad) es uno de los problemas "
        "más complejos. Actualmente el sistema incluye el módulo **🔄 Comparar Book vs Sofland**, "
        "que normaliza las columnas de ambos sistemas y compara sus totales.\n\n"
        "El proceso sugerido es:\n"
        "1. Exportar desde Book el libro de remuneraciones.\n"
        "2. Exportar desde Sofland el comprobante del período.\n"
        "3. Cargar ambos en el comparador para detectar discrepancias antes de la carga masiva."
    ),
    "cierre": (
        "El objetivo del sistema es que puedas completar el cierre mensual dentro de tu carga "
        "permitida de 4 horas (cerrando a las 2 PM) en lugar de las 12 horas actuales.\n\n"
        "Para lograrlo, el flujo recomendado es:\n"
        "1. **8:00 AM** → Limpiar comprobantes de las 5 empresas (automatizado, ~5 min)\n"
        "2. **8:10 AM** → Consolidar en un solo libro (automatizado, ~2 min)\n"
        "3. **8:15 AM** → Ejecutar cuadratura automática (automatizado, ~3 min)\n"
        "4. **8:20 AM** → Revisar descuadres detectados (revisión humana, ~30-60 min)\n"
        "5. **10:00 AM** → Importar a Sofland (validado y listo)\n\n"
        "Usa el módulo **⚡ Orquestador** para ejecutar los pasos 1-3 en un solo clic."
    ),
    "analisis_cuentas": (
        "Para el análisis de cuentas de los 13.000 colaboradores, usa el módulo **📊 Tablas Dinámicas**.\n\n"
        "El sistema genera automáticamente:\n"
        "- **Pivot por Cuenta**: resumen de Debe/Haber/Saldo para cada cuenta contable.\n"
        "- **Pivot por Empresa y Cuenta**: desagregado por sucursal.\n"
        "- **Pivot por Centro de Costo**: equivalente al análisis que hacías manualmente con las plantillas.\n\n"
        "Este proceso, que tomaba hasta 12 horas manualmente, se ejecuta en segundos."
    ),
    "ayuda": (
        "Puedo ayudarte con las siguientes tareas del cierre mensual:\n\n"
        "• **Limpiar comprobantes** de Sofland → Módulo 1\n"
        "• **Consolidar múltiples empresas** → Módulo 2\n"
        "• **Generar tablas dinámicas** (Pivots) → Módulo 3\n"
        "• **Conciliación bancaria** → Módulo 4\n"
        "• **Comparar Book vs Sofland** → Módulo Integración\n"
        "• **Cuadratura automática** → Módulo Cuadratura\n"
        "• **Ejecutar todo el pipeline** → Orquestador\n\n"
        "Cuéntame en qué parte del proceso estás y te guío al módulo correcto."
    ),
}

RESPUESTA_DEFAULT = (
    "No estoy seguro de entender exactamente tu consulta. "
    "Recuerda que puedo ayudarte con:\n"
    "• Limpiar encabezados de Sofland\n"
    "• Consolidar libros de múltiples empresas\n"
    "• Cuadratura y validación de cuentas\n"
    "• Análisis de glosas (aguinaldos, finiquitos, vacaciones)\n"
    "• Comparar Book vs Sofland\n\n"
    "¿Podrías reformular tu pregunta o indicarme en qué etapa del cierre estás?"
)


def detectar_intencion(mensaje: str) -> str:
    """Detecta la intención del mensaje buscando palabras clave."""
    msg = mensaje.lower()
    for intencion, palabras in INTENCIONES.items():
        if any(palabra in msg for palabra in palabras):
            return intencion
    return "default"


def generar_respuesta(mensaje: str) -> str:
    """Genera una respuesta basada en el mensaje del usuario."""
    intencion = detectar_intencion(mensaje)
    return RESPUESTAS.get(intencion, RESPUESTA_DEFAULT)


def modo_consola():
    """Ejecuta el asistente en modo texto desde la terminal."""
    print("=" * 60)
    print("  ASISTENTE CONTABLE - Sistema Sofland / Jocelyn")
    print("  (escribe 'salir' para terminar)")
    print("=" * 60)
    print("\nAsistente: ¡Hola Jocelyn! Estoy listo para ayudarte con")
    print("  el cierre mensual. ¿En qué te puedo ayudar hoy?\n")

    historial = []
    while True:
        try:
            entrada = input("Tú: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAsistente: ¡Hasta luego! Buen cierre mensual.")
            break

        if entrada.lower() in ("salir", "exit", "quit"):
            print("Asistente: ¡Hasta luego! Buen cierre mensual.")
            break
        if not entrada:
            continue

        historial.append({"rol": "usuario", "mensaje": entrada})
        respuesta = generar_respuesta(entrada)
        historial.append({"rol": "asistente", "mensaje": respuesta})
        print(f"\nAsistente: {respuesta}\n")

    return historial


if __name__ == "__main__":
    modo_consola()
