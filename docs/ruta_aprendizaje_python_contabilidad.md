# Ruta de aprendizaje: Python para contabilidad con Sofland

Esta ruta usa los ejemplos sintéticos del sistema. Cada ejercicio produce evidencia y exige revisión humana; Python no reemplaza la aprobación contable.

## Nivel 1: leer y limpiar

**Archivo:** `ejemplos/analizar_casos_contables.py`

Objetivos:

- Detectar encabezados Sofland con `read_excel` y `skiprows`.
- Normalizar nombres de columnas y valores numéricos.
- Identificar columnas faltantes, cuentas vacías y filas duplicadas.
- Calcular totales Debe, Haber y diferencia.

Ejercicio:

1. Ejecuta primero `python ejemplos/generar_ejemplos.py`.
2. Abre `empresa_A.xlsx` y localiza las cuatro filas iniciales de metadatos.
3. Ejecuta `python ejemplos/analizar_casos_contables.py`.
4. Revisa la hoja `Control_empresas`.
5. Explica por qué `EmpresaE` no debe continuar sin revisión.

## Nivel 2: consolidar y resumir

Objetivos:

- Combinar empresas con `pd.concat`.
- Agrupar por cuenta y centro de costo.
- Construir una tabla de control con totales, registros y diferencias.
- Separar datos originales, transformados y reportes.

Ejercicio:

- Compara el total consolidado por empresa con el resumen de la interfaz.
- Ordena `Resumen_cuentas` por valor absoluto de diferencia.
- Investiga si una cuenta concentra el descuadre o si se distribuye entre varias.
- Compara centros de costo y documenta qué información falta para interpretarlos.

## Nivel 3: conciliación y relaciones

Conceptos a practicar:

- `merge` entre libro y cartola mediante una clave acordada.
- `indicator=True` para distinguir coincidencias y faltantes.
- `validate="one_to_one"` o `validate="many_to_one"` cuando la regla de negocio lo permita.
- Tolerancia explícita para diferencias de redondeo.
- Registro de movimientos no conciliados.

No inventar la clave de conciliación: antes se debe definir con la persona responsable si será referencia, fecha+monto, documento, cuenta u otra combinación.

## Nivel 4: calidad y trazabilidad

Agregar al análisis:

- Conteo de filas de entrada y salida.
- Archivos procesados y fecha de ejecución.
- Columnas faltantes y valores no convertibles.
- Duplicados detectados.
- Casos no procesados.
- Regla y tolerancia usadas.
- Responsable de revisión.
- Resultado aprobado, observado o rechazado.

## Nivel 5: transferencia al trabajo real

Antes de usar un archivo real:

1. Confirmar códigos de cuenta y centros de costo.
2. Confirmar clases de documento y glosas válidas.
3. Comparar una muestra manual con el resultado automático.
4. Mantener datos anonimizados durante el desarrollo.
5. Guardar entrada, versión del script y salida.
6. Registrar quién aprueba la importación a Sofland.

## Secuencia recomendada de sesiones

El laboratorio 2 implementa la sesión de consolidación con explicaciones,
tablas intermedias y gráficos:

- `laboratorios/lab_02_consolidacion_sofland.ipynb`
- `laboratorios/lab_03_conciliacion_movimientos.ipynb`
- `py -3 ejemplos/ejecutar_ejemplos.py` para recorrer todo el flujo con log.

| Sesión | Tema | Evidencia |
|---|---|---|
| 1 | Leer y limpiar Excel Sofland | notebook o script reproducible |
| 2 | Consolidar empresas | libro consolidado y conteo de filas |
| 3 | Cuadratura Debe/Haber | reporte de diferencias |
| 4 | Agrupar por cuenta y centro de costo | tablas de control |
| 5 | Conciliar con cartola | coincidencias y pendientes |
| 6 | Pipeline y revisión humana | manifiesto, checklist y propuesta |
