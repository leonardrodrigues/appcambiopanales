import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. Configuración de página móvil
st.set_page_config(page_title="Baby Log", layout="centered")

# Estilos CSS específicos para crear "Filas-Botón" masivas y táctiles
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 480px !important; /* Ancho ideal para simular app nativa */
    }

    /* Estructura de fila contenedora (Icono + Texto) */
    .row-container {
        display: flex;
        align-items: center;
        gap: 1.2rem;
        padding: 0.5rem 0;
    }

    /* Forzar que las columnas se alineen verticalmente de forma perfecta */
    [data-testid="stHorizontalBlock"] {
        align-items: center !important;
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 0.8rem 1.2rem !important;
        margin-bottom: 1rem !important;
        transition: all 0.2s ease-in-out;
    }
    
    [data-testid="stHorizontalBlock"]:hover {
        background-color: #F1F5F9;
        border-color: #CBD5E1;
    }

    /* Estilo del botón "Registrar" a la derecha */
    .stButton>button {
        width: 100% !important;
        border-radius: 12px;
        border: 1px solid #CBD5E1;
        background-color: #FFFFFF;
        font-weight: 600;
        color: #475569;
        padding: 0.6rem 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #334155; margin-bottom: 2rem; font-size: 26px;'>Registro de Pañales 👶</h2>", unsafe_allow_html=True)

# 2. Conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def guardar_registro(tipo):
    tipo_limpio = "Pipi" if tipo == "Pipí" else tipo
    ahora = datetime.now()
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
col_img1, col_btn1 = st.columns([2, 1])
with col_img1:
    st.markdown('<div class="row-container"><img src="app/pipiapp.png" style="width:55px;height:55px;"><span style="font-weight:600; font-size:18px; color:#334155;">Pipí</span></div>', unsafe_allow_html=True)
with col_btn1:
    if st.button("Registrar", key="btn_pipi"):
        guardar_registro("Pipí")

# Fila 2: Caca
col_img2, col_btn2 = st.columns([2, 1])
with col_img2:
    st.markdown('<div class="row-container"><img src="app/cacaapp.png" style="width:55px;height:55px;"><span style="font-weight:600; font-size:18px; color:#334155;">Caca</span></div>', unsafe_allow_html=True)
with col_btn2:
    if st.button("Registrar", key="btn_caca"):
        guardar_registro("Caca")

# Fila 3: Ambos
col_img3, col_btn3 = st.columns([2, 1])
with col_img3:
    st.markdown('<div class="row-container"><img src="app/ambosapp.png" style="width:55px;height:55px;"><span style="font-weight:600; font-size:18px; color:#334155;">Ambos</span></div>', unsafe_allow_html=True)
with col_btn3:
    if st.button("Registrar", key="btn_ambos"):
        guardar_registro("Ambos")
