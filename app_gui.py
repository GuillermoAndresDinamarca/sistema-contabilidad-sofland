"""
app_gui.py — Interfaz Gráfica del Sistema de Contabilidad
===========================================================
Interfaz moderna operable SOLO CON MOUSE.
Basada en Streamlit para UI web moderna con botones, tablas y gráficos.

Ejecutar con:
    streamlit run app_gui.py

Requiere (instalar una vez):
    pip install streamlit pandas openpyxl
"""

import os
import sys
import io
import datetime
import pandas as pd
import streamlit as st

# --- Ruta de scripts compartidos (reutiliza los agentes de la carpeta de clases) ---
CLASES_DIR = os.path.join(
    os.path.expanduser("~"),
    "Documents", "progra", "clases", "intro a la programación"
)
if CLASES_DIR not in sys.path:
    sys.path.insert(0, CLASES_DIR)

# Importar el asistente local
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from asistente import generar_respuesta

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Sistema Contable Sofland — Jocelyn",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# ESTILOS MODERNOS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Colores principales */
    :root {
        --azul-oscuro: #1E3A5F;
        --azul-medio: #2563EB;
        --verde: #059669;
        --rojo: #DC2626;
        --gris-claro: #F8FAFC;
        --borde: #E2E8F0;
    }

    /* Títulos */
    .titulo-principal {
        font-size: 2rem;
        font-weight: 800;
        color: var(--azul-oscuro);
        margin-bottom: 0;
    }
    .subtitulo {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }

    /* Tarjetas métricas */
    .tarjeta {
        background: linear-gradient(135deg, #1E3A5F 0%, #2563EB 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(37,99,235,0.2);
        margin-bottom: 1rem;
        text-align: center;
    }
    .tarjeta h2 { font-size: 1.8rem; margin: 0; }
    .tarjeta p  { font-size: 0.85rem; margin: 0; opacity: 0.85; }

    .tarjeta-verde {
        background: linear-gradient(135deg, #065F46 0%, #059669 100%);
    }
    .tarjeta-roja {
        background: linear-gradient(135deg, #7F1D1D 0%, #DC2626 100%);
    }
    .tarjeta-naranja {
        background: linear-gradient(135deg, #78350F 0%, #D97706 100%);
    }

    /* Barra lateral */
    [data-testid="stSidebar"] {
        background-color: #1E3A5F !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-size: 0.95rem;
    }

    /* Chat bubbles */
    .chat-user {
        background-color: #DBEAFE;
        border-radius: 12px 12px 2px 12px;
        padding: 0.6rem 1rem;
        margin: 0.4rem 0;
        max-width: 80%;
        margin-left: auto;
        color: #1E3A5F;
        font-size: 0.95rem;
    }
    .chat-bot {
        background-color: #F1F5F9;
        border-left: 3px solid #2563EB;
        border-radius: 2px 12px 12px 12px;
        padding: 0.6rem 1rem;
        margin: 0.4rem 0;
        max-width: 85%;
        color: #1E3A5F;
        font-size: 0.95rem;
    }
    .chat-label {
        font-size: 0.7rem;
        color: #94A3B8;
        margin-bottom: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR / NAVEGACIÓN
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Sistema Contable")
    st.markdown("**Área de Remuneraciones**")
    st.markdown("---")

    modulo = st.radio(
        "Selecciona un módulo:",
        options=[
            "🏠  Panel Principal",
            "🧹  Limpiar Comprobantes",
            "🔗  Consolidar Empresas",
            "📊  Tablas Dinámicas",
            "⚖️  Cuadratura Bancaria",
            "🤖  Asistente Virtual",
            "⚡  Orquestador Completo",
        ],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.caption(f"🕐 {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
    st.caption("v1.0 · Sofland / Jocelyn")


# ═══════════════════════════════════════════════
# 🏠  PANEL PRINCIPAL
# ═══════════════════════════════════════════════
if modulo == "🏠  Panel Principal":
    st.markdown('<div class="titulo-principal">📊 Sistema de Contabilidad Sofland</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo">Panel de control del Área de Remuneraciones — Diseñado para el cierre mensual eficiente</div>', unsafe_allow_html=True)

    # Métricas clave
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="tarjeta tarjeta-roja">
            <p>Tiempo actual (manual)</p>
            <h2>12 hrs</h2>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="tarjeta tarjeta-verde">
            <p>Objetivo con sistema</p>
            <h2>&lt; 4 hrs</h2>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="tarjeta">
            <p>Colaboradores en nómina</p>
            <h2>13.000</h2>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="tarjeta tarjeta-naranja">
            <p>Empresas a consolidar</p>
            <h2>5</h2>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Flujo de trabajo
    st.subheader("📋 Flujo de Cierre Mensual")
    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.markdown("""
        | Paso | Tarea | Antes | Con el Sistema |
        |------|-------|-------|---------------|
        | 1️⃣ | Limpiar encabezados de comprobantes Sofland | ~1 hora manual | ✅ 5 minutos |
        | 2️⃣ | Consolidar 5 empresas en un libro único | ~3 horas copy-paste | ✅ 2 minutos |
        | 3️⃣ | Generar tablas dinámicas (13.000 colaboradores) | ~4 horas manual | ✅ 30 segundos |
        | 4️⃣ | Cuadratura Debe/Haber + detección de errores | ~3 horas revisión | ✅ Automático |
        | 5️⃣ | Revisión humana de descuadres detectados | Mezclado con todo | ✅ 1-2 horas enfocadas |
        """)
    with col_b:
        st.info(
            "**Tip:** Usa el módulo ⚡ **Orquestador Completo** para ejecutar "
            "los pasos 1 a 4 en un solo clic y ver el reporte final listo para importar a Sofland."
        )

    st.markdown("---")
    st.subheader("⚠️ Alertas de Cuentas Críticas")
    st.warning(
        "**Cuentas que requieren validación especial** (según historial de errores):\n"
        "- Aguinaldo: verificar que esté en cuenta 4105 y **no** en 5100 (remuneraciones generales).\n"
        "- Finiquito: confirmar que la glosa indique 'Rol General' o 'Rol Privado' para defensa ante auditoría.\n"
        "- Vacaciones: validar que los gastos anticipados estén correctamente centralizados."
    )


# ═══════════════════════════════════════════════
# 🧹  LIMPIAR COMPROBANTES
# ═══════════════════════════════════════════════
elif modulo == "🧹  Limpiar Comprobantes":
    st.header("🧹 Módulo 1: Limpieza de Comprobantes Sofland")
    st.write(
        "Elimina automáticamente las filas de encabezado (logo, fecha, usuario) que Sofland "
        "agrega al exportar. El sistema detecta cuántas filas saltar y deja el archivo listo para importar."
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded = st.file_uploader(
            "📂 Arrastra tu comprobante Excel aquí o haz clic para buscarlo",
            type=["xlsx", "xls"],
            accept_multiple_files=True
        )
    with col2:
        st.info(
            "**¿Qué hace este módulo?**\n\n"
            "1. Lee las primeras 10 filas\n"
            "2. Detecta la fila real de encabezados (Cuenta, Debe, Haber...)\n"
            "3. Descarta las filas anteriores (basura)\n"
            "4. Limpia columnas sin nombre y filas vacías\n"
            "5. Entrega el Excel limpio para descarga"
        )

    if uploaded:
        resultados = []
        for f in uploaded:
            try:
                preview = pd.read_excel(f, header=None, nrows=10)
                # Detectar fila header
                palabras = ["Cuenta", "Debe", "Haber", "Fecha", "Glosa", "Monto", "Empresa"]
                skiprows = 0
                for i, row in preview.iterrows():
                    vals = [str(v).strip() for v in row.values]
                    if any(k in vals for k in palabras):
                        skiprows = i
                        break

                f.seek(0)
                df_clean = pd.read_excel(f, skiprows=skiprows)
                df_clean = df_clean.loc[:, ~df_clean.columns.astype(str).str.contains("^Unnamed")]
                df_clean = df_clean.dropna(how="all")
                for col in df_clean.select_dtypes(include="object").columns:
                    df_clean[col] = df_clean[col].str.strip()

                resultados.append((f.name, df_clean, skiprows))
            except Exception as e:
                st.error(f"Error procesando {f.name}: {e}")

        for nombre, df, filas_saltadas in resultados:
            with st.expander(f"✅ {nombre} — {len(df)} filas válidas (se saltaron {filas_saltadas} de encabezado)"):
                st.dataframe(df.head(10), use_container_width=True)

                buf = io.BytesIO()
                with pd.ExcelWriter(buf, engine="openpyxl") as w:
                    df.to_excel(w, index=False)
                buf.seek(0)

                st.download_button(
                    label=f"📥 Descargar {nombre.replace('.xlsx', '_limpio.xlsx')}",
                    data=buf,
                    file_name=nombre.replace(".xlsx", "_limpio.xlsx"),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )


# ═══════════════════════════════════════════════
# 🔗  CONSOLIDAR EMPRESAS
# ═══════════════════════════════════════════════
elif modulo == "🔗  Consolidar Empresas":
    st.header("🔗 Módulo 2: Consolidación de Libros Multiempresa")
    st.write(
        "Sube todos los archivos de las empresas (A, B, C, D, E) a la vez. "
        "El sistema los une en un único libro consolidado y agrega una columna de origen."
    )

    uploaded = st.file_uploader(
        "📂 Selecciona los archivos de las empresas (puedes subir varios a la vez)",
        type=["xlsx", "xls"],
        accept_multiple_files=True
    )

    if uploaded:
        st.info(f"Se cargaron **{len(uploaded)} archivo(s)**. Haz clic en el botón para consolidar.")

        if st.button("🔗 Consolidar Ahora", type="primary"):
            dfs = []
            errores = []
            for f in uploaded:
                try:
                    preview = pd.read_excel(f, header=None, nrows=10)
                    palabras = ["Cuenta", "Debe", "Haber", "Fecha", "Glosa", "Monto"]
                    skiprows = 0
                    for i, row in preview.iterrows():
                        vals = [str(v).strip() for v in row.values]
                        if any(k in vals for k in palabras):
                            skiprows = i
                            break
                    f.seek(0)
                    df = pd.read_excel(f, skiprows=skiprows)
                    df = df.loc[:, ~df.columns.astype(str).str.contains("^Unnamed")]
                    df = df.dropna(how="all")
                    df["_empresa_origen"] = os.path.splitext(f.name)[0]
                    dfs.append(df)
                except Exception as e:
                    errores.append(f"{f.name}: {e}")

            if errores:
                for err in errores:
                    st.error(err)

            if dfs:
                consolidado = pd.concat(dfs, ignore_index=True)
                st.success(f"✅ Consolidación exitosa: **{len(consolidado):,} registros** de **{len(dfs)} empresa(s)**")

                st.subheader("Vista previa del libro consolidado")
                st.dataframe(consolidado.head(20), use_container_width=True)

                # Pivot rápido de resumen
                if "Debe" in consolidado.columns and "Haber" in consolidado.columns:
                    st.subheader("Resumen por Empresa de Origen")
                    resumen = consolidado.groupby("_empresa_origen").agg(
                        Registros=("_empresa_origen", "count"),
                        Total_Debe=("Debe", "sum"),
                        Total_Haber=("Haber", "sum")
                    )
                    resumen["Diferencia"] = resumen["Total_Debe"] - resumen["Total_Haber"]
                    resumen["Estado"] = resumen["Diferencia"].apply(
                        lambda x: "✅ Cuadrado" if abs(x) < 1 else "⚠️ Descuadre"
                    )
                    st.dataframe(resumen, use_container_width=True)

                buf = io.BytesIO()
                with pd.ExcelWriter(buf, engine="openpyxl") as w:
                    consolidado.to_excel(w, index=False)
                buf.seek(0)

                st.download_button(
                    label="📥 Descargar Libro Consolidado",
                    data=buf,
                    file_name="libro_consolidado.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary"
                )


# ═══════════════════════════════════════════════
# 📊  TABLAS DINÁMICAS
# ═══════════════════════════════════════════════
elif modulo == "📊  Tablas Dinámicas":
    st.header("📊 Módulo 3: Tablas Dinámicas / Pivot de Remuneraciones")
    st.write(
        "Genera análisis de cuentas automáticamente. Equivalente a las Tablas Dinámicas de Excel "
        "pero sin construcción manual. Ideal para el análisis de 13.000 colaboradores."
    )

    uploaded = st.file_uploader("📂 Sube el libro consolidado o cualquier Excel de remuneraciones", type=["xlsx"])

    if uploaded:
        df = pd.read_excel(uploaded)
        st.success(f"Archivo cargado: {len(df):,} filas | {len(df.columns)} columnas")

        col_index = st.multiselect(
            "Selecciona las columnas de filas (índice del pivot):",
            options=list(df.columns),
            default=[c for c in ["Cuenta", "Empresa", "Centro_Costo"] if c in df.columns] or [df.columns[0]]
        )
        col_values = st.multiselect(
            "Selecciona las columnas de valores a sumar:",
            options=[c for c in df.columns if df[c].dtype in ["float64", "int64"]],
            default=[c for c in ["Debe", "Haber", "Monto"] if c in df.columns]
        )

        if col_index and col_values and st.button("📊 Generar Pivot", type="primary"):
            pivot = pd.pivot_table(
                df,
                values=col_values,
                index=col_index,
                aggfunc="sum",
                fill_value=0,
                margins=True,
                margins_name="TOTAL"
            )
            if "Debe" in pivot.columns and "Haber" in pivot.columns:
                pivot["Saldo"] = pivot["Debe"] - pivot["Haber"]
                pivot["Estado"] = pivot["Saldo"].apply(
                    lambda x: "✅ OK" if abs(x) < 1 else ("⚠️ Descuadre" if abs(x) < 100000 else "🚨 Revisar")
                )

            st.dataframe(pivot, use_container_width=True)

            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine="openpyxl") as w:
                pivot.to_excel(w)
            buf.seek(0)
            st.download_button(
                "📥 Descargar Pivot",
                data=buf,
                file_name="pivot_remuneraciones.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


# ═══════════════════════════════════════════════
# ⚖️  CUADRATURA BANCARIA
# ═══════════════════════════════════════════════
elif modulo == "⚖️  Cuadratura Bancaria":
    st.header("⚖️ Módulo 4: Cuadratura Libro vs Cartola Bancaria")
    st.write("Sube el libro contable y la cartola del banco para detectar descuadres automáticamente.")

    col1, col2 = st.columns(2)
    with col1:
        f_libro = st.file_uploader("📗 Libro Contable / Consolidado", type=["xlsx"], key="libro")
    with col2:
        f_cartola = st.file_uploader("🏦 Cartola Bancaria", type=["xlsx"], key="cartola")

    if f_libro and f_cartola and st.button("🔍 Ejecutar Cuadratura", type="primary"):
        df_l = pd.read_excel(f_libro)
        df_b = pd.read_excel(f_cartola)

        col_l = "Debe" if "Debe" in df_l.columns else ("Monto" if "Monto" in df_l.columns else df_l.select_dtypes("number").columns[0])
        col_b = "Monto_Banco" if "Monto_Banco" in df_b.columns else ("Monto" if "Monto" in df_b.columns else df_b.select_dtypes("number").columns[0])

        total_l = df_l[col_l].sum()
        total_b = df_b[col_b].sum()
        dif = total_l - total_b

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Libro Contable", f"${total_l:,.0f}")
        c2.metric("Total Cartola Banco", f"${total_b:,.0f}")
        c3.metric("Diferencia", f"${dif:,.0f}", delta_color="inverse")

        if abs(dif) < 1:
            st.balloons()
            st.success("🎉 ¡CUADRATURA PERFECTA! Los saldos coinciden al 100%.")
        elif abs(dif) < 100_000:
            st.warning(f"⚠️ Diferencia menor detectada de ${dif:,.0f}. Revisar transacciones de los últimos días del período.")
        else:
            st.error(f"🚨 Descuadre significativo de ${dif:,.0f}. Revisar antes de importar a Sofland.")


# ═══════════════════════════════════════════════
# 🤖  ASISTENTE VIRTUAL
# ═══════════════════════════════════════════════
elif modulo == "🤖  Asistente Virtual":
    st.header("🤖 Asistente Virtual del Área Contable")
    st.write(
        "Escribe tu consulta en lenguaje natural. El asistente te guiará al módulo correcto "
        "y explicará cómo resolver tu problema del cierre mensual."
    )

    # Inicializar historial
    if "chat_historial" not in st.session_state:
        st.session_state.chat_historial = [
            {
                "rol": "bot",
                "msg": (
                    "¡Hola! Soy tu asistente del cierre mensual. Puedo ayudarte con:\n"
                    "• Limpiar comprobantes de Sofland\n"
                    "• Consolidar las 5 empresas\n"
                    "• Resolver descuadres de remuneraciones\n"
                    "• Validar glosas de aguinaldo, finiquito o vacaciones\n\n"
                    "¿En qué etapa del proceso estás?"
                )
            }
        ]

    # Mostrar historial
    for item in st.session_state.chat_historial:
        if item["rol"] == "usuario":
            st.markdown(f"""
            <div class="chat-label" style="text-align:right">Tú</div>
            <div class="chat-user">{item['msg']}</div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-label">🤖 Asistente</div>
            <div class="chat-bot">{item['msg']}</div>
            """, unsafe_allow_html=True)

    # Input del usuario
    with st.form("chat_form", clear_on_submit=True):
        col_inp, col_btn = st.columns([5, 1])
        with col_inp:
            user_input = st.text_input(
                "Tu consulta:",
                placeholder="Ej: ¿Cómo limpio los comprobantes de Sofland?",
                label_visibility="collapsed"
            )
        with col_btn:
            enviado = st.form_submit_button("Enviar", type="primary")

    if enviado and user_input.strip():
        st.session_state.chat_historial.append({"rol": "usuario", "msg": user_input})
        respuesta = generar_respuesta(user_input)
        st.session_state.chat_historial.append({"rol": "bot", "msg": respuesta})
        st.rerun()

    if st.button("🗑️ Limpiar conversación"):
        st.session_state.chat_historial = []
        st.rerun()


# ═══════════════════════════════════════════════
# ⚡  ORQUESTADOR COMPLETO
# ═══════════════════════════════════════════════
elif modulo == "⚡  Orquestador Completo":
    st.header("⚡ Orquestador: Pipeline Completo de Cierre")
    st.write(
        "Sube una carpeta con los archivos de las empresas y ejecuta **todo el pipeline en secuencia**: "
        "limpieza → consolidación → pivot → cuadratura. En un solo clic."
    )

    uploaded = st.file_uploader(
        "📂 Sube todos los archivos de las empresas para procesar",
        type=["xlsx", "xls"],
        accept_multiple_files=True
    )

    if uploaded and st.button("🚀 Ejecutar Pipeline Completo", type="primary"):
        progress = st.progress(0)
        status = st.empty()

        # Paso 1: Limpieza
        status.info("🧹 Paso 1/4: Limpiando encabezados...")
        dfs_limpios = []
        for f in uploaded:
            preview = pd.read_excel(f, header=None, nrows=10)
            palabras = ["Cuenta", "Debe", "Haber", "Fecha", "Glosa", "Monto"]
            skiprows = 0
            for i, row in preview.iterrows():
                vals = [str(v).strip() for v in row.values]
                if any(k in vals for k in palabras):
                    skiprows = i
                    break
            f.seek(0)
            df = pd.read_excel(f, skiprows=skiprows)
            df = df.loc[:, ~df.columns.astype(str).str.contains("^Unnamed")]
            df = df.dropna(how="all")
            df["_empresa_origen"] = os.path.splitext(f.name)[0]
            dfs_limpios.append(df)
        progress.progress(25)

        # Paso 2: Consolidación
        status.info("🔗 Paso 2/4: Consolidando empresas...")
        consolidado = pd.concat(dfs_limpios, ignore_index=True)
        progress.progress(50)

        # Paso 3: Pivot
        status.info("📊 Paso 3/4: Generando tablas dinámicas...")
        pivot = None
        cols_num = [c for c in consolidado.columns if consolidado[c].dtype in ["float64", "int64"]]
        cols_idx = [c for c in ["_empresa_origen", "Cuenta"] if c in consolidado.columns]
        if cols_idx and cols_num:
            pivot = pd.pivot_table(
                consolidado,
                values=cols_num[:2],
                index=cols_idx,
                aggfunc="sum",
                fill_value=0,
                margins=True,
                margins_name="TOTAL"
            )
        progress.progress(75)

        # Paso 4: Cuadratura
        status.info("⚖️ Paso 4/4: Ejecutando cuadratura...")
        if "Debe" in consolidado.columns and "Haber" in consolidado.columns:
            consolidado["_cuadratura"] = consolidado["Debe"] - consolidado["Haber"]
            descuadres = consolidado[abs(consolidado["_cuadratura"]) > 1]
        else:
            descuadres = pd.DataFrame()
        progress.progress(100)

        # Resultados
        status.empty()
        st.success(f"✅ Pipeline completado. {len(consolidado):,} registros procesados.")

        tabs = st.tabs(["📋 Consolidado", "📊 Pivot", "🚨 Descuadres"])
        with tabs[0]:
            st.dataframe(consolidado.head(50), use_container_width=True)
        with tabs[1]:
            if pivot is not None:
                st.dataframe(pivot, use_container_width=True)
            else:
                st.info("No se encontraron columnas numéricas para el pivot.")
        with tabs[2]:
            if descuadres.empty:
                st.success("🎉 Sin descuadres. El cierre puede proceder.")
            else:
                st.warning(f"Se encontraron {len(descuadres)} registros con descuadre.")
                st.dataframe(descuadres, use_container_width=True)

        # Descargar reporte final
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            consolidado.to_excel(w, sheet_name="Consolidado", index=False)
            if pivot is not None:
                pivot.to_excel(w, sheet_name="Pivot")
            if not descuadres.empty:
                descuadres.to_excel(w, sheet_name="Descuadres", index=False)
        buf.seek(0)

        st.download_button(
            label="📥 Descargar Reporte Completo de Cierre",
            data=buf,
            file_name=f"cierre_{datetime.datetime.now().strftime('%Y%m')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )
