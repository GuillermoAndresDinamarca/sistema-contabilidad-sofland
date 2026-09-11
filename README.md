# Sistema de Contabilidad Sofland — Área de Remuneraciones

Plataforma de automatización contable empaquetada con Docker, diseñada específicamente para resolver los cuellos de botella en la centralización y cuadratura de remuneraciones (basado en los requerimientos de Jocelyn).

## Estructura del Proyecto

```
sistema contabilidad para sofland/
├── app/                      ← Código fuente de la app (Streamlit, Python)
├── docs/                     ← Documentación para el usuario final
│   ├── manual_de_uso.md
│   ├── tutorial.md
│   └── glosario.md
├── planificacion/            ← Hojas de ruta y tareas pendientes
│   ├── fases.md
│   ├── tareas.md
│   └── decisiones.md
├── ejemplos/                 ← Scripts y Excels sintéticos para practicar
│   └── analizar_casos_contables.py ← Controles, cuadratura y resúmenes reproducibles
├── docker-compose.yml        ← Orquestación de contenedores
├── Dockerfile                ← Definición de la imagen base
├── INSTALAR.bat              ← 🚀 SCRIPT PARA INICIAR EL SISTEMA EN WINDOWS (DOBLE CLIC)
├── DETENER.bat               ← Script para apagar el sistema en Windows
├── instalar_y_ejecutar.sh    ← Script para iniciar en Mac/Linux
└── detener.sh                ← Script para apagar en Mac/Linux
```

## 🚀 Cómo Empezar (Sin saber programar)

### ¿Qué se debe entregar a otra persona?

No es necesario enviar una imagen Docker ni instalar Python manualmente. La
forma recomendada es compartir el enlace del repositorio Git y que la persona
clone el proyecto. El repositorio ya contiene `Dockerfile`, `docker-compose.yml`,
la aplicación, ejemplos y scripts de instalación.

Requisitos del equipo destinatario:

- Docker Desktop instalado y ejecutándose.
- Git instalado, o alternativamente un ZIP descargado del repositorio.
- Puerto local `8501` disponible.

### Instalación desde un repositorio clonado

```powershell
git clone <URL_DEL_REPOSITORIO>
Set-Location sistema-contabilidad-sofland
.\INSTALAR.bat
```

En Windows también se puede abrir `INSTALAR.bat` con doble clic. La primera
ejecución construye la imagen y puede tardar algunos minutos; las siguientes
solo levantan el sistema. Para detenerlo, ejecutar `DETENER.bat`.

Si se entrega un ZIP, hay que descomprimirlo completo: no basta enviar solo
`Dockerfile`, porque Docker necesita también `app/`, `ejemplos/`, `docker-compose.yml`
y los scripts de inicio.

### En Windows
1. Descarga e instala [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Haz doble clic en el archivo **`INSTALAR.bat`**.
3. El sistema se abrirá automáticamente en tu navegador web.
4. Consulta [el manual de uso](docs/manual_de_uso.md) y [la guía de ejemplos](ejemplos/README.md) para hacer la primera prueba.

### En Mac / Linux
1. Asegúrate de tener Docker instalado.
2. Otorga permisos de ejecución al script: `chmod +x instalar_y_ejecutar.sh`
3. Ejecuta el script: `./instalar_y_ejecutar.sh`

## Características Clave

- **Limpieza Automática:** Elimina las 4 filas de encabezado basura de Sofland.
- **Consolidación Masiva:** Une N empresas en un solo Excel con 1 clic.
- **Pivot Automático:** Genera análisis de cuentas para >13.000 colaboradores.
- **Detección de Descuadres:** Cuadratura automática Debe/Haber y Libro vs Cartola.
- **Orquestador Central:** Ejecuta todos los pasos anteriores secuencialmente.

## Dónde quedan los archivos

- `ejemplos/`: archivos sintéticos de entrada y scripts de práctica.
- `reportes/`: reportes Excel generados por los analizadores y el pipeline.
- `datos_salida/`: archivos de salida de la aplicación Docker.
- `logs/`: registros del scheduler automático.

No subir datos reales de remuneraciones al repositorio. Para producción se debe
usar una carpeta de entrada controlada y revisar los permisos de los reportes.

## Ruta de aprendizaje y recursos

- [Ruta de aprendizaje Python para contabilidad](docs/ruta_aprendizaje_python_contabilidad.md)
- [Recursos externos Python, Excel y contabilidad](docs/recursos_python_contabilidad.md)
- [Tutorial completo del cierre sintético](docs/tutorial.md)
- [Laboratorio 2: consolidación y visualización](laboratorios/lab_02_consolidacion_sofland.ipynb)
- [Laboratorio 3: conciliación de movimientos](laboratorios/lab_03_conciliacion_movimientos.ipynb)
- [Guía de ejemplos prácticos](ejemplos/README.md)

El análisis local usa datos sintéticos y deja la decisión contable en manos de la persona responsable.

## Módulos de Análisis y Validación

La carpeta `ejemplos/` contiene scripts reutilizables para analizar y validar datos contables:

### 📊 `generar_ejemplos.py`
Genera 5 casos de prueba sintéticos (Empresas A-E) + cartola bancaria.
- **Empresa E:** Incluye descuadre intencional de $1,500,000 para practicar detección.
- Uso: `python generar_ejemplos.py`

### 🔍 `analizar_casos_contables.py`
Analiza archivos Excel y detecta cuadrados de Debe/Haber.
- Genera reporte Excel con 4 hojas: Control, Consolidado, Cuentas, Centros.
- Uso: `python analizar_casos_contables.py`

### ⚠️ `validar_datos_contables.py`
Detección avanzada de anomalías: duplicados, valores faltantes, caracteres especiales.
- Genera reporte con recomendaciones de corrección.
- Sanitiza glosas problemáticas (ñ→n, á→a).
- Uso: `python validar_datos_contables.py <archivo.xlsx>`

### 🔗 `generar_casos_especiales.py`
Crea casos para practicar: duplicados, tolerancias, movimientos faltantes.
- Uso: `python generar_casos_especiales.py`

### 🎯 `pipeline_contable_completo.py`
Orquesta el flujo: validación → análisis → reporte integrado.
- Genera Excel con resumen de estado de todos los archivos.
- Uso: `python pipeline_contable_completo.py <directorio>`

### ⏰ `planificacion/scheduler_contable.py`
Ejecuta el pipeline inmediatamente o lo programa diariamente.
- Prueba segura: `python planificacion/scheduler_contable.py --run --entrada ejemplos --salida reportes`
- Genera instalador de Windows: `python planificacion/scheduler_contable.py --install`
- Servicio continuo: `python planificacion/scheduler_contable.py --watch --time 06:00`

### ✉️ `planificacion/notificador.py`
Prepara alertas por correo para archivos con estado `ERROR` o `REVISAR`.
- El scheduler usa simulación por defecto.
- Para SMTP se requiere `--enviar` y las variables `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` y `ALERTA_EMAIL`.

### 🧪 `ejemplos/ejecutar_ejemplos.py`
Ejecuta el recorrido completo por etapas y registra cada paso en `logs/`.
- Uso: `py -3 ejemplos/ejecutar_ejemplos.py`
- Las salidas Excel se agrupan en `reportes/`.

### 🎓 `ejemplos/primeros_codigos.py`
Script breve para la primera capacitación: leer, limpiar, calcular, comparar y graficar.
- Uso: `py -3 ejemplos/primeros_codigos.py`
