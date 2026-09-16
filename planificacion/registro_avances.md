# Registro de avances

Este registro conserva solo hitos verificables. Cada entrada debe indicar fecha,
resultado, evidencia y siguiente acción.

## 2026-09-16

### Publicado y verificado

- Repositorio remoto configurado en GitHub.
- Navegador de ejemplos agregado a Streamlit.
- Ejecutor guiado de ejemplos con logs en `ejemplos/ejecutar_ejemplos.py`.
- Reportes separados en `reportes/` y salidas temporales excluidas por `.gitignore`.
- Laboratorios 2 y 3 validados como JSON con `metadata.language`.
- Scheduler probado con ejecución inmediata.
- Notificador probado en modo simulación.

### Evidencia

- `py -3 -m py_compile` sin errores en los módulos modificados.
- `py -3 ejemplos/ejecutar_ejemplos.py` finaliza con código 0.
- `py -3 ejemplos/primeros_codigos.py` detecta la diferencia sintética de EmpresaE.
- Rama `main` publicada y sincronizada con `origin/main`.

### Pendiente o bloqueado

- Primera sesión de capacitación con el equipo.
- Prueba de instalación Docker desde un clon limpio.
- Aprobación de cuentas, glosas y centros de costo por la persona responsable.
- Configuración SMTP institucional.
- Definición del formato Book para avanzar en Fase 2.

## Formato para próximas entradas

```markdown
## AAAA-MM-DD

### Terminado

- [Descripción breve]

### Evidencia

- [Comando, archivo, captura o revisión humana]

### Pendiente o bloqueado

- [Siguiente acción y responsable]
```
