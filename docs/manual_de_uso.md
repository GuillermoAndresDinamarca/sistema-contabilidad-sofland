# Manual de Uso — Sistema de Contabilidad Sofland

**Versión 1.0 · Área de Remuneraciones**

---

## ¿Para quién es este manual?

Para el equipo del Área de Remuneraciones que necesita procesar el cierre mensual
sin conocimientos de programación. Todo se opera con el mouse desde el navegador web.

---

## Primeros pasos: cómo abrir el sistema

### Si es la primera vez

1. Asegúrate de que Docker Desktop esté instalado _(ver sección "Instalación")_.
2. Haz **doble clic** en el archivo **`INSTALAR.bat`**.
3. Espera 2-5 minutos mientras el sistema se prepara (solo la primera vez).
4. El navegador Chrome o Edge se abrirá automáticamente con el sistema listo.

### Para uso diario (después de la primera instalación)

1. Haz **doble clic** en **`INSTALAR.bat`**.
2. El sistema se inicia en menos de 30 segundos.
3. Si el navegador no se abre solo, escribe esto en la barra de direcciones:
   ```
   http://localhost:8501
   ```

### Para cerrar el sistema al terminar

1. Haz **doble clic** en **`DETENER.bat`**.
2. El sistema se apaga de forma segura.

> [!NOTE]
> El sistema **no requiere internet** para funcionar una vez instalado.
> Todos los datos se procesan en tu propio computador.

## Instalar el sistema en otro computador

La entrega recomendada es el enlace del repositorio Git. La persona destinataria
debe clonar el repositorio completo, no solo el `Dockerfile`:

```powershell
git clone <URL_DEL_REPOSITORIO>
Set-Location sistema-contabilidad-sofland
.\INSTALAR.bat
```

También puede descargar el repositorio como ZIP y descomprimir todas sus carpetas.
Debe tener Docker Desktop abierto antes de ejecutar `INSTALAR.bat`. El script
construye la imagen, inicia Streamlit y abre `http://localhost:8501`.

Para cerrar el sistema se ejecuta `DETENER.bat`. La primera construcción requiere
internet para descargar la imagen base y dependencias; después el uso diario es
local, salvo que se reconstruya la imagen.

## Usar los ejemplos de práctica

Los ejemplos son sintéticos y no contienen remuneraciones reales. Desde la raíz
del proyecto, en PowerShell, ejecutar:

```powershell
py -3 ejemplos/generar_ejemplos.py
py -3 ejemplos/generar_casos_especiales.py
py -3 ejemplos/generar_casos_practicos.py
```

### Primera práctica recomendada

1. Abrir la aplicación con `INSTALAR.bat`.
2. Entrar a **Limpiar Comprobantes** y cargar `empresaa.xlsx`.
3. Confirmar que desaparecen las cuatro filas iniciales del encabezado Sofland.
4. Entrar a **Consolidar Empresas** y cargar `empresaa.xlsx` a `empresad.xlsx`.
5. Descargar el consolidado y revisar que aparece la empresa de origen.
6. Entrar a **Tablas Dinámicas** y agrupar por `Cuenta` y `CentroCosto`.
7. Entrar a **Cuadratura Bancaria** con `cartola_banco.xlsx` para practicar la
   revisión de diferencias.

### Segunda práctica: detectar errores

Ejecutar:

```powershell
py -3 ejemplos/validar_datos_contables.py
```

Revisar los casos `caso_duplicados.xlsx`, `caso_valores_faltantes.xlsx`,
`caso_tolerancia.xlsx` y `caso_conciliacion.xlsx`. Los reportes quedan en la
carpeta `reportes/`. Un estado `ERROR` o `REVISAR` no se corrige automáticamente:
la persona responsable debe revisar el comprobante y aprobar la acción.

### Tercera práctica: ejecutar el pipeline

```powershell
py -3 ejemplos/analizar_casos_contables.py
py -3 ejemplos/pipeline_contable_completo.py ejemplos
```

Abrir `reportes/reporte_analisis_contable.xlsx` y
`reportes/reporte_pipeline_completo.xlsx`. EmpresaE debe aparecer con un
descuadre intencional de $1.500.000. Este resultado es una prueba del sistema,
no una instrucción contable para datos reales.

---

## Navegación principal

La pantalla tiene dos zonas:

| Zona | Descripción |
|------|-------------|
| **Panel izquierdo (Sidebar)** | Menú de navegación. Haz clic en cualquier módulo para abrirlo. |
| **Área central** | Contenido del módulo seleccionado. Aquí subes archivos, ves resultados y descargas reportes. |

---

## Módulo 1: Panel Principal 🏠

Al entrar al sistema, verás el panel de control con:

- **Tarjetas de métricas**: resumen del estado del cierre (tiempo estimado, empresas pendientes).
- **Tabla del Flujo de Cierre**: los 5 pasos del proceso con el tiempo esperado.
- **Alertas de Cuentas Críticas**: recordatorios sobre aguinaldo, finiquito y vacaciones.

**No necesitas hacer nada aquí.** Es solo un resumen visual.

---

## Módulo 2: Limpiar Comprobantes 🧹

**¿Para qué sirve?**
Cuando exportas un comprobante desde Sofland, el archivo trae 4 filas iniciales
con el nombre del sistema, la fecha y tu usuario. Estas filas impiden usarlo directamente.
Este módulo las elimina automáticamente.

**Pasos:**
1. Haz clic en **"Browse files"** (o arrastra el archivo al recuadro).
2. Selecciona uno o varios archivos Excel de Sofland.
3. El sistema muestra una vista previa "Antes" y "Después".
4. Haz clic en **"📥 Descargar"** para obtener el archivo limpio.

**Resultado:** Un Excel sin las filas de encabezado, listo para importar o consolidar.

> [!TIP]
> Puedes subir los 5 archivos de las empresas al mismo tiempo.
> El sistema los limpia todos a la vez.

---

## Módulo 3: Consolidar Empresas 🔗

**¿Para qué sirve?**
Une los libros de remuneraciones de las 5 empresas (A, B, C, D, E) en un solo archivo.
Reemplaza el proceso de copy-paste manual que tomaba hasta 3 horas.

**Pasos:**
1. Haz clic en **"Browse files"**.
2. Selecciona los archivos de las **5 empresas simultáneamente** (mantén Ctrl presionado para seleccionar varios).
3. Haz clic en **"🔗 Consolidar Ahora"**.
4. Revisa el resumen por empresa (con estado ✅ o ⚠️).
5. Descarga el libro consolidado.

**Resultado:** Un único Excel con todos los registros y una columna `_empresa_origen`.

> [!WARNING]
> Si un archivo muestra ⚠️ **Descuadre** en el resumen por empresa,
> ese archivo tiene diferencias entre el Debe y el Haber. Revísalo antes de continuar.

---

## Módulo 4: Tablas Dinámicas 📊

**¿Para qué sirve?**
Genera resúmenes automáticos de los datos (como las Tablas Dinámicas de Excel,
pero sin tener que construirlas manualmente). Útil para el análisis de los
13.000 colaboradores.

**Pasos:**
1. Sube el libro consolidado (del paso anterior).
2. Selecciona las **columnas de filas** (ej: Cuenta, Empresa).
3. Selecciona las **columnas de valores** (ej: Debe, Haber).
4. Haz clic en **"📊 Generar Pivot"**.
5. Revisa el resultado e identifica las filas marcadas como ⚠️ o 🚨.
6. Descarga el pivot para adjuntar al reporte de cierre.

**Indicadores de estado:**
| Símbolo | Significado |
|---------|-------------|
| ✅ OK | Saldo dentro de tolerancia aceptable |
| ⚠️ Descuadre | Diferencia menor, revisar |
| 🚨 Revisar | Diferencia significativa, no continuar sin revisar |

---

## Módulo 5: Cuadratura Bancaria ⚖️

**¿Para qué sirve?**
Compara el total del libro contable con el total de la cartola bancaria
para verificar que coincidan.

**Pasos:**
1. Sube el **Libro Contable / Consolidado** en el recuadro izquierdo.
2. Sube la **Cartola Bancaria** en el recuadro derecho.
3. Haz clic en **"🔍 Ejecutar Cuadratura"**.
4. El sistema muestra los totales y la diferencia.

**Resultados posibles:**
| Resultado | Qué hacer |
|-----------|-----------|
| 🎉 Cuadratura Perfecta | Puedes proceder con la importación a Sofland |
| ⚠️ Diferencia menor | Revisar transacciones de los últimos días del período |
| 🚨 Descuadre significativo | No importar a Sofland. Buscar la cuenta con error |

---

## Módulo 6: Asistente Virtual 🤖

**¿Para qué sirve?**
Un chatbot que responde preguntas sobre el proceso de cierre mensual en lenguaje natural.

**Cómo usarlo:**
1. Escribe tu consulta en el campo de texto inferior.
2. Presiona **Enter** o el botón **"Enviar"**.
3. El asistente te guiará al módulo correcto o explicará cómo resolver el problema.

**Ejemplos de preguntas que puedes hacer:**
- *"¿Cómo limpio los comprobantes de Sofland?"*
- *"El libro no cuadra con el banco, ¿qué hago?"*
- *"¿Dónde van las glosas de aguinaldo?"*
- *"Quiero consolidar las 5 empresas"*

---

## Módulo 7: Orquestador Completo ⚡

**¿Para qué sirve?**
Ejecuta **todo el pipeline de cierre en un solo clic**: limpieza → consolidación
→ tablas dinámicas → cuadratura. Ideal para el primer procesamiento del mes.

**Pasos:**
1. Sube todos los archivos de las empresas (puedes subir varios a la vez).
2. Haz clic en **"🚀 Ejecutar Pipeline Completo"**.
3. Espera. El sistema mostrará el progreso en tiempo real.
4. Revisa las 3 pestañas de resultados:
   - **📋 Consolidado**: todos los registros unidos.
   - **📊 Pivot**: tablas dinámicas automáticas.
   - **🚨 Descuadres**: registros que necesitan revisión humana.
5. Descarga el **Reporte Completo de Cierre** (un solo Excel con todo).

---

## Preguntas frecuentes (FAQ)

**¿Se pierden mis datos si cierro el sistema?**
Los reportes descargados se guardan donde tú los descargues. Los archivos que subes
al sistema son temporales y no se almacenan. Siempre descarga el resultado antes de cerrar.

**¿Puedo usar el sistema mientras otro compañero también lo usa?**
Si el sistema está instalado en un servidor de la empresa (ver `planificacion/fases.md`),
varios usuarios pueden usarlo al mismo tiempo desde sus propios navegadores.

**¿Funciona con archivos de Book (RRHH)?**
El sistema acepta cualquier archivo Excel. Si el archivo de Book no tiene las columnas
estándar (Cuenta, Debe, Haber), el módulo de Tablas Dinámicas te pedirá que selecciones
manualmente cuáles columnas usar.

**¿Qué pasa si subo un archivo con formato incorrecto?**
El sistema mostrará un mensaje de error describiendo el problema. Generalmente
se debe a que el archivo está en formato `.xls` antiguo. En ese caso, ábrelo en Excel,
guárdalo como `.xlsx` y vuelve a subirlo.

---

## Solución de problemas comunes

| Problema | Solución |
|----------|----------|
| El sistema no abre en el navegador | Verifica que Docker Desktop esté corriendo (ícono en la barra de tareas) |
| "Error de conexión" en el navegador | Espera 30 segundos y recarga la página (F5) |
| El archivo no se sube | Verifica que sea `.xlsx` (no `.xls` ni `.csv`) |
| Descuadre inesperado | Revisa que no hayas subido el mismo archivo de empresa dos veces |
| El sistema está muy lento | Cierra otras aplicaciones pesadas (Chrome con muchas pestañas, Teams, etc.) |
