import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import date

# Configuración de la página
st.set_page_config(page_title="CRM & Control de Proyectos", layout="wide")

# --- INYECCIÓN DE CSS PARA DISEÑO ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stMetricValue"] {font-size: 2.2rem !important; color: #0047AB; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE LOGIN ---
def check_password():
    def password_entered():
        if st.session_state["username"] in st.secrets["passwords"] and \
           st.session_state["password"] == st.secrets["passwords"][st.session_state["username"]]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        if os.path.exists("logo.jpg"): st.image("logo.jpg", width=250)
        st.title("🔒 Acceso al CRM")
        st.text_input("Usuario", key="username")
        st.text_input("Contraseña", type="password", key="password")
        st.button("Ingresar", on_click=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        if os.path.exists("logo.jpg"): st.image("logo.jpg", width=250)
        st.title("🔒 Acceso al CRM")
        st.text_input("Usuario", key="username")
        st.text_input("Contraseña", type="password", key="password")
        st.button("Ingresar", on_click=password_entered)
        st.error("😕 Usuario o contraseña incorrectos")
        return False
    return True

# --- EJECUCIÓN DEL CRM ---
if check_password():
    if os.path.exists("logo.jpg"): st.sidebar.image("logo.jpg", use_container_width=True)
    st.sidebar.success(f"Sesión iniciada")
    
    # 1. Base de datos ampliada y estructurada
    if 'crm_db' not in st.session_state:
        st.session_state.crm_db = pd.DataFrame(columns=[
            'ID_Proyecto', 'Cliente', 'Nombre_Proyecto', 'Sector', 'Presupuesto_$', 'Avance_%',
            'Responsable', 'Prioridad', 'Fecha_Inicio', 'Fecha_Cierre_Est', 
            'Estado_Detallado', 'Acciones_Realizadas', 'Proximas_Acciones', 'Observaciones'
        ])
        # Proyectos de muestra iniciales
        st.session_state.crm_db.loc[0] = ['PRJ-001', 'Integramed', 'Estrategia Digital', 'Consultoría', 1500, 25, 'Nico', 'Alta', str(date.today()), '', 'Planificación inicial', 'Revisión de requerimientos', 'Armar calendario', '']
        st.session_state.crm_db.loc[1] = ['PRJ-002', 'El Rey del Golpe', 'Campaña y Visuales', 'Construcción', 2800, 60, 'Mateo', 'Media', str(date.today()), '', 'En ejecución', 'Scripts redactados', 'Generar imágenes IA', '']
        st.session_state.crm_db.loc[2] = ['PRJ-003', 'ACRE', 'Desarrollo E-commerce', 'Corretaje', 4500, 10, 'Nico', 'Alta', str(date.today()), '', 'Fase de diseño', 'Brand manual listo', 'Cotizar importaciones', '']

    # --- MENÚ LATERAL ---
    st.sidebar.markdown("---")
    menu = st.sidebar.radio("Navegación:", [
        "📊 1. Dashboard (Vista Rápida)", 
        "➕ 2. Agregar Nuevo Proyecto", 
        "📂 3. Ficha Detallada (Editar)"
    ])

    # ==========================================
    # PANTALLA 1: DASHBOARD (Solo Lectura)
    # ==========================================
    if menu == "📊 1. Dashboard (Vista Rápida)":
        st.title("📊 Resumen General de Proyectos")
        st.info("💡 **Vista de Lectura:** Aquí ves los datos esenciales. Para agregar proyectos usa el menú 'Agregar', y para editar usa la 'Ficha Detallada'. ¡Ya nada se borrará por accidente!")
        
        # Filtramos solo las columnas esenciales para que la tabla sea limpia y fácil de leer
        columnas_basicas = ['ID_Proyecto', 'Cliente', 'Nombre_Proyecto', 'Sector', 'Responsable', 'Prioridad', 'Presupuesto_$', 'Avance_%']
        df_vista = st.session_state.crm_db[columnas_basicas]
        
        st.dataframe(df_vista, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        df = st.session_state.crm_db.copy()
        df['Avance_%'] = pd.to_numeric(df['Avance_%'], errors='coerce').fillna(0)
        df['Presupuesto_$'] = pd.to_numeric(df['Presupuesto_$'], errors='coerce').fillna(0)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Proyectos Activos", len(df))
        col2.metric("Presupuesto Total", f"${df['Presupuesto_$'].sum():,.2f}")
        if not df.empty:
            col3.metric("Promedio de Avance", f"{df['Avance_%'].mean():.1f}%")
            fig_bar = px.bar(df, x='Nombre_Proyecto', y='Avance_%', color='Sector', text='Avance_%', title="Avance por Proyecto", range_y=[0,100])
            st.plotly_chart(fig_bar, use_container_width=True)

    # ==========================================
    # PANTALLA 2: AGREGAR NUEVO PROYECTO
    # ==========================================
    elif menu == "➕ 2. Agregar Nuevo Proyecto":
        st.title("➕ Registrar Nuevo Proyecto")
        
        # Formulario cerrado: Asegura que presionar Enter no borre nada
        with st.form("form_nuevo_proyecto", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                nuevo_id = st.text_input("ID Proyecto (Ej. PRJ-004)")
                nuevo_cliente = st.text_input("Nombre del Cliente / Empresa")
            with col2:
                nuevo_nombre = st.text_input("Nombre del Proyecto")
                nuevo_sector = st.selectbox("Sector", ["Arquitectura", "Construcción", "Consultoría", "Corretaje"])
            with col3:
                nuevo_presupuesto = st.number_input("Presupuesto ($)", min_value=0.0, step=100.0)
                nuevo_responsable = st.selectbox("Responsable", ["Nico", "Mateo", "Sin Asignar"])
            
            boton_crear = st.form_submit_button("✅ Crear Proyecto")
            
            if boton_crear:
                if nuevo_id == "" or nuevo_nombre == "":
                    st.error("El ID y el Nombre del Proyecto son obligatorios.")
                else:
                    nueva_fila = {
                        'ID_Proyecto': nuevo_id, 'Cliente': nuevo_cliente, 'Nombre_Proyecto': nuevo_nombre, 
                        'Sector': nuevo_sector, 'Presupuesto_$': nuevo_presupuesto, 'Avance_%': 0,
                        'Responsable': nuevo_responsable, 'Prioridad': 'Media', 'Fecha_Inicio': str(date.today()), 
                        'Fecha_Cierre_Est': '', 'Estado_Detallado': '', 'Acciones_Realizadas': '', 
                        'Proximas_Acciones': '', 'Observaciones': ''
                    }
                    st.session_state.crm_db = pd.concat([st.session_state.crm_db, pd.DataFrame([nueva_fila])], ignore_index=True)
                    st.success(f"Proyecto {nuevo_id} creado con éxito. Ve a la Ficha Detallada para agregar las notas.")

    # ==========================================
    # PANTALLA 3: FICHA DETALLADA (Edición Completa)
    # ==========================================
    elif menu == "📂 3. Ficha Detallada (Editar)":
        st.title("📂 Control y Ficha Detallada")
        
        lista_ids = st.session_state.crm_db['ID_Proyecto'].tolist()
        
        if not lista_ids or all(id == '' for id in lista_ids):
            st.warning("Aún no hay proyectos. Agrega uno en el menú 'Agregar Nuevo Proyecto'.")
        else:
            proyecto_seleccionado = st.selectbox("Selecciona un proyecto para gestionar:", lista_ids)
            idx = st.session_state.crm_db[st.session_state.crm_db['ID_Proyecto'] == proyecto_seleccionado].index[0]
            
            # Formulario cerrado para la edición general
            with st.form("form_edicion"):
                st.markdown(f"### Detalles: {st.session_state.crm_db.at[idx, 'Nombre_Proyecto']}")
                
                c1, c2, c3, c4 = st.columns(4)
                with c1: act_avance = st.number_input("Avance (%)", 0, 100, int(st.session_state.crm_db.at[idx, 'Avance_%']))
                with c2: act_resp = st.selectbox("Responsable", ["Nico", "Mateo", "Sin Asignar"], index=["Nico", "Mateo", "Sin Asignar"].index(st.session_state.crm_db.at[idx, 'Responsable']) if st.session_state.crm_db.at[idx, 'Responsable'] in ["Nico", "Mateo", "Sin Asignar"] else 2)
                with c3: act_prio = st.selectbox("Prioridad", ["Alta", "Media", "Baja"], index=["Alta", "Media", "Baja"].index(st.session_state.crm_db.at[idx, 'Prioridad']) if st.session_state.crm_db.at[idx, 'Prioridad'] in ["Alta", "Media", "Baja"] else 1)
                with c4: act_cierre = st.text_input("Fecha Cierre Est.", value=st.session_state.crm_db.at[idx, 'Fecha_Cierre_Est'])
                
                st.markdown("#### Control de Ejecución")
                colA, colB = st.columns(2)
                with colA:
                    act_estado = st.text_area("Estado Actual (Descripción Detallada)", value=st.session_state.crm_db.at[idx, 'Estado_Detallado'], height=120)
                    act_acciones = st.text_area("Acciones Realizadas", value=st.session_state.crm_db.at[idx, 'Acciones_Realizadas'], height=120)
                with colB:
                    act_proximas = st.text_area("Próximas Acciones", value=st.session_state.crm_db.at[idx, 'Proximas_Acciones'], height=120)
                    act_obs = st.text_area("Observaciones Adicionales", value=st.session_state.crm_db.at[idx, 'Observaciones'], height=120)
                
                boton_guardar = st.form_submit_button("💾 Actualizar Proyecto")
                
                if boton_guardar:
                    st.session_state.crm_db.at[idx, 'Avance_%'] = act_avance
                    st.session_state.crm_db.at[idx, 'Responsable'] = act_resp
                    st.session_state.crm_db.at[idx, 'Prioridad'] = act_prio
                    st.session_state.crm_db.at[idx, 'Fecha_Cierre_Est'] = act_cierre
                    st.session_state.crm_db.at[idx, 'Estado_Detallado'] = act_estado
                    st.session_state.crm_db.at[idx, 'Acciones_Realizadas'] = act_acciones
                    st.session_state.crm_db.at[idx, 'Proximas_Acciones'] = act_proximas
                    st.session_state.crm_db.at[idx, 'Observaciones'] = act_obs
                    st.success("¡Datos guardados! Revisa el Pipeline General para ver los cambios.")
