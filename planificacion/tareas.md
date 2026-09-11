# Backlog de Tareas (Por Hacer)

Este documento centraliza todas las tareas pendientes del proyecto, ordenadas por prioridad.
Cada tarea debe moverse a la sección "En Progreso" cuando se comience a trabajar en ella.

## 🔴 Alta Prioridad (Próximo Cierre)

- [ ] **T001**: Validar con Jocelyn los códigos exactos de las cuentas de beneficios en Sofland para actualizar el script generador de ejemplos.
- [ ] **T002**: Revisar el formato de exportación directo de Book (RRHH) para ver si la estructura de columnas coincide con el comparador actual.
- [ ] **T003**: Enseñar a un segundo analista (backup de Jocelyn) a ejecutar el script `INSTALAR.bat` y realizar el proceso completo en su máquina.
  - 📋 Documentación preparada; falta ejecutar la prueba en su computador.
- [ ] **T004**: Actualizar la regla de "skiprows" en la limpieza de Sofland si el formato de exportación cambia en la nueva actualización del ERP.

## 🟡 Media Prioridad (Próximo Trimestre)

- [x] **T005**: Investigar por qué Sofland rechaza comprobantes que tienen glosas con caracteres especiales (tildes, ñ) y añadir un sanitizador de texto al módulo de limpieza.
  - ✅ `validar_datos_contables.py` detecta y sanitiza caracteres problemáticos para revisión humana.
- [ ] **T006**: Agregar un gráfico de barras al Dashboard de la interfaz que muestre la evolución del total de remuneraciones mes a mes.
- [ ] **T007**: Personalizar las respuestas del Asistente Virtual para que incluya enlaces directos a videos tutoriales internos.

## 🟢 Baja Prioridad (Deseables a futuro)

- [ ] **T008**: Implementar un sistema de "Deshacer" por si el usuario consolida archivos equivocados por accidente.
- [ ] **T009**: Evaluar si es posible conectar la app directamente a la base de datos SQL de Sofland para evitar la exportación/importación de Excels por completo.
- [ ] **T010**: Configurar un cron job que ejecute la limpieza de la carpeta de "datos de entrada" cada 30 días para no acumular Excels antiguos.

## ⚙️ Automatización Fase 3

- [x] Crear scheduler diario para ejecutar el pipeline.
  - ✅ `planificacion/scheduler_contable.py` funciona con Windows Task Scheduler y cron.
  - ✅ Usa solo biblioteca estándar; no requiere instalar `schedule`.
  - ✅ Filtra reportes generados para no reprocesarlos como entradas.
- [x] Crear notificador de resultados.
  - ✅ `planificacion/notificador.py` genera alertas SMTP.
  - ✅ Modo simulación predeterminado; no envía correo sin `--enviar` y variables SMTP.
- [ ] Configurar credenciales SMTP y probar envío controlado con cuenta institucional.
- [ ] Instalar la tarea diaria en el equipo de operación y documentar el horario aprobado.

## 📦 Instalación y ejemplos

- [x] Documentar entrega por repositorio clonado, Docker Desktop y `INSTALAR.bat`.
- [x] Separar reportes generados en `reportes/` y evitar su reprocesamiento.
- [x] Documentar los ejemplos en `ejemplos/README.md` y en el manual de uso.
- [x] Agregar casos prácticos sintéticos para Book, banco y revisión de cuentas.
- [ ] Probar instalación desde un clon limpio en el equipo del segundo analista.
  - 📋 Pendiente porque Docker no está disponible en el entorno actual.
- [x] Agregar navegador de ejemplos a la interfaz Streamlit.
  - ✅ Permite seleccionar Excel, ver filas, tipos, nulos, memoria y gráficos.
- [x] Crear recorrido guiado con log.
  - ✅ `ejemplos/ejecutar_ejemplos.py` registra cada etapa y sus salidas.

## 🟣 Capacitación y ejemplos Python

- [x] **T011**: Ejecutar `ejemplos/generar_ejemplos.py` y validar que EmpresaE sea detectada como descuadrada.
  - ✅ Genera 5 empresas + cartola bancaria. EmpresaE detectada con diferencia de $1,500,000.
  
- [x] **T012**: Ejecutar `ejemplos/analizar_casos_contables.py` y revisar las cuatro hojas del reporte.
  - ✅ Reporte generado con 4 hojas: Control, Consolidado, Cuentas, Centros.
  - ✅ Confirmado: Empresas A-D cuadradas, EmpresaE descuadrada como esperado.
  
- [x] **T013**: Crear un caso sintético con duplicado de fila, cuenta vacía y centro de costo faltante.
  - ✅ Script `generar_casos_especiales.py` genera 4 casos:
    - caso_duplicados.xlsx (fila repetida)
    - caso_valores_faltantes.xlsx (cuenta/glosa/centro vacíos)
    - caso_tolerancia.xlsx (redondeo ±1000)
    - caso_conciliacion.xlsx (movimiento faltante)
  
- [x] **T014**: Crear un caso sintético de conciliación con clave acordada, movimiento faltante y diferencia por tolerancia.
  - ✅ Implementado en caso_conciliacion.xlsx (falta pago nómina, diferencia $5.22M).
  
- [ ] **T015**: Completar las sesiones 1 a 6 de `docs/ruta_aprendizaje_python_contabilidad.md` con evidencias y revisión humana.
  - 🔄 En progreso: laboratorio 2 creado en `laboratorios/lab_02_consolidacion_sofland.ipynb`.
  - ✅ Ejecutor guiado `ejemplos/ejecutar_ejemplos.py` registra cada etapa en `logs/`.
  - Próximo: crear y ejecutar labs 03-06 con estudiantes.
  
- [ ] **T016**: Validar con la persona responsable los códigos de cuenta, glosas y centros de costo antes de usar datos reales.
  - 📋 Pendiente: Reunión con Jocelyn para validar Plan de Cuentas.
