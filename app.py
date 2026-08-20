import streamlit as st
import pandas as pd
from datetime import date
import requests
import json
import time

# Configuración principal de la ventana
st.set_page_config(
    page_title="CRM Proyectos | Sistema de Control Integral",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# ⚙️ CONFIGURACIONES PRINCIPALES
# ==========================================
NOMBRE_LOGO = "logo.jpg" # Nombre exacto de tu archivo en GitHub
URL_WEB_APP = "https://script.google.com/macros/s/AKfycbxvYHu0QM4CGbxk-0Ex2JIwWjDk7Ui6l1FgV2E1ygfAnfJlf-DTVfJfKQ7GffegFEHU/exec" # Tu enlace de Google Apps Script

# ==========================================
# 🎨 CSS PROFESIONAL Y DISEÑO INTEGRAL
# ==========================================
st.markdown("""
    <style>
    /* Ocultar elementos innecesarios de la interfaz nativa */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}

    /* Fondo general: Perla / Pizarra ultra limpio y sofisticado */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
    }

    /* Tipografía General */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* BANNER Y TITULO PRINCIPAL */
    .header-container {
        background: #FFFFFF;
        padding: 24px 32px;
        border-radius: 16px;
        box-shadow: 0px 10px 25px -5px rgba(15, 23, 42, 0.05), 0px 8px 10px -6px rgba(15, 23, 42, 0.03);
        border: 1px solid #E2E8F0;
        margin-bottom: 25px;
    }

    .titulo-principal {
        font-size: 42px !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        letter-spacing: 2px !important;
        line-height: 1.1 !important;
        margin: 0 !important;
        padding: 0 !important;
        text-transform: uppercase;
    }

    .subtitulo-marca {
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #D97706 !important; /* Acento cálido / dorado */
        letter-spacing: 4px !important;
        text-transform: uppercase;
        margin-top: 6px !important;
        margin-bottom: 0 !important;
    }

    /* TARJETAS DE MÉTRICAS / KPIS */
    .kpi-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 18px 22px;
        border: 1px solid #E2E8F0;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.06);
    }
    .kpi-titulo {
        font-size: 12px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .kpi-valor {
        font-size: 26px;
        font-weight: 800;
        color: #0F172A;
        margin-top: 4px;
    }

    /* FORMULARIOS Y CONTENEDORES FLOTANTES */
    div[data-testid="stForm"] {
        background-color: #FFFFFF;
        border-radius: 18px;
        padding: 32px;
        box-shadow: 0px 20px 25px -5px rgba(0, 0, 0, 0.05), 0px 8px 10px -6px rgba(0, 0, 0, 0.02);
        border: 1px solid #E2E8F0;
    }

    /* BORDES DE ENTRADA DE TEXTO */
    .stTextInput input, .stSelectbox select, .stNumberInput input, .stTextArea textarea {
        border-radius: 8px !important;
        border: 1px solid #CBD5E1 !important;
        padding: 10px 14px !important;
        font-size: 15px !important;
    }
    .stTextInput input:focus, .stSelectbox select:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: #D97706 !important;
        box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.15) !important;
    }

    /* BOTONES */
    div.stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        padding: 12px 24px !important;
        letter-spacing: 0.5px !important;
        transition: all 0.25s ease !important;
    }
    div.stButton > button[type="primary"] {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.25) !important;
    }
    div.stButton > button[type="primary"]:hover {
        background: linear-gradient(135deg, #334155 0%, #1E293B 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0px 6px 18px rgba(15, 23, 42, 0.35) !important;
    }

    /* TABLA DATAFRAME ELEGANTE */
    [data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border-radius: 14px;
        padding: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.02);
    }
    </style>
""", unsafe_allow_html=True)


# --- CABECERA DE MARCA PRINCIPAL ---
def mostrar_cabecera(mostrar_salir=False):
    col_logo, col_info, col_accion = st.columns([2.5, 6.5, 3])
    
    with col_logo:
        try:
            # Logo con amplitud prominente
            st.image(NOMBRE_LOGO, width=280)
        except:
            st.warning(f"⚠️ Imagen '{NOMBRE_LOGO}' no encontrada en GitHub")
            
    with col_info:
        st.markdown('<p class="titulo-principal">CRM PROYECTOS</p>', unsafe_allow_html=True)
        st.markdown('<p class="subtitulo-marca">Plataforma de Control Integral & Gestión Directiva</p>', unsafe_allow_html=True)
        
    with col_accion:
        if mostrar_salir:
            st.write("<br>", unsafe_allow_html=True)
            if st.button("🚪 Cerrar Sesión", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
                
    st.markdown("<hr style='border: none; height: 1px; background: #E2E8F0; margin: 20px 0 30px 0;'>", unsafe_allow_html=True)


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


# --- LOGIN DE ALTO NIVEL ---
def check_password():
    def password_entered():
        if st.session_state["username"] in st.secrets["passwords"] and \
           st.session_state["password"] == st.secrets["passwords"][st.session_state["username"]]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state or not st.session_state["password_correct"]:
        st.write("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2.2, 1])
        
        with col2:
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            try:
                st.image(NOMBRE_LOGO, width=320)
            except:
                pass
            st.markdown('<p class="titulo-principal" style="text-align: center; margin-top: 15px !important;">CRM PROYECTOS</p>', unsafe_allow_html=True)
            st.markdown('<p class="subtitulo-marca" style="text-align: center; margin-bottom: 25px !important;">CONTROL Y GESTIÓN ESTRATÉGICA</p>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            with st.form("login_form"):
                st.markdown("<h4 style='color: #0F172A; font-weight: 700; margin-bottom: 20px;'>🔒 Iniciar Sesión</h4>", unsafe_allow_html=True)
                st.text_input("Usuario Corporativo", key="username")
                st.text_input("Contraseña de Acceso", type="password", key="password")
                st.write("<br>", unsafe_allow_html=True)
                st.form_submit_button("ACCEDER AL PANEL", on_click=password_entered, use_container_width=True, type="primary")

        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            col1, col2, col3 = st.columns([1, 2.2, 1])
            with col2:
                st.error("😕 Credenciales de acceso incorrectas. Verifique e intente nuevamente.")
        return False
        
    return True


# --- EJECUCIÓN PRINCIPAL DEL CRM ---
if check_password():
    
    # 1. Cargar Cabecera
    mostrar_cabecera(mostrar_salir=True)

    # 2. Inicializar Base de Datos en Sesión
    if 'crm_db' not in st.session_state:
        st.session_state.crm_db = cargar_datos()

    if 'vista_actual' not in st.session_state:
        st.session_state.vista_actual = 'resumen'
    if 'proyecto_activo' not in st.session_state:
        st.session_state.proyecto_activo = None

    # ====================================================
    # VISTA 1: RESUMEN GENERAL (DASHBOARD EJECUTIVO)
    # ====================================================
    if st.session_state.vista_actual == 'resumen':
        
        # --- TARJETAS DE MÉTRICAS RÁPIDAS ---
        if not st.session_state.crm_db.empty:
            st.session_state.crm_db['Presupuesto_$'] = pd.to_numeric(st.session_state.crm_db['Presupuesto_$'], errors='coerce').fillna(0)
            st.session_state.crm_db['Avance_%'] = pd.to_numeric(st.session_state.crm_db['Avance_%'], errors='coerce').fillna(0).astype(int)

            total_proyectos = len(st.session_state.crm_db)
            suma_presupuesto = st.session_state.crm_db['Presupuesto_$'].sum()
            promedio_avance = st.session_state.crm_db['Avance_%'].mean()

            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-titulo">📂 Proyectos Registrados</div>
                        <div class="kpi-valor">{total_proyectos} Obras/Servicios</div>
                    </div>
                """, unsafe_allow_html=True)
            with kpi2:
                st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-titulo">💰 Portafolio Financiero Total</div>
                        <div class="kpi-valor">${suma_presupuesto:,.2f}</div>
                    </div>
                """, unsafe_allow_html=True)
            with kpi3:
                st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-titulo">📈 Avance Promedio Global</div>
                        <div class="kpi-valor">{promedio_avance:.1f}%</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.write("<br>", unsafe_allow_html=True)

        # --- TABLA DE PROYECTOS ---
        st.markdown("<h3 style='color: #0F172A; font-weight: 700; margin-bottom: 15px;'>📊 Resumen de Obras y Proyectos</h3>", unsafe_allow_html=True)
        columnas_basicas = ['ID_Proyecto', 'Cliente', 'Nombre_Proyecto', 'Sector', 'Responsable', 'Presupuesto_$', 'Avance_%']
        
        if not st.session_state.crm_db.empty:
            st.dataframe(
                st.session_state.crm_db[columnas_basicas], 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "ID_Proyecto": st.column_config.TextColumn("ID / Código"),
                    "Nombre_Proyecto": st.column_config.TextColumn("Nombre del Proyecto"),
                    "Presupuesto_$": st.column_config.NumberColumn("Presupuesto ($)", format="$ %,.2f"),
                    "Avance_%": st.column_config.ProgressColumn("Avance Ejecutado (%)", format="%d%%", min_value=0, max_value=100)
                }
            )
        else:
            st.info("ℹ️ No hay proyectos registrados en tu base de datos todavía.")

        st.write("<br><br>", unsafe_allow_html=True)
        
        # --- ACCIONES PRINCIPALES ---
        col_det, col_crear = st.columns(2)
        
        with col_det:
            st.markdown("<h4 style='color: #0F172A; font-weight: 700;'>🔍 Inspeccionar Ficha de Proyecto</h4>", unsafe_allow_html=True)
            lista_ids = st.session_state.crm_db['ID_Proyecto'].dropna().tolist() if not st.session_state.crm_db.empty else []
            
            if lista_ids:
                seleccion = st.selectbox("Seleccione el Proyecto por Código ID:", lista_ids)
                if st.button("➡️ INGRESAR A LA FICHA TÉCNICA", type="primary"):
                    st.session_state.proyecto_activo = seleccion
                    st.session_state.vista_actual = 'detalles'
                    st.rerun()
            else:
                st.write("Registra un proyecto para activar la vista detallada.")
                
        with col_crear:
            st.markdown("<h4 style='color: #0F172A; font-weight: 700;'>➕ Nueva Alta de Proyecto</h4>", unsafe_allow_html=True)
            st.write("Abre la bitácora para ingresar una nueva obra o contrato.")
            if st.button("➕ REGISTRAR NUEVO PROYECTO", type="primary"):
                st.session_state.vista_actual = 'nuevo'
                st.rerun()

    # ====================================================
    # VISTA 2: FICHA DETALLADA Y EDICIÓN
    # ====================================================
    elif st.session_state.vista_actual == 'detalles':
        if st.button("🔙 VOLVER AL RESUMEN GENERAL"):
            st.session_state.vista_actual = 'resumen'
            st.rerun()
            
        idx = st.session_state.crm_db[st.session_state.crm_db['ID_Proyecto'] == st.session_state.proyecto_activo].index[0]
        
        col_tit, col_borrar = st.columns([4, 1.2])
        with col_tit:
            st.markdown(f"<h3 style='color: #0F172A; font-weight: 800;'>📂 Expediente del Proyecto: <span style='color: #D97706;'>{st.session_state.proyecto_activo}</span></h3>", unsafe_allow_html=True)
        with col_borrar:
            st.write("") 
            if st.button("🗑️ Eliminar Proyecto"):
                with st.spinner("Eliminando expediente de Google Drive... ⏳"):
                    st.session_state.crm_db = st.session_state.crm_db.drop(idx).reset_index(drop=True)
                    guardar_datos(st.session_state.crm_db)
                st.success("✅ Registro eliminado correctamente.")
                time.sleep(1.5)
                st.session_state.vista_actual = 'resumen'
                st.rerun()

        with st.form("form_detalles"):
            st.markdown("<h5 style='color: #0F172A; font-weight: 700;'>1. Información General y Contacto</h5>", unsafe_allow_html=True)
            c_p1, c_p2, c_p3 = st.columns(3)
            with c_p1: act_nombre = st.text_input("Nombre de la Obra / Proyecto", value=str(st.session_state.crm_db.at[idx, 'Nombre_Proyecto']))
            with c_p2: act_cliente = st.text_input("Cliente / Razón Social", value=str(st.session_state.crm_db.at[idx, 'Cliente']))
            with c_p3: 
                try: val_presupuesto = float(st.session_state.crm_db.at[idx, 'Presupuesto_$'])
                except: val_presupuesto = 0.0
                act_presupuesto = st.number_input("Presupuesto Adjudicado ($)", min_value=0.0, value=val_presupuesto, format="%.2f", step=100.0)

            c_id1, c_id2, c_id3, c_id4 = st.columns(4)
            with c_id1: act_contacto = st.text_input("Persona de Contacto", value=str(st.session_state.crm_db.at[idx, 'Nombre_Contacto']))
            with c_id2: act_telefono = st.text_input("Teléfono Directo", value=str(st.session_state.crm_db.at[idx, 'Telefono_Contacto']))
            with c_id3: 
                sectores = ["Arquitectura", "Construcción", "Consultoría", "Corretaje"]
                sect_actual = str(st.session_state.crm_db.at[idx, 'Sector'])
                act_sector = st.selectbox("Sector de Actividad", sectores, index=sectores.index(sect_actual) if sect_actual in sectores else 0)
            with c_id4: act_resp = st.text_input("Director / Responsable", value=str(st.session_state.crm_db.at[idx, 'Responsable']))

            st.write("<hr style='border: none; height: 1px; background: #E2E8F0; margin: 15px 0;'>", unsafe_allow_html=True)
            st.markdown("<h5 style='color: #0F172A; font-weight: 700;'>2. Planificación Estratégica</h5>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            try: val_avance = int(st.session_state.crm_db.at[idx, 'Avance_%'])
            except: val_avance = 0
            with c1: act_avance = st.number_input("Porcentaje de Avance Actual (%)", 0, 100, val_avance)
            with c2: 
                prio_actual = str(st.session_state.crm_db.at[idx, 'Prioridad'])
                act_prio = st.selectbox("Prioridad de Ejecución", ["Alta", "Media", "Baja"], index=["Alta", "Media", "Baja"].index(prio_actual) if prio_actual in ["Alta", "Media", "Baja"] else 1)
            with c3: act_cierre = st.text_input("Fecha Estimada de Finalización", value=str(st.session_state.crm_db.at[idx, 'Fecha_Cierre_Est']))
            
            st.write("<hr style='border: none; height: 1px; background: #E2E8F0; margin: 15px 0;'>", unsafe_allow_html=True)
            st.markdown("<h5 style='color: #0F172A; font-weight: 700;'>3. Bitácora de Campo y Seguimiento</h5>", unsafe_allow_html=True)
            colA, colB = st.columns(2)
            with colA:
                act_estado = st.text_area("Diagnóstico / Estado Operativo Actual", value=str(st.session_state.crm_db.at[idx, 'Estado_Detallado']), height=110)
                act_acciones = st.text_area("Acciones Ejecutadas Recientemente", value=str(st.session_state.crm_db.at[idx, 'Acciones_Realizadas']), height=110)
            with colB:
                act_proximas = st.text_area("Próximos Hitos a Cumplir", value=str(st.session_state.crm_db.at[idx, 'Proximas_Acciones']), height=110)
                act_obs = st.text_area("Observaciones Generales", value=str(st.session_state.crm_db.at[idx, 'Observaciones']), height=110)
            
            st.write("<br>", unsafe_allow_html=True)
            if st.form_submit_button("💾 GUARDAR TODOS LOS CAMBIOS", type="primary", use_container_width=True):
                with st.spinner("Sincronizando expediente con Google Drive... ⏳"):
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
                
                st.success("✅ ¡Expediente actualizado y guardado en la nube!")
                time.sleep(2)
                st.session_state.vista_actual = 'resumen'
                st.rerun()

    # ====================================================
    # VISTA 3: REGISTRO DE NUEVO PROYECTO
    # ====================================================
    elif st.session_state.vista_actual == 'nuevo':
        if st.button("🔙 VOLVER AL RESUMEN GENERAL"):
            st.session_state.vista_actual = 'resumen'
            st.rerun()
            
        st.markdown("<h3 style='color: #0F172A; font-weight: 800;'>➕ Apertura de Nuevo Proyecto</h3>", unsafe_allow_html=True)
        
        with st.form("form_nuevo_proyecto"):
            st.markdown("<h5 style='color: #0F172A; font-weight: 700;'>Datos de Apertura</h5>", unsafe_allow_html=True)
            
            c_1, c_2, c_3 = st.columns(3)
            with c_1:
                n_id = st.text_input("Código / ID Único de Proyecto *")
                n_cli = st.text_input("Cliente / Empresa")
                n_nom = st.text_input("Nombre del Proyecto / Obra *")
            with c_2:
                n_cont = st.text_input("Nombre de Contacto")
                n_tel = st.text_input("Teléfono de Contacto")
                n_sec = st.selectbox("Sector de Servicio", ["Arquitectura", "Construcción", "Consultoría", "Corretaje"])
            with c_3:
                n_pres = st.number_input("Presupuesto Inicial ($)", min_value=0.0, value=None, format="%.2f", step=100.0)
                n_resp = st.text_input("Director de Proyecto / Responsable")
                
            st.write("<br>", unsafe_allow_html=True)
            if st.form_submit_button("✅ REGISTRAR Y GUARDAR EN DRIVE", type="primary", use_container_width=True):
                if n_id == "" or n_nom == "":
                    st.error("⚠️ El Código ID y el Nombre del Proyecto son campos obligatorios.")
                else:
                    with st.spinner("Creando nuevo registro en Google Sheets... ⏳"):
                        nueva_fila = {
                            'ID_Proyecto': n_id, 'Cliente': n_cli, 'Nombre_Contacto': n_cont, 'Telefono_Contacto': n_tel, 
                            'Nombre_Proyecto': n_nom, 'Sector': n_sec, 
                            'Presupuesto_$': n_pres if n_pres is not None else 0.0, 
                            'Avance_%': 0, 'Responsable': n_resp, 'Prioridad': 'Media', 'Fecha_Inicio': str(date.today()), 
                            'Fecha_Cierre_Est': '', 'Estado_Detallado': '', 'Acciones_Realizadas': '', 
                            'Proximas_Acciones': '', 'Observaciones': ''
                        }
                        
                        df_nuevo = pd.DataFrame([nueva_fila])
                        st.session_state.crm_db = pd.concat([st.session_state.crm_db, df_nuevo], ignore_index=True)
                        guardar_datos(st.session_state.crm_db)
                    
                    st.success("✅ ¡Nuevo proyecto aperturado y guardado en Google Drive con éxito!")
                    time.sleep(2)
                    st.session_state.vista_actual = 'resumen'
                    st.rerun()

# --- FIN DEL CÓDIGO ---
