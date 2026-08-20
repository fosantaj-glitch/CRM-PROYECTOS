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
    div.stButton > button:first-child {
        border-radius: 8px;
        font-weight: 500;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# ⚙️ CONFIGURACIONES PRINCIPALES
# ==========================================
NOMBRE_LOGO = "logo.png" # <-- ASEGÚRATE DE QUE EL NOMBRE SEA EXACTO AL DE GITHUB
URL_WEB_APP = "https://script.google.com/macros/s/AKfycbxvYHu0QM4CGbxk-0Ex2JIwWjDk7Ui6l1FgV2E1ygfAnfJlf-DTVfJfKQ7GffegFEHU/exec" # <-- PEGA TU ENLACE LARGO AQUÍ


# --- FUNCIÓN VISUAL: CABECERA CON LOGO Y TÍTULO ---
def mostrar_cabecera():
    # Usamos columnas ajustadas: el logo ocupa poco espacio, el título el resto
    col_logo, col_titulo = st.columns([1, 10])
    
    with col_logo:
        try:
            st.image(NOMBRE_LOGO, width=80) # Logo compacto y elegante
        except:
            pass # Si no encuentra el logo, no muestra error feo, solo lo omite
            
    with col_titulo:
        # Texto con estilo CSS inyectado
        st.markdown('<p class="titulo-crm">CRM - PROYECTOS</p>', unsafe_allow_html=True)
    
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
            mostrar_cabecera()
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
            mostrar_cabecera()
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
    
    # 0. Mostrar Cabecera Profesional en todas las páginas internas
    mostrar_cabecera()

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
                    st.session_state.crm_db = st.session_state.crm_db.drop(idx).reset_index(drop=True)
                    guardar_datos(st.session_state.crm_db)
                st.success("✅ Proyecto borrado.")
                time.sleep(1.5)
                st.session_state.vista_actual = 'resumen'
                st.rerun()

        with st.form("form_detalles"):
            st.markdown("#### Datos Principales")
            c_p1, c_p2, c_p3 = st.columns(3)
            with c_p1: act_nombre = st.text_input("Nombre del Proyecto", value=str(st.session_state.crm_db.at[idx, 'Nombre_Proyecto']))
            with c_p2: act_cliente = st.text_input("Cliente / Empresa", value=str(st.session_state.crm_db.at[idx, 'Cliente']))
            with c_p3: 
                try: val_presupuesto = float(st.session_state.crm_db.at[idx, 'Presupuesto_$'])
                except: val_presupuesto = 0.0
                act_presupuesto = st.number_input("Presupuesto ($)", min_value=0.0, value=val_presupuesto, format="%.2f", step=100.0)

            c_id1, c_id2, c_id3, c_id4 = st.columns(4)
            with c_id1: act_contacto = st.text_input("Contacto Directo", value=str(st.session_state.crm_db.at[idx, 'Nombre_Contacto']))
            with c_id2: act_telefono = st.text_input("Teléfono", value=str(st.session_state.crm_db.at[idx, 'Telefono_Contacto']))
            with c_id3: 
                sectores = ["Arquitectura", "Construcción", "Consultoría", "Corretaje"]
                sect_actual = str(st.session_state.crm_db.at[idx, 'Sector'])
                act_sector = st.selectbox("Sector", sectores, index=sectores.index(sect_actual) if sect_actual in sectores else 0)
            with c_id4: act_resp = st.text_input("Responsable", value=str(st.session_state.crm_db.at[idx, 'Responsable']))

            st.markdown("#### Planificación y Avance")
            c1, c2, c3 = st.columns(3)
            try: val_avance = int(st.session_state.crm_db.at[idx, 'Avance_%'])
            except: val_avance = 0
            with c1: act_avance = st.number_input("Porcentaje de Avance (%)", 0, 100, val_avance)
            with c2: 
                prio_actual = str(st.session_state.crm_db.at[idx, 'Prioridad'])
                act_prio = st.selectbox("Prioridad Operativa", ["Alta", "Media", "Baja"], index=["Alta", "Media", "Baja"].index(prio_actual) if prio_actual in ["Alta", "Media", "Baja"] else 1)
            with c3: act_cierre = st.text_input("Fecha Estimada de Cierre", value=str(st.session_state.crm_db.at[idx, 'Fecha_Cierre_Est']))
            
            st.markdown("#### Bitácora de Ejecución")
            colA, colB = st.columns(2)
            with colA:
                act_estado = st.text_area("Estado Actual del Proyecto", value=str(st.session_state.crm_db.at[idx, 'Estado_Detallado']), height=100)
                act_acciones = st.text_area("Acciones Realizadas", value=str(st.session_state.crm_db.at[idx, 'Acciones_Realizadas']), height=100)
            with colB:
                act_proximas = st.text_area("Próximos Pasos", value=str(st.session_state.crm_db.at[idx, 'Proximas_Acciones']), height=100)
                act_obs = st.text_area("Observaciones Generales", value=str(st.session_state.crm_db.at[idx, 'Observaciones']), height=100)
            
            st.write("<br>", unsafe_allow_html=True)
            if st.form_submit_button("💾 Guardar Cambios", type="primary"):
                with st.spinner("Sincronizando con la nube... ⏳"):
                    st.session_state.crm_db.at[idx, 'Nombre_Proyecto'] = act_nombre
                    st.session_state.crm_db.at[idx, 'Cliente'] = act_cliente
                    st.session_state.crm_db.at[idx, 'Presupuesto_$'] = act_presupuesto
                    st.session_state.crm_db.at[idx, 'Nombre_Contacto'] = act_contacto
                    st.session_state.crm_db.at[idx, 'Telefono_Contacto'] = act_telefono
                    st.session_state.crm_db.at[idx, 'Sector'] = act_sector
                    st.session_state.crm_db.at[idx, 'Responsable'] = act_resp
                    st.session_state.crm_db.at[idx, 'Avance_%'] = act_avance
                    st.session_state.crm_db.at[idx, 'Prioridad'] = act_prio
                    st.session_state.crm_db.at[idx, 'Fecha_Cierre_Est'] = act_cierre
                    st.session_state.crm_db.at[idx, 'Estado_Detallado'] = act_estado
                    st.session_state.crm_db.at[idx, 'Acciones_Realizadas'] = act_acciones
                    st.session_state.crm_db.at[idx, 'Proximas_Acciones'] = act_proximas
                    st.session_state.crm_db.at[idx, 'Observaciones'] = act_obs
                    
                    guardar_datos(st.session_state.crm_db)
                
                st.success("✅ ¡Actualización guardada con éxito!")
                time.sleep(2)
                st.session_state.vista_actual = 'resumen'
                st.rerun()

    # ====================================================
    # VISTA 3: CREAR NUEVO PROYECTO
    # ====================================================
    elif st.session_state.vista_actual == 'nuevo':
        if st.button("🔙 Volver al Resumen"):
            st.session_state.vista_actual = 'resumen'
            st.rerun()
            
        st.markdown("### ➕ Registrar Nuevo Proyecto")
        
        with st.form("form_nuevo_proyecto"):
            st.markdown("#### Datos Básicos")
            
            c_1, c_2, c_3 = st.columns(3)
            with c_1:
                n_id = st.text_input("Código / ID Proyecto")
                n_cli = st.text_input("Cliente / Empresa")
                n_nom = st.text_input("Nombre del Proyecto")
            with c_2:
                n_cont = st.text_input("Nombre de Contacto")
                n_tel = st.text_input("Teléfono")
                n_sec = st.selectbox("Sector", ["Arquitectura", "Construcción", "Consultoría", "Corretaje"])
            with c_3:
                n_pres = st.number_input("Presupuesto Estimado ($)", min_value=0.0, value=None, format="%.2f", step=100.0)
                n_resp = st.text_input("Responsable Asignado")
                
            st.write("<br>", unsafe_allow_html=True)
            if st.form_submit_button("✅ Crear Registro", type="primary"):
                if n_id == "" or n_nom == "":
                    st.error("⚠️ El Código/ID y el Nombre del Proyecto son obligatorios.")
                else:
                    with st.spinner("Creando expediente en la nube... ⏳"):
                        nueva_fila = {
                            'ID_Proyecto': n_id, 'Cliente': n_cli, 'Nombre_Contacto': n_cont, 'Telefono_Contacto': n_tel, 
                            'Nombre_Proyecto': n_nom, 'Sector': n_sec,
