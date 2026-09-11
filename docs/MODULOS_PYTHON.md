# Módulos Python — Guía Técnica

**Última actualización:** 2025-09-10  
**Ubicación:** `ejemplos/`

## Visión General

Los módulos Python en esta carpeta están diseñados para:
1. **Generar** casos de prueba sintéticos (Empresas A-E)
2. **Validar** datos de entrada (detectar anomalías)
3. **Analizar** cuadratura contable (Debe vs Haber)
4. **Reportar** hallazgos en Excel estructurado

Cada módulo es **independiente** (puede ejecutarse solo) y **reutilizable** (importable como librería).

---

## 1️⃣ `generar_ejemplos.py`

**Propósito:** Crear 5 casos de prueba sintéticos + cartola bancaria.

**Salida:**
- `empresaa.xlsx` — Empresa A (9 registros, cuadrada)
- `empresab.xlsx` — Empresa B (11 registros, cuadrada)
- `empresac.xlsx` — Empresa C (9 registros, cuadrada)
- `empresad.xlsx` — Empresa D (7 registros, cuadrada)
- `empresae.xlsx` — Empresa E (10 registros, **descuadrada $1.5M**)
- `cartola_banco.xlsx` — Extracto bancario (80 movimientos)

**Uso:**
```bash
python generar_ejemplos.py
```

**Características:**
- Encabezado Sofland incluido en cada archivo (4 filas de "basura")
- Empresa E tiene descuadre intencional para practicar detección
- Datos reproducibles (semilla `seed=42`)
- Estructura: Cuenta, Glosa, Debe, Haber, CentroCosto

**Casos de uso:**
- ✅ Práctica con dados reales (no confidenciales)
- ✅ Validación de que el analizador detecta errores
- ✅ Material para capacitación del equipo

---

## 2️⃣ `analizar_casos_contables.py`

**Propósito:** Analizar archivos Excel y verificar cuadratura.

**Entrada:** Archivos `empresa*.xlsx` en la misma carpeta.

**Salida:**
- `reporte_analisis_contable.xlsx` con 4 hojas:
  1. **Control_empresas:** Tabla de control (filas, duplicados, descuadres)
  2. **Consolidado:** Totales globales Debe/Haber
  3. **Resumen_cuentas:** Agregación por Cuenta + Glosa
  4. **Resumen_centros:** Agregación por Centro de Costo

**Uso:**
```bash
python analizar_casos_contables.py
```

**Funciones internas:**
- `detectar_fila_encabezado(path, max_rows=12)` — Busca fila donde empiezan datos
- `leer_comprobante(path)` — Lee Excel, normaliza, convierte a float
- `revisar_comprobante(frame)` — Retorna dict con controles
- `resumen_por_cuenta(frame)` — Agrupa por Cuenta + Glosa
- `resumen_por_centro_de_costo(frame)` — Agrupa por Centro de Costo

**Importar para uso personalizado:**
```python
from analizar_casos_contables import leer_comprobante, revisar_comprobante

df = leer_comprobante("empresa_A.xlsx")
control = revisar_comprobante(df)
print(f"Debe: ${control['debe_total']:,.0f}")
print(f"Haber: ${control['haber_total']:,.0f}")
print(f"Cuadra: {control['cuadrado']}")
```

---

## 3️⃣ `validar_datos_contables.py`

**Propósito:** Detección avanzada de anomalías y sanitización.

**Anomalías que detecta:**
- ❌ **Duplicados exactos:** Fila idéntica repetida
- ❌ **Valores faltantes:** Cuenta/Glosa/Centro vacíos
- ⚠️ **Caracteres especiales:** Tildes (á, ñ), símbolos problemáticos
- ⚠️ **Descuadres por tolerancia:** Diferencia ±1000 pesos
- ❌ **Descuadres significativos:** Diferencia > 1000 pesos
- ⚠️ **Cuentas inválidas:** No coinciden patrón (7 dígitos)

**Uso individual:**
```bash
python validar_datos_contables.py archivo.xlsx
```

**Uso en lote (todos los casos especiales):**
```bash
python validar_datos_contables.py
```

**Salida:**
- Imprime resumen en consola
- Genera `validacion_<archivo>.xlsx` con anomalías y recomendaciones

**Importar para uso personalizado:**
```python
from validar_datos_contables import ValidadorContable

validador = ValidadorContable("empresa_A.xlsx")
validador.detectar_duplicados_exactos()
validador.detectar_valores_faltantes()
validador.detectar_caracteres_problematicos()

reporte = validador.obtener_reporte()
print(f"Anomalías: {reporte['anomalias']}")
print(f"Errores: {reporte['errores']}")
print(f"Avisos: {reporte['avisos']}")

validador.generar_excel_anomalias()
```

**Sanitización:**
```python
texto = "Pago Aguinaldo Fiestas Patrias - Año 2024"
limpio = validador.sanitizar_texto(texto)
# → "Pago Aguinaldo Fiestas Patrias - Ano 2024"
```

---

## 4️⃣ `generar_casos_especiales.py`

**Propósito:** Crear casos de prueba con errores específicos.

**Casos generados:**
1. **caso_duplicados.xlsx:** Fila idéntica repetida (error común en importación)
2. **caso_valores_faltantes.xlsx:** Cuenta vacía, Glosa vacía, Centro de Costo vacío
3. **caso_tolerancia.xlsx:** Descuadre de $1000 (dentro de tolerancia de redondeo)
4. **caso_conciliacion.xlsx:** Movimiento faltante ($5.22M de descuadre)

**Uso:**
```bash
python generar_casos_especiales.py
```

**Propósito pedagógico:**
- ✅ Aprender a reconocer patrones de error
- ✅ Practicar corrección manual de datos
- ✅ Validar que detección funciona en casos reales

---

## 5️⃣ `pipeline_contable_completo.py`

**Propósito:** Orquestar flujo completo: validación → análisis → reporte.

**Flujo:**
1. Detecta todos los archivos `empresa*.xlsx` y `caso_*.xlsx`
2. **Para cada archivo:**
   - Valida anomalías
   - Analiza cuadratura
   - Asigna estado: "LISTO" / "REVISAR" / "ERROR"
3. Genera reporte Excel con 3 hojas

**Uso:**
```bash
python pipeline_contable_completo.py ejemplos/
```

**Salida:**
- `reporte_pipeline_completo.xlsx` con:
  1. **Resumen:** Conteo por estado
  2. **Detalle:** Archivo, Estado, Anomalías, Cuadratura
  3. **Recomendaciones:** Guía de próximos pasos

**Clasificación de estados:**
- 🟢 **LISTO:** Cuadra + sin anomalías
- 🟡 **REVISAR:** Cuadra pero tiene anomalías (revisar antes de procesar)
- 🔴 **ERROR:** Descuadre o error crítico (requer revisión manual)

**Importar para uso personalizado:**
```python
from pipeline_contable_completo import PipelineContable

pipeline = PipelineContable("ejemplos/")
resultados = pipeline.ejecutar()

for resultado in resultados:
    print(f"{resultado['nombre']}: {resultado['estado']}")

pipeline.generar_reporte_excel("salida/reporte_custom.xlsx")
```

---

## 🔄 Flujo Recomendado

### Para Capacitación
```bash
# Paso 1: Generar casos de prueba
python generar_ejemplos.py

# Paso 2: Analizar casos
python analizar_casos_contables.py
# → Revisar reporte_analisis_contable.xlsx

# Paso 3: Generar casos con errores
python generar_casos_especiales.py

# Paso 4: Validar detección de errores
python validar_datos_contables.py

# Paso 5: Ejecutar pipeline completo
python pipeline_contable_completo.py ejemplos/
# → Revisar reporte_pipeline_completo.xlsx
```

### Para Operación (Futuro)
```bash
# Copia Excel del cierre a ejemplos/
# Ejecuta pipeline integrado
python pipeline_contable_completo.py ejemplos/

# Revisa reporte de estado
# Si TODO está "LISTO" → proceder con importación a Sofland
# Si alguno está "REVISAR" o "ERROR" → corrección manual antes de importar
```

---

## 📊 Esquema de Datos

### Formato esperado (después de limpiar encabezado)

| Cuenta  | Glosa                    | Debe      | Haber     | CentroCosto   |
|---------|--------------------------|-----------|-----------|---------------|
| 5100001 | Sueldo base agosto       | 5000000.0 | 0.0       | CC001-Admin   |
| 5100002 | Horas extras agosto      | 800000.0  | 0.0       | CC002-Operac  |
| 2105001 | AFP retenida agosto      | 0.0       | 580000.0  | (vacío)       |
| 1101001 | Pago nómina masiva       | 0.0       | 5220000.0 | (vacío)       |

**Requisitos:**
- `Cuenta`: Código de 7 dígitos (ej: 5100001)
- `Debe` y `Haber`: Números (convertidos a float automáticamente)
- `Glosa`: Texto descriptivo (puede contener tildes)
- `CentroCosto`: Texto o vacío (si es vacío → usar valor por defecto)

---

## 🐛 Troubleshooting

### "No hay empresa_*.xlsx"
**Causa:** Los archivos de prueba no existen.  
**Solución:** Ejecuta `python generar_ejemplos.py` primero.

### "No se encontró encabezado contable"
**Causa:** El archivo no tiene las columnas esperadas (Cuenta, Debe, Haber).  
**Solución:** Verifica que el archivo sea de Sofland o tenga estructura correcta.

### Valores de Debe/Haber en 0
**Causa:** Las columnas están como texto, no como números.  
**Solución:** Asegúrate que Excel los tenga como "Número" (no texto).

### "Caracter especial detectado: 'Pago nómina'"
**Advertencia:** Las ñ, tildes, etc. pueden causar rechazo en Sofland.  
**Solución:** Usar `sanitizar_texto()` antes de importar.

---

## 📚 Lecturas Relacionadas

- [Ruta de aprendizaje Python](../docs/ruta_aprendizaje_python_contabilidad.md)
- [Recursos Python, Excel y contabilidad](../docs/recursos_python_contabilidad.md)
- [Tutorial completo](../docs/tutorial.md)
