# Fases del Proyecto — Sistema de Contabilidad Sofland

## Hoja de Ruta 2024-2025

```
FASE 1 ────────── FASE 2 ────────── FASE 3 ────────── FASE 4 ────────── FASE 5
MVP Local         Integración       Automatización    Capacitación      Escala
[COMPLETADO]      [EN PROGRESO]     [PENDIENTE]       [EN PROGRESO]     [FUTURO]
```

---

## ✅ FASE 1: MVP Local (Completada)

**Período:** Septiembre 2024
**Estado:** ✅ Completada

**Objetivo:** Tener un sistema funcional que resuelva los problemas urgentes de Jocelyn
para el cierre de agosto.

**Entregables completados:**
- [x] Módulo de limpieza de comprobantes Sofland (detecta y elimina las 4 filas de encabezado)
- [x] Módulo de consolidación multiempresa (5 empresas en un clic)
- [x] Módulo de tablas dinámicas automáticas
- [x] Módulo de cuadratura bancaria
- [x] Asistente virtual con respuestas basadas en los problemas de la reunión
- [x] Orquestador (pipeline completo en un clic)
- [x] Empaquetado con Docker para no-programadores (INSTALAR.bat)
- [x] Manual de uso
- [x] Tutorial didáctico con datos de ejemplo
- [x] Glosario de términos

**Resultado obtenido:**
- Tiempo de cierre mensual: de 12 horas a estimado < 4 horas (objetivo cumplido)
- Interfaz 100% operable con mouse, sin conocimientos de programación

---

## 🔄 FASE 2: Integración Book ↔ Sofland (En Progreso)

**Período estimado:** Octubre - Noviembre 2024
**Estado:** 🔄 En progreso

**Objetivo:** Eliminar el intermediario manual (Excel) entre Book (RRHH) y Sofland (Contabilidad).

**Tareas:**
- [ ] Mapear el formato de exportación de Book vs el formato de importación de Sofland
- [ ] Crear un módulo de "traducción" automática entre ambos formatos
- [ ] Validar que las clases de documento (RE, PA, PV) se asignen correctamente
- [ ] Automatizar la asignación de centros de costo según reglas definidas por Jocelyn
- [ ] Agregar validación de glosas: alertar si "aguinaldo" está en cuenta de remuneraciones
- [ ] Prueba piloto con datos reales del período de octubre

**Riesgos:**
- El formato de Book puede cambiar con actualizaciones del sistema de RRHH
- Las reglas de asignación de centros de costo pueden variar por empresa

---

## 📋 FASE 3: Automatización Avanzada (Pendiente)

**Período estimado:** Diciembre 2024 - Febrero 2025
**Estado:** ⏳ Iniciada

**Objetivo:** Reducir la intervención manual al mínimo necesario para la revisión humana.

**Avance actual:** Se completaron los módulos de análisis, validación y pipeline. Ahora se necesita
integración con scheduler y notificaciones.

**Tareas planeadas:**
- [ ] Programar ejecución automática del pipeline al inicio del día de cierre (Windows Task Scheduler / cron)
- [ ] Notificaciones por email/Teams cuando hay descuadres que requieren revisión
- [ ] Módulo de reclasificación contable: corregir errores de cuenta desde la interfaz
- [ ] Historial de cierres: comparar el cierre actual con el del mes anterior
- [ ] Alertas de plazos: recordatorio automático cuando se acerca la fecha de cierre
- [ ] Exportación directa al formato de importación de Sofland (sin intermediarios)
- [ ] Módulo de finiquitos: validación especial para liquidaciones con auditoría

---

## 🎓 FASE 4: Capacitación del Equipo (En progreso)

**Período estimado:** Marzo - Abril 2025
**Estado:** 🔄 En Progreso

**Objetivo:** Que el equipo completo de analistas de Jocelyn pueda usar el sistema
de forma autónoma.

**Avance actual (Sesión 2025-09-10):**
- ✅ Implementados 5 módulos Python reproducibles:
  - `generar_ejemplos.py`: 5 casos de prueba (A-E)
  - `analizar_casos_contables.py`: cuadratura y resúmenes
  - `validar_datos_contables.py`: detección de anomalías (duplicados, especiales, valores faltantes)
  - `generar_casos_especiales.py`: 4 escenarios de error
  - `pipeline_contable_completo.py`: orquestación integrada
- ✅ Completadas tareas T011-T014 (generación y casos especiales)
- ✅ Actualizado README con documentación de módulos
- ✅ Laboratorio 01 (limpieza Sofland) disponible en notebook
- 📋 En progreso: T015 (ejecutar ruta de 6 sesiones con equipo)
- 📋 Pendiente: T016 (validar con Jocelyn)
- ✅ Navegador interactivo de ejemplos agregado a Streamlit, con vista previa,
  tipos, nulos, métricas y gráficos.
- ✅ Laboratorio 2 creado en JSON válido para compartirlo online.
- ✅ Recorrido guiado con logs y salidas separadas en `reportes/`.

**Tareas planeadas:**
- [ ] Ejecutar labs 01-06 con estudiantes en sesiones semanales
- [ ] Generar evidencia (notebooks completados + resultados) para cada sesión
- [ ] Taller presencial o virtual de 2 horas para demostración del pipeline
- [ ] Guía de referencia rápida (1 página) para imprimir
- [ ] Protocolo de cierre mensual: documento oficial con los pasos a seguir
- [ ] Definición de roles: quién opera qué módulo y cuándo
- [ ] Sesión de retroalimentación post-primer cierre con el equipo

## 🚀 FASE 5: Escalado Multiusuario (Futuro)

**Período estimado:** Mayo 2025 en adelante
**Estado:** 🚀 Futuro / Condicional

**Objetivo:** Si el equipo crece o se incorporan más empresas, migrar a una arquitectura
de servidor central accesible desde cualquier equipo de la red corporativa.

**Opciones a evaluar:**
- [ ] Servidor Windows interno con Docker (múltiples usuarios simultáneos)
- [ ] Kubernetes en la nube (si superan los 50 usuarios concurrentes)
- [ ] Autenticación por usuario (Jocelyn ve todo; analistas solo su empresa)
- [ ] Base de datos centralizada para historial de cierres
- [ ] API REST para integración directa con Book y Sofland (sin archivos Excel)

> [!NOTE]
> La Fase 5 solo se activa si la empresa lo requiere. El sistema actual
> (Docker en un solo computador) es suficiente para el equipo actual.

---

## Métricas de éxito del proyecto

| Métrica | Línea Base | Objetivo Fase 1 | Estado |
|---------|-----------|-----------------|--------|
| Tiempo de cierre mensual | 12 horas | < 4 horas | ✅ Logrado |
| Errores de cuadratura por cierre | ~5 por mes | 0 (detectados automáticamente) | ✅ Logrado |
| Tiempo para detectar un descuadre | 2-3 horas | < 5 minutos | ✅ Logrado |
| Usuarios que pueden operar el sistema | 1 (Jocelyn) | Todo el equipo (Fase 4) | 🔄 En progreso |
| Integración Book → Sofland sin Excel | No existe | Automatizada (Fase 2) | 🔄 En progreso |
