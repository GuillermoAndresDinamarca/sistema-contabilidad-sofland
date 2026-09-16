# Planificación del proyecto

Esta carpeta contiene decisiones, fases, tareas y registros de avance. La regla es
simple: el código puede avanzar rápido, pero una fase solo se cierra cuando existe
evidencia reproducible y una persona responsable.

## Documentos

| Documento | Uso |
|---|---|
| `fases.md` | Hoja de ruta, estado de cada fase y criterios de avance. |
| `tareas.md` | Backlog priorizado con estados y próximos pasos. |
| `decisiones.md` | Decisiones técnicas o contables aprobadas. |
| `registro_avances.md` | Historial breve por fecha, commit y evidencia. |
| `scheduler_contable.py` | Automatización técnica del pipeline. |
| `notificador.py` | Notificaciones en modo simulación o SMTP configurado. |

## Estados permitidos

- **Pendiente:** no iniciado.
- **En progreso:** trabajo local abierto, todavía no es entregable final.
- **Bloqueada:** depende de acceso, datos o aprobación externa.
- **Completada:** validada y lista para publicar.

## Política de publicación

Antes de hacer `git add`:

1. Separar datos sintéticos de datos reales.
2. Excluir credenciales, reportes temporales, logs y cachés.
3. Ejecutar una prueba mínima del módulo afectado.
4. Actualizar `tareas.md` o `fases.md` si cambia el estado.
5. Registrar la evidencia en `registro_avances.md`.
6. Crear un commit pequeño con un propósito claro.

## Estructura recomendada para crecer

```text
planificacion/
  README.md
  fases.md
  tareas.md
  decisiones.md
  registro_avances.md

docs/
  manual_de_uso.md
  tutorial.md
  checklist_cierre_mensual.md
  plantillas/
    evidencia_sesion.md
    decision_contable.md

laboratorios/
  lab_01_*.ipynb
  lab_02_*.ipynb
  lab_03_*.ipynb

reportes/       # salidas locales, no versionar
logs/           # ejecuciones locales, no versionar
```

Los documentos de `docs/` explican el uso; los de `planificacion/` explican el
estado y las decisiones; los notebooks enseñan el procedimiento reproducible.
