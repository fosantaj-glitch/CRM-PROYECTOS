import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuración de la página
st.set_page_config(page_title="CRM & Control de Proyectos", layout="wide")

# --- INYECCIÓN DE CSS PARA DISEÑO ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        color: #0047AB; 
        font-weight: bold;
    }
    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
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
    
    # Base de datos ampliada
    if 'crm_db' not in st.session_state:
        st.session_state.crm_db = pd.DataFrame(columns=[
            'ID_Proyecto', 'Cliente', 'Nombre_Proyecto', 'Sector', 'Presupuesto_$', 'Avance_%',
            'Responsable', 'Estado_Detallado', 'Acciones_Realizadas', 'Proximas_Acciones', 'Observaciones'
        ])
        st.session_state.crm_db.loc[0] = ['PRJ-001', 'Ejemplo', 'Proyecto Alfa', 'Arquitectura', 0, 0, 'Nico', '', '', '', '']

    # --- MENÚ LATERAL ---
    st.sidebar.markdown("---")
    menu = st.sidebar.radio("Navegación:", ["📊 Pipeline General", "📂 Ficha Detallada"])

    # ==========================================
    # PANTALLA 1: PIPELINE GENERAL
    # ==========================================
    if menu == "📊 Pipeline General":
        col_logo, col_title = st.columns([1, 4])
        with col_logo:
            if os.path.exists("logo.jpg"): st.image("logo.jpg", width=150)
        with col_title:
            st.title("📊 Pipeline y Resumen")
        
        st.info("💡 **Instrucciones:** Edita aquí los datos básicos. Para confirmar un dato, presiona **Enter** o haz clic fuera de la celda. Para redactar detalles largos, ve a la 'Ficha Detallada' en el menú izquierdo.")
        
        # Configuramos la tabla para ocultar las columnas de texto largo
        columnas_ocultas = ['Responsable', 'Estado_Detallado', 'Acciones_Realizadas', 'Proximas_Acciones', 'Observaciones']
        configuracion_columnas = {col: None for col in columnas_ocultas}
        
        st.session_state.crm_db = st.data_editor(
            st.session_state.crm_db, 
            column_config=configuracion_columnas,
            num_rows="dynamic", 
            use_container_width=True,
            key="editor_proyectos"
        )

        st.markdown("---")
        df = st.session_state.crm_db.copy()
        df['Avance_%'] = pd.to_numeric(df['Avance_%'], errors='coerce').fillna(0)
        df['Presupuesto_$'] = pd.to_numeric(df['Presupuesto_$'], errors='coerce').fillna(0)
        df_validos = df[df['Nombre_Proyecto'] != '']
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Proyectos Registrados", len(df_validos))
        col2.metric("Presupuesto Total", f"${df_validos['Presupuesto_$'].sum():,.2f}")
        if not df_validos.empty:
            col3.metric("Promedio de Avance", f"{df_validos['Avance_%'].mean():.1f}%")
            fig_bar = px.bar(df_validos, x='Nombre_Proyecto', y='Avance_%', color='Sector', 
                             text='Avance_%', title="Avance por Proyecto", range_y=[0,100])
            st.plotly_chart(fig_bar, use_container_width=True)

    # ==========================================
    # PANTALLA 2: FICHA DETALLADA (MODO FORMULARIO)
    # ==========================================
    elif menu == "📂 Ficha Detallada":
        st.title("📂 Ficha Detallada del Proyecto")
        
        lista_ids = st.session_state.crm_db['ID_Proyecto'].tolist()
        
        if no lista_ids or all(id == '' for id in lista_ids):
            st.warning("Aún no hay proyectos. Agrega uno en el Pipeline General primero.")
        else:
            # Selector de proyecto
            proyecto_seleccionado = st.selectbox("Selecciona un proyecto para ver/editar detalles:", lista_ids)
            idx = st.session_state.crm_db[st.session_state.crm_db['ID_Proyecto'] == proyecto_seleccionado].index[0]
            
            nombre_actual = st.session_state.crm_db.at[idx, 'Nombre_Proyecto']
            st.markdown(f"### Editando: {nombre_actual if nombre_actual else 'Proyecto sin nombre'}")
            
            # Formulario robusto (no se borra al presionar Enter)
            with st.form("form_detalles"):
                col1, col2 = st.columns(2)
                
                with col1:
                    resp_actual = st.session_state.crm_db.at[idx, 'Responsable']
                    opciones_resp = ["Nico", "Mateo", "Sin Asignar"]
                    idx_resp = opciones_resp.index(resp_actual) if resp_actual in opciones_resp else 2
                    
                    nuevo_resp = st.selectbox("Responsable del Proyecto", opciones_resp, index=idx_resp)
                    nuevo_estado = st.text_area("Estado Actual (Descripción Detallada)", value=st.session_state.crm_db.at[idx, 'Estado_Detallado'], height=150)
                
                with col2:
                    nuevas_acciones = st.text_area("Acciones Realizadas", value=st.session_state.crm_db.at[idx, 'Acciones_Realizadas'], height=150)
                    nuevas_proximas = st.text_area("Próximas Acciones", value=st.session_state.crm_db.at[idx, 'Proximas_Acciones'], height=150)
                
                nuevas_obs = st.text_area("Observaciones Adicionales", value=st.session_state.crm_db.at[idx, 'Observaciones'])
                
                boton_guardar = st.form_submit_button("💾 Guardar Detalles")
                
                if boton_guardar:
                    st.session_state.crm_db.at[idx, 'Responsable'] = nuevo_resp
                    st.session_state.crm_db.at[idx, 'Estado_Detallado'] = nuevo_estado
                    st.session_state.crm_db.at[idx, 'Acciones_Realizadas'] = nuevas_acciones
                    st.session_state.crm_db.at[idx, 'Proximas_Acciones'] = nuevas_proximas
                    st.session_state.crm_db.at[idx, 'Observaciones'] = nuevas_obs
                    st.success("¡Detalles guardados correctamente!")
