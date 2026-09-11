# Recursos externos: Python, Excel y contabilidad

Los recursos se usan para aprender técnicas de procesamiento de datos. No deben tomarse como autoridad para decidir cuentas, impuestos, centros de costo o reglas de importación de Sofland.

## Documentación oficial

- [pandas: 10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html): DataFrame, limpieza, `concat`, `merge`, `groupby`, tablas dinámicas, fechas y Excel.
- [pandas.read_excel](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html): `skiprows`, `header`, `dtype`, `parse_dates`, `thousands`, `decimal` y lectura de hojas.
- [pandas.merge](https://pandas.pydata.org/docs/reference/api/pandas.merge.html): cruces, `indicator` y `validate` para detectar relaciones inesperadas.
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/): lectura y escritura de archivos `.xlsx`, estilos, hojas y celdas.

## Tutoriales prácticos

- [Real Python: pandas GroupBy](https://realpython.com/pandas-groupby/): agregaciones, agrupación por varias columnas, series temporales y rendimiento.
- [Real Python: limpieza con pandas y NumPy](https://realpython.com/python-data-cleaning-numpy-pandas/): columnas innecesarias, índices, texto, filas iniciales y normalización.
- [Real Python: lectura y escritura CSV](https://realpython.com/python-csv/): delimitadores, encabezados, fechas y transferencia entre archivos.
- [Real Python: combinar datos con merge, join y concat](https://realpython.com/pandas-merge-join-and-concat/): útil para consolidación y conciliación.
- [Real Python: Excel con openpyxl](https://realpython.com/openpyxl-excel-spreadsheets-python/): automatización de hojas y reportes.

## Cómo aplicar al sistema Sofland

| Técnica | Aplicación local | Ejemplo |
|---|---|---|
| `read_excel` + `skiprows` | quitar las cuatro filas iniciales de Sofland | limpieza de comprobantes |
| `concat` | unir empresas | consolidación multiempresa |
| `groupby` | resumir cuentas y centros de costo | tablas de control |
| `pivot_table` | análisis por empresa, cuenta y período | módulo de tablas dinámicas |
| `merge` + `indicator` | conciliar libro y cartola | cuadratura bancaria |
| `validate` | verificar cardinalidad de claves | controles antes de unir datos |
| `to_excel` | entregar reportes revisables | salida del cierre |

## Criterios de selección

1. Preferir documentación oficial para la sintaxis.
2. Usar tutoriales secundarios para ejemplos y explicaciones, no para reglas contables.
3. Adaptar cada ejemplo a datos sintéticos o anonimizados.
4. Registrar la fecha de consulta y la versión de las bibliotecas cuando un ejemplo pase a producción.
5. Probar casos normales, descuadres, duplicados, valores faltantes y formatos cambiantes.
