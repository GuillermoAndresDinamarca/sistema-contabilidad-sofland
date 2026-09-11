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

Los Excel generados por los analizadores quedan en `reportes/`. Los archivos
de entrada permanecen en `ejemplos/`.

### 0. Primeros códigos de Python

Antes de entrar a todos los módulos, ejecuta:

```powershell
py -3 ejemplos/primeros_codigos.py
```

El script muestra en consola leer, limpiar, calcular, agrupar y graficar.
Genera `reportes/primeros_codigos_empresae.xlsx` y
`reportes/primeros_codigos_empresae.png`.

## Casos iniciales

### 1. EmpresaE descuadrada

`generar_ejemplos.py` crea cinco empresas. A-D cuadran y EmpresaE tiene una
diferencia intencional de $1.500.000.

```powershell
py -3 ejemplos/analizar_casos_contables.py
```

Revisar `reportes/reporte_analisis_contable.xlsx`, hoja `Control_empresas`.

### 2. Duplicados y datos faltantes

`generar_casos_especiales.py` crea duplicados, cuentas vacías, glosas vacías y
centros de costo faltantes.

```powershell
py -3 ejemplos/validar_datos_contables.py
```

Revisar los archivos `reportes/validacion_*.xlsx`.

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