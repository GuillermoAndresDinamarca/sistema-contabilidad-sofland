# Ejemplos prácticos

Esta carpeta contiene datos sintéticos y scripts de práctica. No deben
mezclarse aquí reportes de producción ni archivos con datos personales.

## Inicio rápido

Desde la raíz del proyecto:

```powershell
py -3 ejemplos/generar_ejemplos.py
py -3 ejemplos/generar_casos_especiales.py
py -3 ejemplos/generar_casos_practicos.py
py -3 ejemplos/primeros_codigos.py
py -3 ejemplos/analizar_casos_contables.py
py -3 ejemplos/validar_datos_contables.py
py -3 ejemplos/pipeline_contable_completo.py ejemplos
```

Antes de ejecutar, puedes pedir orientación directamente al programa:

```powershell
py -3 ejemplos/generar_ejemplos.py --help
py -3 ejemplos/analizar_casos_contables.py --help
py -3 ejemplos/ejecutar_ejemplos.py --help
```

La ayuda está pensada para una persona que conoce el proceso contable, pero no
recuerda todavía la sintaxis de Python.

Los Excel generados por los analizadores quedan en `reportes/`. Los archivos
de entrada permanecen en `ejemplos/`.

## Cómo leer los mensajes de la terminal

Cada programa informa tres cosas: **qué está leyendo**, **qué transformación
realiza** y **qué debes revisar**.

| Mensaje | Qué significa |
|---|---|
| `Archivo seleccionado` | El Excel que se usará en esta práctica. |
| `Filas de metadata` | Información inicial de Sofland, no movimientos contables. |
| `Filas útiles` | Registros que quedan después de limpiar. |
| `Debe`, `Haber` | Totales calculados desde las columnas numéricas. |
| `Diferencia` | `Debe - Haber`; no explica por sí sola la causa. |
| `CUADRA` | La diferencia está dentro de la tolerancia indicada. |
| `REVISAR` | Hay una diferencia que requiere inspección humana. |
| `Reporte generado` | Ruta del Excel que debes abrir para continuar. |

Si no sabes qué ejecutar, empieza por:

```powershell
py -3 ejemplos/primeros_codigos.py --help
py -3 ejemplos/ejecutar_ejemplos.py --help
```

### 0. Primeros códigos de Python

Antes de entrar a todos los módulos, ejecuta:

```powershell
py -3 ejemplos/primeros_codigos.py
```

El script muestra en consola leer, limpiar, calcular, agrupar y graficar.
Genera `reportes/primeros_codigos_empresae.xlsx` y
`reportes/primeros_codigos_empresae.png`.

Puedes cambiar el caso sin editar el código:

```powershell
py -3 ejemplos/primeros_codigos.py --empresa empresaa.xlsx
py -3 ejemplos/primeros_codigos.py --empresa empresae.xlsx --tolerancia 1000
py -3 ejemplos/primeros_codigos.py --empresa empresae.xlsx --salida clase_01
```

La primera orden muestra un caso que cuadra; la segunda permite conversar sobre
tolerancias; la tercera evita sobreescribir el nombre de salida de otra clase.

## Casos iniciales

### 1. EmpresaE descuadrada

`generar_ejemplos.py` crea cinco empresas. A-D cuadran y EmpresaE tiene una
diferencia intencional de $1.500.000.

```powershell
py -3 ejemplos/analizar_casos_contables.py
```

El analizador acepta otra carpeta y otro nombre de salida:

```powershell
py -3 ejemplos/analizar_casos_contables.py --entrada ejemplos/practica_3 --salida reportes/analisis_practica_3.xlsx
```

Revisar `reportes/reporte_analisis_contable.xlsx`, hoja `Control_empresas`.

### 1.1 Más o menos empresas, sin mezclar ejercicios

No conviene generar tres empresas dentro de la misma carpeta que ya contiene
cinco. Usa una carpeta aislada:

```powershell
py -3 ejemplos/generar_ejemplos.py --empresas 3 --sin-desbalance --periodo 2026-09 --salida ejemplos/practica_3
py -3 ejemplos/analizar_casos_contables.py --entrada ejemplos/practica_3 --salida reportes/analisis_practica_3.xlsx
```

Para volver a incluir un error conocido:

```powershell
py -3 ejemplos/generar_ejemplos.py --empresas 5 --periodo 2026-09 --salida ejemplos/practica_5
```

### 2. Duplicados y datos faltantes

`generar_casos_especiales.py` crea duplicados, cuentas vacías, glosas vacías y
centros de costo faltantes.

```powershell
py -3 ejemplos/validar_datos_contables.py
```

Revisar los archivos `reportes/validacion_*.xlsx`.

La conversación sugerida es: “¿El programa encontró un error técnico o una
decisión que todavía debe tomar un contador?”. Por ejemplo, una cuenta vacía es
un problema de calidad; elegir la cuenta correcta es una decisión contable.

### 3. Casos de Book, banco y cuentas

`generar_casos_practicos.py` crea tres archivos pequeños para iniciar:

- `practica_book_rrhh.xlsx`: columnas típicas de una exportación de remuneraciones.
- `practica_conciliacion_banco.xlsx`: movimientos con una diferencia intencional.
- `practica_revision_cuentas.xlsx`: cuenta desconocida y centro de costo faltante.

Estos archivos se pueden cargar en Streamlit, especialmente en consolidación,
tablas dinámicas y cuadratura bancaria.

## Orden recomendado para una persona nueva

1. Ejecutar `generar_ejemplos.py`.
2. Abrir una empresa y observar las cuatro filas iniciales de Sofland.
3. Usar **Limpiar Comprobantes**.
4. Cargar A-D en **Consolidar Empresas**.
5. Ejecutar el analizador y revisar EmpresaE por separado.
6. Ejecutar los casos especiales y clasificar cada hallazgo como error o aviso.
7. Cargar los casos prácticos en la interfaz y descargar los reportes.

Todos los resultados automáticos requieren revisión humana antes de importar
datos a Sofland.

## Recorrido por etapas

Para una demostración en clase no es necesario ejecutar todo:

```powershell
py -3 ejemplos/ejecutar_ejemplos.py --solo 01
py -3 ejemplos/ejecutar_ejemplos.py --desde 01 --hasta 03
py -3 ejemplos/ejecutar_ejemplos.py --desde 04
```

El log queda en `logs/` y resume qué etapa terminó, qué advertencias aparecieron
y dónde están los reportes. En una exposición, deténte después de cada etapa y
abre el Excel antes de continuar.

## Variaciones para practicar

1. Cambia una cuenta en un Excel sintético y observa el resumen por cuenta.
2. Duplica una fila y ejecuta el validador.
3. Borra un centro de costo y pregunta qué dato falta para decidir.
4. Genera tres empresas y luego cinco en carpetas separadas.
5. Cambia la tolerancia de `1` a `1000` y compara el estado.
6. Usa `practica_conciliacion_banco.xlsx` en el módulo de cuadratura.
7. Abre los gráficos generados y explica qué representa cada eje.

Nunca uses un dato real para aprender una operación nueva: primero reproduce el
caso con un Excel sintético y luego solicita aprobación para el piloto.