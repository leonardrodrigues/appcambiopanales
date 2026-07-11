import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from streamlit_gsheets import GSheetsConnection

# 1. Configuración de página móvil
st.set_page_config(page_title="Baby Log", layout="centered")

# Estilos CSS específicos para crear "Filas-Botón" masivas y táctiles
st.markdown("""
    <style>
    /* Ocultar elementos nativos innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Optimizar los márgenes en pantallas de teléfono */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        max-width: 480px !important;
    }

    /* FORZAR LA VISTA EN FILA (Imagen + Texto + Botón en línea) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important; /* Centra verticalmente los 3 elementos */
        justify-content: space-between !important;
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 0.75rem 1rem !important;
        margin-bottom: 0.75rem !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
        width: 100% !important;
    }
    
    /* Ajustes basados en los contenedores de columna nativos de Streamlit */
    [data-testid="stHorizontalBlock"] [data-testid="column"] {
        flex-grow: 1 !important;
        flex-shrink: 1 !important;
        flex-basis: auto !important;
        min-width: 0 !important;
    }

    /* Empujar y dar tamaño específico al botón de registrar */
    .stButton {
        text-align: right !important;
        width: 100% !important;
    }

    /* Corrección de márgenes internos de Streamlit que empujan el texto */
    [data-testid="stMarkdownContainer"] p {
        margin-bottom: 0px !important;
    }

    /* Estilo del botón "Registrar" compacto y visible */
    .stButton>button {
        width: 90px !important; /* Ancho fijo y seguro para el botón en móviles */
        border-radius: 12px;
        border: 1px solid #CBD5E1;
        background-color: #F8FAFC;
        font-weight: 600;
        font-size: 13px !important;
        color: #475569;
        padding: 0.4rem 0.2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #334155; margin-bottom: 2rem; font-size: 26px;'>Registro de Pañales 👶</h2>", unsafe_allow_html=True)

# 2. Conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def guardar_registro(tipo):
    tipo_limpio = "Pipi" if tipo == "Pipí" else tipo
    
    # Forzar explícitamente la zona horaria de España
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

# 3. Interfaz Vertical (Cada opción es una fila horizontal ancha)

# Fila 1: Pipí
col_img1, col_txt1, col_btn1 = st.columns([1, 2, 1.5])
with col_img1:
    st.image("pipiapp.png", width=55)
with col_txt1:
    st.markdown('<div style="padding-top: 12px;"><span style="font-weight:600; font-size:18px; color:#334155;">Pipí</span></div>', unsafe_allow_html=True)
with col_btn1:
    if st.button("Registrar", key="btn_pipi"):
        guardar_registro("Pipí")

# Fila 2: Caca
col_img2, col_txt2, col_btn2 = st.columns([1, 2, 1.5])
with col_img2:
    st.image("cacaapp.png", width=55)
with col_txt2:
    st.markdown('<div style="padding-top: 12px;"><span style="font-weight:600; font-size:18px; color:#334155;">Caca</span></div>', unsafe_allow_html=True)
with col_btn2:
    if st.button("Registrar", key="btn_caca"):
        guardar_registro("Caca")

# Fila 3: Ambos
col_img3, col_txt3, col_btn3 = st.columns([1, 2, 1.5])
with col_img3:
    st.image("ambosapp.png", width=55)
with col_txt3:
    st.markdown('<div style="padding-top: 12px;"><span style="font-weight:600; font-size:18px; color:#334155;">Ambos</span></div>', unsafe_allow_html=True)
with col_btn3:
    if st.button("Registrar", key="btn_ambos"):
        guardar_registro("Ambos")
