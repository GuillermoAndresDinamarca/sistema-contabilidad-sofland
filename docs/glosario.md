# Glosario — Sistema de Contabilidad Sofland

Diccionario de términos contables y del sistema, ordenado alfabéticamente.
Diseñado para que cualquier miembro del equipo pueda consultar cuando encuentre
un término desconocido en el sistema o en los reportes.

---

## Términos Contables

### A

**Aguinaldo**
Beneficio en dinero que se paga a los trabajadores en fechas especiales (Fiestas Patrias
y Navidad). En el sistema, se valida que su glosa esté asociada a la cuenta `4105`
(Beneficios) y **no** a la cuenta `5100` (Remuneraciones Generales).

**Análisis de Cuentas**
Proceso de revisar el movimiento detallado de una cuenta contable durante un período,
identificando todos los registros que la componen. En el sistema, este proceso se
genera automáticamente con el módulo de **Tablas Dinámicas**.

**Asiento Contable**
Registro de una transacción en el libro contable. Siempre tiene al menos una línea
de Debe y una de Haber, y ambas deben sumar lo mismo (principio de partida doble).

### B

**Balance**
Estado financiero que muestra los activos, pasivos y patrimonio de una empresa en un
momento determinado. El cierre mensual contribuye a preparar el balance.

**Book (Sistema RRHH)**
Sistema de Recursos Humanos que genera la información de remuneraciones. No se comunica
automáticamente con Sofland (Sistema Contable), lo que genera el proceso manual que
este sistema busca automatizar.

### C

**Centralización**
Proceso de consolidar todos los comprobantes individuales de las empresas en un solo
libro contable. El módulo **Consolidar Empresas** automatiza este proceso.

**Centro de Costo**
Código que identifica a qué área o departamento se imputa un gasto. Ejemplos:
`CC001-Admin`, `CC002-Operaciones`. Errores en el centro de costo generan reportes
financieros incorrectos por área.

**Cierre Mensual**
Proceso de registrar y verificar todas las transacciones de un mes para cerrar
el período contable. Incluye la carga de remuneraciones, verificación de cuadratura
y preparación de reportes para auditoría.

**Clase de Documento**
Código de 2 letras que clasifica el tipo de comprobante. En el sistema:
- `RE` → Remuneraciones (gastos de personal)
- `PA` → Pago (salida de dinero al banco)
- `PV` → Provisión (obligación estimada)

**Comprobante**
Documento digital que respalda un asiento contable. En Sofland, se exportan como
archivos Excel con 4 filas de encabezado que hay que eliminar antes de procesar.

**Conciliación Bancaria** → *ver Cuadratura Bancaria*

**Cuadratura**
Verificación de que el total del Debe sea igual al total del Haber en un conjunto
de registros contables. Si no cuadra, hay un error en el registro. El módulo
**Cuadratura Bancaria** lo detecta automáticamente.

**Cuadratura Bancaria**
Proceso específico de comparar el saldo del libro contable con el saldo de la
cartola bancaria para verificar que coincidan. Las diferencias pueden ocurrir por
transacciones en tránsito o errores de registro.

### D

**Debe**
En partida doble, el Debe representa el lado izquierdo de una cuenta contable.
Registra entradas de activos o gastos. En el sistema, la columna `Debe` contiene
los montos del lado deudor.

**Descuadre**
Diferencia entre el total del Debe y el total del Haber. Un descuadre indica un
error de registro. En el sistema, los descuadres se marcan con ⚠️ o 🚨 según su magnitud.

### F

**Finiquito**
Pago que se hace a un trabajador al término de su contrato laboral. Incluye
indemnizaciones, vacaciones pendientes y otros conceptos. En el sistema, se valida
que la glosa indique si es "Rol General" o "Rol Privado" para defensa ante auditoría.

### G

**Glosa**
Descripción textual de un asiento contable que explica el concepto del movimiento.
Ejemplo: `"Sueldo base agosto colaboradores"`. Las glosas incorrectas o ambiguas
dificultan las auditorías. El asistente virtual puede ayudar a identificar glosas problemáticas.

**Gasto Anticipado**
Monto pagado que corresponde a un gasto de períodos futuros. Ejemplo: aguinaldo
de Navidad pagado en noviembre. Se registra como un activo transitorio hasta que
se devenga.

### H

**Haber**
En partida doble, el Haber representa el lado derecho de una cuenta contable.
Registra salidas de activos o ingresos. En el sistema, la columna `Haber` contiene
los montos del lado acreedor.

### I

**Impuesto Único de Segunda Categoría (IUSC)**
Impuesto que se aplica a las remuneraciones de los trabajadores dependientes en Chile.
Se retiene mensualmente y se declara al SII. En el sistema, aparece en la cuenta `2105003`.

### L

**Libro de Remuneraciones**
Registro mensual de todos los sueldos, descuentos y haberes de los trabajadores de
una empresa. Puede tener hasta 300 columnas según las necesidades de RRHH.

### N

**Nómina Masiva**
Procesamiento del pago de sueldos para todos los colaboradores de una empresa
en un solo lote. Para 13.000 colaboradores, este proceso genera archivos Excel grandes
que el sistema maneja automáticamente.

### P

**Partida Doble**
Principio contable fundamental: toda transacción afecta al menos dos cuentas,
y el total del Debe siempre debe ser igual al total del Haber.

**Plan de Cuentas**
Listado ordenado de todas las cuentas contables que usa una empresa, con sus códigos
y descripciones. Ejemplo: `5100001 - Remuneraciones Sueldo Base`.

**Período Contable**
Intervalo de tiempo (generalmente un mes) al que corresponden los registros contables.
En el sistema, el período se indica como `YYYY-MM` (ejemplo: `2024-08`).

**Pivot / Tabla Dinámica**
Resumen agrupado de datos que muestra totales por categorías. El módulo **Tablas Dinámicas**
genera pivots automáticamente a partir del libro consolidado.

**Provisionamiento**
Registro anticipado de un gasto o ingreso que se espera ocurra en el futuro.
Ejemplo: provisión de vacaciones devengadas no tomadas.

### R

**Remuneraciones**
Todo pago que recibe un trabajador por sus servicios. Incluye sueldo base, horas extra,
bonos, aguinaldos y otros beneficios.

**Rol de Remuneraciones**
Lista detallada de las remuneraciones de los trabajadores en un período, con todos
los haberes y descuentos. En el sistema, puede ser "Rol General" o "Rol Privado".

### S

**Saldo**
Diferencia entre el Debe y el Haber de una cuenta. Saldo deudor: Debe > Haber.
Saldo acreedor: Haber > Debe. En el sistema, el saldo se calcula automáticamente
en las Tablas Dinámicas.

**SII (Servicio de Impuestos Internos)**
Institución del Estado chileno que administra los tributos. El cierre mensual
debe producir información coherente con las declaraciones al SII.

**Sofland**
Sistema ERP (Enterprise Resource Planning) de contabilidad utilizado por la empresa.
Sus exportaciones de comprobantes incluyen 4 filas de encabezado que el sistema elimina automáticamente.

### V

**Vacaciones**
Beneficio legal de descanso pagado. Las vacaciones devengadas no tomadas se
provisionan mensualmente. En el sistema, se registran en la cuenta `2300001`.

---

## Términos del Sistema

| Término | Significado |
|---------|-------------|
| **Docker** | Tecnología que empaqueta el sistema con todo lo necesario para que funcione en cualquier computador sin instalar Python |
| **Contenedor** | Instancia en ejecución del sistema dentro de Docker |
| **Puerto 8501** | Dirección de red interna donde corre el sistema (`localhost:8501`) |
| **Streamlit** | Tecnología usada para construir la interfaz web del sistema |
| **Pipeline** | Secuencia automática de pasos del proceso (limpieza → consolidación → pivot → cuadratura) |
| **Orquestador** | Módulo que ejecuta el pipeline completo en un solo clic |
| **`_empresa_origen`** | Columna que el sistema agrega automáticamente al consolidar, indicando de qué archivo viene cada fila |
| **`skiprows`** | Número de filas que el sistema salta al leer un archivo (generalmente 4, para ignorar el encabezado de Sofland) |
| **Dato Sintético** | Dato de ejemplo generado artificialmente para practicar, que no corresponde a información real de la empresa |
