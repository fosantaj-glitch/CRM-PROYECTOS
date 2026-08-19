import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuración de la página
st.set_page_config(page_title="CRM & Control de Proyectos", layout="wide")

# --- INYECCIÓN DE CSS PARA DISEÑO ---
st.markdown("""
    <style>
    /* Ocultar elementos predeterminados de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Estilo para las métricas */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        color: #0047AB; 
        font-weight: bold;
    }
    
    /* Estilo para la tabla */
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
        # LOGO: Pantalla de Login
        if os.path.exists("logo.jpg"):
            st.image("logo.jpg", width=250)
            
        st.title("🔒 Acceso al CRM")
        st.text_input("Usuario", key="username")
        st.text_input("Contraseña", type="password", key="password")
        st.button("Ingresar", on_click=password_entered)
        return False
        
    elif not st.session_state["password_correct"]:
        # LOGO: Pantalla de Login (Si la clave es incorrecta)
        if os.path.exists("logo.jpg"):
            st.image("logo.jpg", width=250)
            
        st.title("🔒 Acceso al CRM")
        st.text_input("Usuario", key="username")
        st.text_input("Contraseña", type="password", key="password")
        st.button("Ingresar", on_click=password_entered)
        st.error("😕 Usuario o contraseña incorrectos")
        return False
        
    return True

# --- EJECUCIÓN DEL CRM ---
if check_password():
    # LOGO: Barra lateral, arriba de "Sesión iniciada"
    if os.path.exists("logo.jpg"):
        st.sidebar.image("logo.jpg", use_container_width=True)
        
    st.sidebar.success(f"Sesión iniciada")
    
    if 'pipeline_data' not in st.session_state:
        st.session_state.pipeline_data = pd.DataFrame(
            columns=['ID_Proyecto', 'Cliente', 'Nombre_Proyecto', 'Sector', 'Presupuesto_$', 'Estado', 'Avance_%']
        )
        st.session_state.pipeline_data.loc[0] = ['PRJ-001', '', '', 'Arquitectura', 0, 'Prospecto', 0]

    # LOGO: Panel principal superior (Dashboard)
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        if os.path.exists("logo.jpg"):
            st.image("logo.jpg", width=150)
    with col_title:
        st.title("📊 Dashboard General y Base de Datos")
    
    st.markdown("### 1. Panel de Edición de Proyectos")
    st.info("💡 **Instrucciones:** Haz doble clic en cualquier celda para escribir. Para agregar un nuevo proyecto, haz clic en el botón '+' o en la fila vacía al final. Para borrar un proyecto, selecciona la casilla de la izquierda y presiona la tecla Delete/Suprimir o el ícono de la papelera.")
    
    st.session_state.pipeline_data = st.data_editor(
        st.session_state.pipeline_data, 
        num_rows="dynamic", 
        use_container_width=True,
        key="editor_proyectos"
    )

    st.markdown("---")
    st.markdown("### 2. Gráficos y Resumen Automático")
    
    df = st.session_state.pipeline_data.copy()
    df['Avance_%'] = pd.to_numeric(df['Avance_%'], errors='coerce').fillna(0)
    df['Presupuesto_$'] = pd.to_numeric(df['Presupuesto_$'], errors='coerce').fillna(0)

    df_validos = df[df['Nombre_Proyecto'] != '']
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Proyectos Registrados", len(df_validos))
    col2.metric("Presupuesto Total", f"${df_validos['Presupuesto_$'].sum():,.2f}")
    
    if not df_validos.empty:
        col3.metric("Promedio de Avance", f"{df_validos['Avance_%'].mean():.1f}%")
        
        fig_bar = px.bar(df_validos, x='Nombre_Proyecto', y='Avance_%', color='Sector', 
                         text='Avance_%', title="Porcentaje de Completitud por Proyecto", range_y=[0,100])
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        col3.metric("Promedio de Avance", "0%")
        st.warning("Ingresa el nombre de tus proyectos en la tabla de arriba para generar los gráficos.")
