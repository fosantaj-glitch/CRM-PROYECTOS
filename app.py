import streamlit as st
import pandas as pd
from datetime import date
import requests
import json
import time

# Configuración de la página
st.set_page_config(page_title="CRM Proyectos", layout="wide")

# ==========================================
# 🎨 CSS AVANZADO: DISEÑO ELEGANTE Y PROFESIONAL
# ==========================================
st.markdown("""
    <style>
    /* Ocultar elementos por defecto de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Fondo general de la app: Beige/Hueso muy sutil y elegante */
    [data-testid="stAppViewContainer"] {
        background-color: #F9F7F2; 
    }

    /* Estilo de los Títulos para que sean suaves y corporativos */
    h1, h2, h3, h4 {
        color: #2C3E50 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 400;
    }

    /* El título principal que va al lado del logo */
    .titulo-crm {
        font-size: 28px;
        font-weight: 600;
        color: #4A5568;
        letter-spacing: 2px;
        margin-top: 15px; /* Alineación vertical con el logo */
        margin-bottom: 0px;
    }

    /* Tarjetas/Formularios blancos flotantes sobre el fondo beige */
    div[data-testid="stForm"] {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.04);
        border: 1px solid #EBE6DF;
    }

    /* Estilo de los Dataframes (Tablas) */
    [data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.03);
    }
    
    /* Botones principales más estilizados */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 500;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# ⚙️ CONFIGURACIONES PRINCIPALES
# ==========================================
NOMBRE_LOGO = "logo.png" # <-- REVISA MAYÚSCULAS Y MINÚSCULAS EXACTAS DE TU GITHUB
URL_WEB_APP = "Pega_tu_URL_de_Apps_Script_AQUI" # <-- PEGA TU ENLACE LARGO AQUÍ


# --- FUNCIÓN VISUAL: CABECERA CON LOGO, TÍTULO Y BOTÓN DE SALIDA ---
def mostrar_cabecera(mostrar_salir=False):
    # Creamos tres columnas: logo (izquierda), título (centro), y botón de salir (derecha)
    col_logo, col_titulo, col_salir = st.columns([1, 7, 2])
    
    with col_logo:
        try:
            st.image(NOMBRE_LOGO, width=80) 
        except:
            # Si falla, ahora te avisará exactamente qué archivo está buscando
            st.error(f"Falta imagen: {NOMBRE_LOGO}") 
            
    with col_titulo:
        st.markdown('<p class="titulo-crm">CRM - PROYECTOS</p>', unsafe_allow_html=True)
        
    with col_salir:
        if mostrar_salir:
            st.write("<br>", unsafe_allow_html=True) # Empujamos el botón hacia abajo para alinearlo
            if st.button("🚪 Cerrar Sesión", use_container_width=True):
                # Borrar credenciales y memoria temporal
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
    
    st.markdown("---") # Línea divisoria


# --- FUNCIONES DE BASE DE DATOS (Apps Script) ---
def cargar_datos():
    try:
        res = requests.get(URL_WEB_APP)
        data = res.json()
        if len(data) > 1:
            return pd.DataFrame(data[1:], columns=data[0])
        elif len(data) == 1:
            return pd.DataFrame(columns=data[0])
    except:
        pass
    return pd.DataFrame(columns=[
        'ID_Proyecto', 'Cliente', 'Nombre_Contacto', 'Telefono_Contacto', 'Nombre_Proyecto', 'Sector', 'Presupuesto_$', 'Avance_%',
        'Responsable', 'Prioridad', 'Fecha_Inicio', 'Fecha_Cierre_Est', 
        'Estado_Detallado', 'Acciones_Realizadas', 'Proximas_Acciones', 'Observaciones'
    ])

def guardar_datos(df):
    try:
        df_clean = df.fillna("").astype(str)
        data_list = [df_clean.columns.tolist()]
        
        for row in df_clean.itertuples(index=False, name=None):
            data_list.append(list(row))
        
        payload = {"action": "overwrite", "data": data_list}
        res = requests.post(URL_WEB_APP, json=payload, allow_redirects=True)
        
        if res.status_code not in [200, 201]:
            st.error(f"⚠️ Google respondió con error: {res.status_code}")
    except Exception as e:
        st.error(f"⚠️ Error al enviar datos: {e}")

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
        # PANTALLA DE LOGIN CON DISEÑO
        st.write("<br><br>", unsafe_allow_html=True) # Espaciado superior
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            mostrar_cabecera(mostrar_salir=False) # Cabecera sin botón de salir
            with st.form("login_form"):
                st.markdown("#### Ingreso Seguro")
                st.text_input("Usuario", key="username")
                st.text_input("Contraseña", type="password", key="password")
                st.form_submit_button("Acceder al Sistema", on_click=password_entered, use_container_width=True)
        return False
        
    elif not st.session_state["password_correct"]:
        # PANTALLA DE ERROR EN LOGIN
        st.write("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            mostrar_cabecera(mostrar_salir=False) # Cabecera sin botón de salir
            with st.form("login_form_error"):
                st.markdown("#### Ingreso Seguro")
                st.text_input("Usuario", key="username")
                st.text_input("Contraseña", type="password", key="password")
                st.form_submit_button("Acceder al Sistema", on_click=password_entered, use_container_width=True)
            st.error("😕 Credenciales incorrectas. Inténtalo de nuevo.")
        return False
        
    return True

# --- EJECUCIÓN DEL CRM ---
if check_password():
    
    # 0. Mostrar Cabecera Profesional en todas las páginas internas (SÍ MOSTRAR BOTÓN SALIR)
    mostrar_cabecera(mostrar_salir=True)

    # 1. Cargar Base de Datos
    if 'crm_db' not in st.session_state:
        st.session_state.crm_db = cargar_datos()

    # 2. Control de Vistas
    if 'vista_actual' not in st.session_state:
        st.session_state.vista_actual = 'resumen'
    if 'proyecto_activo' not in st.session_state:
        st.session_state.proyecto_activo = None

    # ====================================================
    # VISTA 1: RESUMEN GENERAL 
    # ====================================================
    if st.session_state.vista_actual == 'resumen':
        st.markdown("### 📊 Resumen General")
        
        columnas_basicas = ['ID_Proyecto', 'Cliente', 'Nombre_Proyecto', 'Sector', 'Responsable', 'Presupuesto_$', 'Avance_%']
        
        if not st.session_state.crm_db.empty:
            st.session_state.crm_db['Presupuesto_$'] = pd.to_numeric(st.session_state.crm_db['Presupuesto_$'], errors='coerce').fillna(0)
            st.session_state.crm_db['Avance_%'] = pd.to_numeric(st.session_state.crm_db['Avance_%'], errors='coerce').fillna(0).astype(int)

            st.dataframe(
                st.session_state.crm_db[columnas_basicas], 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "Presupuesto_$": st.column_config.NumberColumn("Presupuesto ($)", format="$ %,.2f"),
                    "Avance_%": st.column_config.ProgressColumn("Avance (%)", format="%d%%", min_value=0, max_value=100)
                }
            )
        else:
            st.info("No hay proyectos registrados en tu base de datos todavía.")

        st.write("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🔍 Ver Detalles de Proyecto")
            lista_ids = st.session_state.crm_db['ID_Proyecto'].dropna().tolist() if not st.session_state.crm_db.empty else []
            
            if lista_ids:
                seleccion = st.selectbox("Seleccione el Proyecto:", lista_ids)
                if st.button("➡️ Ingresar al Proyecto", type="primary"):
                    st.session_state.proyecto_activo = seleccion
                    st.session_state.vista_actual = 'detalles'
                    st.rerun()
                
        with col2:
            st.markdown("#### ➕ Nuevo Registro")
            st.write("Abre el formulario para ingresar una nueva obra o proyecto.")
            if st.button("➕ Crear Proyecto", type="primary"):
                st.session_state.vista_actual = 'nuevo'
                st.rerun()

    # ====================================================
    # VISTA 2: FICHA DETALLADA 
    # ====================================================
    elif st.session_state.vista_actual == 'detalles':
        if st.button("🔙 Volver al Resumen"):
            st.session_state.vista_actual = 'resumen'
            st.rerun()
            
        idx = st.session_state.crm_db[st.session_state.crm_db['ID_Proyecto'] == st.session_state.proyecto_activo].index[0]
        
        col_tit, col_borrar = st.columns([4, 1])
        with col_tit:
            st.markdown(f"### 📂 Ficha del Proyecto: **{st.session_state.proyecto_activo}**")
        with col_borrar:
            st.write("") 
            if st.button("🗑️ Borrar Proyecto"):
                with st.spinner("Borrando registro... ⏳"):
                    st.session_state.crm_db = st.session_state.crm_db.drop(idx).reset_index(drop=
