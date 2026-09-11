# Tutorial Didáctico — Cierre de Remuneraciones de Agosto

**Caso real: Empresa A, B, C, D y E · Período 2024-08**

Este tutorial te lleva paso a paso por un cierre mensual completo usando los archivos
de ejemplo incluidos en la carpeta `ejemplos/`. Al terminar, habrás practicado todo
el flujo que el sistema automatiza.

---

## Antes de empezar

1. Inicia el sistema (doble clic en `INSTALAR.bat`).
2. Abre la carpeta `ejemplos/` en tu computador.
3. Verifica que existen estos archivos:
   - `empresaa.xlsx`, `empresab.xlsx`, `empresac.xlsx`, `empresad.xlsx`, `empresae.xlsx`
   - `cartola_banco.xlsx`

> [!NOTE]
> Si los archivos de ejemplo no existen todavía, el equipo de soporte puede generarlos
> ejecutando `python ejemplos/generar_ejemplos.py` desde la terminal.

---

## PASO 1 — Entender el problema (5 min)

Abre `empresaa.xlsx` en Excel. Notarás que las primeras 4 filas son "basura":

```
Fila 1: SISTEMA SOFLAND S.A.
Fila 2: Fecha Impresión: 10/09/2024
Fila 3: Usuario: JOCELYN.CONTABILIDAD
Fila 4: ──────────────────────────────────────
Fila 5: Cuenta | Glosa_Cuenta | Debe | Haber ← ¡Aquí empiezan los datos reales!
```

Si intentas hacer una Tabla Dinámica directamente, Excel no reconoce las columnas.
**Éste es el primer problema que el sistema resuelve.**

Cierra Excel y vuelve al sistema en el navegador.

---

## PASO 2 — Limpiar los comprobantes (5 min)

1. En el menú izquierdo, haz clic en **🧹 Limpiar Comprobantes**.
2. Haz clic en el recuadro de carga de archivos.
3. Selecciona **los 5 archivos** de empresas (`empresaa.xlsx` hasta `empresae.xlsx`).
   - En Windows: mantén la tecla **Ctrl** mientras haces clic en cada archivo.
4. Verás que aparecen 5 bloques desplegables, uno por empresa.
5. Haz clic en el primero (`empresaa.xlsx`) para expandirlo.

**¿Qué observas?**
- La columna A ahora dice `Cuenta`, no `SISTEMA SOFLAND S.A.`
- Las filas de basura desaparecieron
- El sistema detectó que había que saltar 4 filas

6. Descarga cada archivo limpio haciendo clic en los botones **"📥 Descargar"**.

> [!TIP]
> Guarda los archivos limpios en una carpeta llamada `agosto_limpio/` para tenerlos organizados.

---

## PASO 3 — Consolidar las 5 empresas (3 min)

1. Haz clic en **🔗 Consolidar Empresas**.
2. Sube los **5 archivos limpios** que descargaste en el paso anterior.
3. Haz clic en **"🔗 Consolidar Ahora"**.

**¿Qué observas en el resumen?**

| Empresa | Estado esperado |
|---------|----------------|
| EmpresaA | ✅ Cuadrado |
| EmpresaB | ✅ Cuadrado |
| EmpresaC | ✅ Cuadrado |
| EmpresaD | ✅ Cuadrado |
| **EmpresaE** | **⚠️ Descuadre** ← ¡Aquí hay un error intencional! |

4. EmpresaE tiene un descuadre de `$1.500.000`. Esto simula el tipo de error
   que puede ocurrir cuando una cuenta de costo se usa incorrectamente.
5. Para este tutorial, **continúa de todas formas** para ver cómo el orquestador lo detecta.
6. Descarga el libro consolidado.

---

## PASO 4 — Generar las Tablas Dinámicas (3 min)

1. Haz clic en **📊 Tablas Dinámicas**.
2. Sube el libro consolidado que descargaste.
3. En **"columnas de filas"**, selecciona: `_empresa_origen` y `Cuenta`.
4. En **"columnas de valores"**, selecciona: `Debe` y `Haber`.
5. Haz clic en **"📊 Generar Pivot"**.

**¿Qué ves?**
- Una tabla con el resumen por empresa y cuenta contable.
- La fila de EmpresaE / cuenta `5100001` aparecerá con estado **🚨 Revisar**.
- El valor de Debe es `$1.500.000` mayor que el Haber → Confirma el descuadre.

6. Descarga el pivot.

---

## PASO 5 — Cuadratura con el banco (3 min)

1. Haz clic en **⚖️ Cuadratura Bancaria**.
2. Sube el **libro consolidado** en el recuadro izquierdo.
3. Sube **`cartola_banco.xlsx`** en el recuadro derecho.
4. Haz clic en **"🔍 Ejecutar Cuadratura"**.

Como la cartola es sintética y generada independientemente del libro,
lo más probable es que haya una diferencia. Esto es **normal** en este tutorial
y simula la situación real: el banco registra los montos cuando se efectúan,
no cuando se contabilizan.

**Resultado esperado:** Diferencia moderada → ⚠️ *Diferencia menor detectada*.

---

## PASO 6 — Usar el Asistente para resolver la duda (2 min)

1. Haz clic en **🤖 Asistente Virtual**.
2. Escribe: `"El descuadre de EmpresaE es de $1.500.000, ¿qué pudo haber pasado?"`
3. El asistente te explicará las causas más comunes: imputación incorrecta de cuenta,
   doble registro, o un finiquito que falta su contrapartida.

---

## PASO 7 — Pipeline completo en un clic (2 min)

Ahora que entiendes cada paso, prueba el Orquestador:

1. Haz clic en **⚡ Orquestador Completo**.
2. Sube los 5 archivos de empresas originales (con encabezado, sin limpiar).
3. Haz clic en **"🚀 Ejecutar Pipeline Completo"**.
4. Observa cómo los 4 pasos anteriores se ejecutan automáticamente.
5. Revisa las 3 pestañas y descarga el reporte final.

**¡Felicitaciones!** Completaste el cierre de agosto para las 5 empresas.

---

## Resumen del tiempo ahorrado

| Tarea | Antes (manual) | Con el sistema |
|-------|---------------|---------------|
| Limpiar 5 comprobantes | ~1 hora | 2 minutos |
| Consolidar 5 empresas | ~3 horas | 30 segundos |
| Generar tablas dinámicas | ~4 horas | 10 segundos |
| Detectar descuadre | ~2 horas | Automático |
| **Total** | **~10 horas** | **~35 minutos** |

---

## ¿Qué sigue?

- Practica con tus archivos reales del próximo cierre.
- Si un archivo real da error, revisa el `manual_de_uso.md`, sección "Solución de problemas".
- Consulta el `glosario.md` si encuentras términos que no conoces del sistema.
- Si quieres agregar nuevas funcionalidades, revisa `planificacion/tareas.md`.

## Ejercicio adicional: análisis reproducible

Después de generar los ejemplos, ejecuta desde la raíz del proyecto:

```powershell
python ejemplos\analizar_casos_contables.py
```

El script crea `ejemplos/reporte_analisis_contable.xlsx` con cuatro hojas:

- `Control_empresas`: filas, cuentas vacías, duplicados, Debe, Haber y diferencia.
- `Consolidado`: todos los comprobantes con archivo de origen.
- `Resumen_cuentas`: agrupación por cuenta y diferencia absoluta.
- `Resumen_centros`: agrupación por centro de costo.

Usa este reporte para practicar una revisión antes de importar a Sofland. La empresa E contiene un descuadre intencional y debe quedar observada.

Para ampliar la ruta, consulta `docs/ruta_aprendizaje_python_contabilidad.md` y `docs/recursos_python_contabilidad.md`.
