import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from streamlit_gsheets import GSheetsConnection

# 1. Configuración de página móvil
st.set_page_config(page_title="Baby Log", layout="centered")

# Estilos CSS definitivos para forzar la fila horizontal por tarjeta
st.markdown("""
    <style>
    /* Ocultar elementos nativos innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fondo limpio para la aplicación */
    .stApp {
        background-color: #F8FAFC !important;
    }
    
    /* Optimizar los márgenes en pantallas de teléfono */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 450px !important;
    }

    /* FORZAR LA VISTA EN FILA (Icono izquierda, Contenido derecha) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important; 
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 24px;
        padding: 1rem !important;
        margin-bottom: 0.75rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
    }

    /* Columna 1: Contenedor del Icono (Ancho fijo) */
    [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(1) {
        flex: 0 0 65px !important;
        min-width: 65px !important;
        max-width: 65px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    /* Columna 2: Contenedor del Texto + Botón Registrar */
    [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(2) {
        flex: 1 1 auto !important;
        padding-left: 0.75rem !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 0.25rem !important;
    }

    /* Forzar que el botón ocupe todo el ancho de su columna */
    .stButton, .stButton>button {
        width: 100% !important;
    }

    /* Estilo del botón Registrar */
    .stButton>button {
        border-radius: 12px !important;
        border: 1px solid #CBD5E1 !important;
        background-color: #F8FAFC !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        color: #475569 !important;
        padding: 0.5rem 1rem !important;
    }
    
    .stButton>button:active {
        background-color: #E2E8F0 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #334155; margin-bottom: 1.5rem; font-size: 26px;'>Registro de Pañales 👶</h2>", unsafe_allow_html=True)

# 2. Conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def guardar_registro(tipo):
    tipo_limpio = "Pipi" if tipo == "Pipí" else tipo
    zona_madrid = ZoneInfo("Europe/Madrid")
    ahora = datetime.now(zona_madrid)
    
    fecha = ahora.strftime("%Y-%m-%d")
    hora = ahora.strftime("%H:%M:%S")
    
    try:
        df_existente = conn.read(ttl=0)
        nueva_fila = pd.DataFrame([[fecha, hora, tipo_limpio]], columns=["Fecha", "Hora", "Tipo"])
        df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
        conn.update(data=df_actualizado)
        st.toast(f"💾 Guardado: {tipo_limpio} ({hora})", icon="👶")
    except Exception as e:
        st.error(f"Error: {e}")

# 3. Interfaz Vertical de 2 Columnas (Icono Nativo + Texto/Botón)

# Fila 1: Pipí
col1_img, col1_content = st.columns([1, 3])
with col1_img:
    st.image("pipiapp.png", use_container_width=True)
with col1_content:
    st.markdown("<span style='font-weight:700; font-size:18px; color:#334155;'>Pipí</span>", unsafe_allow_html=True)
    st.button("Registrar", key="btn_pipi", on_click=guardar_registro, args=("Pipí",))

# Fila 2: Caca
col2_img, col2_content = st.columns([1, 3])
with col2_img:
    st.image("cacaapp.png", use_container_width=True)
with col2_content:
    st.markdown("<span style='font-weight:700; font-size:18px; color:#334155;'>Caca</span>", unsafe_allow_html=True)
    st.button("Registrar", key="btn_caca", on_click=guardar_registro, args=("Caca",))

# Fila 3: Ambos
col3_img, col3_content = st.columns([1, 3])
with col3_img:
    st.image("ambosapp.png", use_container_width=True)
with col3_content:
    st.markdown("<span style='font-weight:700; font-size:18px; color:#334155;'>Ambos</span>", unsafe_allow_html=True)
    st.button("Registrar", key="btn_ambos", on_click=guardar_registro, args=("Ambos",))
