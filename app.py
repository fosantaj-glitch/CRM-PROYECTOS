import streamlit as st
import pandas as pd
import os
from datetime import date

# Configuración de la página
st.set_page_config(page_title="CRM Proyectos", layout="wide")

# --- CSS PARA DISEÑO LIMPIO ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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
        st.title("🔒 Acceso al CRM")
        st.text_input("Usuario", key="username")
        st.text_input("Contraseña", type="password", key="password")
        st.button("Ingresar", on_click=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        st.title("🔒 Acceso al CRM")
        st.text_input("Usuario", key="username")
        st.text_input("Contraseña", type="password", key="password")
        st.button("Ingresar", on_click=password_entered)
        st.error("😕 Usuario o contraseña incorrectos")
        return False
    return True

# --- EJECUCIÓN DEL CRM ---
if check_password():
    # 1. Base de datos inicial
    if 'crm_db' not in st.session_state:
        st.session_state.crm_db = pd.DataFrame(columns=[
            'ID_Proyecto', 'Cliente', 'Nombre_Proyecto', 'Sector', 'Presupuesto_$', 'Avance_%',
            'Responsable', 'Prioridad', 'Fecha_Inicio', 'Fecha_Cierre_Est', 
            'Estado_Detallado', 'Acciones_Realizadas', 'Proximas_Acciones', 'Observaciones'
        ])
        st.session_state.crm_db.loc[0] = ['PRJ-001', 'Ejemplo S.A.', 'Proyecto Alfa', 'Arquitectura', 1500, 25, 'Nico', 'Alta', str(date.today()), '', 'Planificación', 'Diseño inicial', 'Aprobar planos', 'Ninguna']

    # 2. Control de Vistas (Páginas)
    if 'vista_actual' not in st.session_state:
        st.session_state.vista_actual = 'resumen'
    if 'proyecto_activo' not in st.session_state:
        st.session_state.proyecto_activo = None

    # ====================================================
    # VISTA 1: RESUMEN GENERAL (PANTALLA PRINCIPAL LIMPIA)
    # ====================================================
    if st.session_state.vista_actual == 'resumen':
        st.title("📊 Resumen General de Proyectos")
        
        columnas_basicas = ['ID_Proyecto', 'Cliente', 'Nombre_Proyecto', 'Sector', 'Responsable', 'Avance_%']
        st.dataframe(st.session_state.crm_db[columnas_basicas], use_container_width=True, hide_index=True)

        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🔍 Ver Detalles de Proyecto")
            lista_ids = st.session_state.crm_db['ID_Proyecto'].tolist()
            if lista_ids:
                seleccion = st.selectbox("Seleccione el Proyecto:", lista_ids)
                if st.button("➡️ Ingresar al Proyecto", type="primary"):
                    st.session_state.proyecto_activo = seleccion
                    st.session_state.vista_actual = 'detalles'
                    st.rerun()
            else:
                st.info("No hay proyectos registrados.")
                
        with col2:
            st.markdown("### ➕ Registrar")
            st.write("Abre el formulario para crear un nuevo proyecto.")
            if st.button("➕ CREAR NUEVO PROYECTO", type="primary"):
                st.session_state.vista_actual = 'nuevo'
                st.rerun()

    # ====================================================
    # VISTA 2: FICHA DETALLADA (SOLO SE VE AL INGRESAR)
    # ====================================================
    elif st.session_state.vista_actual == 'detalles':
        if st.button("🔙 Volver al Resumen"):
            st.session_state.vista_actual = 'resumen'
            st.rerun()
            
        idx = st.session_state.crm_db[st.session_state.crm_db['ID_Proyecto'] == st.session_state.proyecto_activo].index[0]
        nombre_proy = st.session_state.crm_db.at[idx, 'Nombre_Proyecto']
        
        col_tit, col_borrar = st.columns([4, 1])
        with col_tit:
            st.title(f"📂 Detalles: {nombre_proy}")
        with col_borrar:
            st.write("") # Espaciador
            if st.button("🗑️ Borrar Proyecto"):
                st.session_state.crm_db = st.session_state.crm_db.drop(idx).reset_index(drop=True)
                st.session_state.vista_actual = 'resumen'
                st.rerun()

        with st.form("form_detalles"):
            c1, c2, c3, c4 = st.columns(4)
            with c1: act_avance = st.number_input("Avance (%)", 0, 100, int(st.session_state.crm_db.at[idx, 'Avance_%']))
            with c2: act_resp = st.text_input("Responsable", value=st.session_state.crm_db.at[idx, 'Responsable'])
            with c3: act_prio = st.selectbox("Prioridad", ["Alta", "Media", "Baja"], index=["Alta", "Media", "Baja"].index(st.session_state.crm_db.at[idx, 'Prioridad']) if st.session_state.crm_db.at[idx, 'Prioridad'] in ["Alta", "Media", "Baja"] else 1)
            with c4: act_cierre = st.text_input("Fecha Cierre Est.", value=st.session_state.crm_db.at[idx, 'Fecha_Cierre_Est'])
            
            colA, colB = st.columns(2)
            with colA:
                act_estado = st.text_area("Estado Actual (Descripción Detallada)", value=st.session_state.crm_db.at[idx, 'Estado_Detallado'], height=120)
                act_acciones = st.text_area("Acciones Realizadas", value=st.session_state.crm_db.at[idx, 'Acciones_Realizadas'], height=120)
            with colB:
                act_proximas = st.text_area("Próximas Acciones", value=st.session_state.crm_db.at[idx, 'Proximas_Acciones'], height=120)
                act_obs = st.text_area("Observaciones Adicionales", value=st.session_state.crm_db.at[idx, 'Observaciones'], height=120)
            
            if st.form_submit_button("💾 Guardar Cambios"):
                st.session_state.crm_db.at[idx, 'Avance_%'] = act_avance
                st.session_state.crm_db.at[idx, 'Responsable'] = act_resp
                st.session_state.crm_db.at[idx, 'Prioridad'] = act_prio
                st.session_state.crm_db.at[idx, 'Fecha_Cierre_Est'] = act_cierre
                st.session_state.crm_db.at[idx, 'Estado_Detallado'] = act_estado
                st.session_state.crm_db.at[idx, 'Acciones_Realizadas'] = act_acciones
                st.session_state.crm_db.at[idx, 'Proximas_Acciones'] = act_proximas
                st.session_state.crm_db.at[idx, 'Observaciones'] = act_obs
                st.success("Cambios guardados correctamente.")
                st.session_state.vista_actual = 'resumen'
                st.rerun()

    # ====================================================
    # VISTA 3: CREAR NUEVO PROYECTO
    # ====================================================
    elif st.session_state.vista_actual == 'nuevo':
        if st.button("🔙 Volver al Resumen"):
            st.session_state.vista_actual = 'resumen'
            st.rerun()
            
        st.title("➕ Crear Nuevo Proyecto")
        
        with st.form("form_nuevo_proyecto"):
            st.markdown("### Datos Básicos del Nuevo Proyecto")
            c_1, c_2, c_3 = st.columns(3)
            with c_1:
                n_id = st.text_input("ID Proyecto")
                n_cli = st.text_input("Cliente / Empresa")
            with c_2:
                n_nom = st.text_input("Nombre del Proyecto")
                n_sec = st.selectbox("Sector", ["Arquitectura", "Construcción", "Consultoría", "Corretaje"])
            with c_3:
                n_pres = st.number_input("Presupuesto ($)", min_value=0.0)
                n_resp = st.text_input("Responsable")
                
            if st.form_submit_button("✅ Guardar Nuevo Proyecto"):
                if n_id == "" or n_nom == "":
                    st.error("Por favor ingresa al menos el ID y el Nombre del Proyecto.")
                else:
                    nueva_fila = {
                        'ID_Proyecto': n_id, 'Cliente': n_cli, 'Nombre_Proyecto': n_nom, 
                        'Sector': n_sec, 'Presupuesto_$': n_pres, 'Avance_%': 0,
                        'Responsable': n_resp, 'Prioridad': 'Media', 'Fecha_Inicio': str(date.today()), 
                        'Fecha_Cierre_Est': '', 'Estado_Detallado': '', 'Acciones_Realizadas': '', 
                        'Proximas_Acciones': '', 'Observaciones': ''
                    }
                    st.session_state.crm_db = pd.concat([st.session_state.crm_db, pd.DataFrame([nueva_fila])], ignore_index=True)
                    st.success("Proyecto agregado con éxito.")
                    st.session_state.vista_actual = 'resumen'
                    st.rerun()
