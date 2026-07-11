import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from streamlit_gsheets import GSheetsConnection
import base64
import os

# 1. Configuración de página móvil
st.set_page_config(page_title="Baby Log", layout="centered")

# Cargar imágenes en Base64 para inyección directa en CSS (garantiza compatibilidad móvil)
@st.cache_data
def get_base64_image(img_path):
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_pipi_b64 = get_base64_image("pipiapp.png")
img_caca_b64 = get_base64_image("cacaapp.png")
img_ambos_b64 = get_base64_image("ambosapp.png")

# Estilos CSS avanzados para transformar los botones en imágenes
st.markdown(f"""
    <style>
    /* Ocultar elementos nativos innecesarios */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Fondo agradable para la aplicación */
    .stApp {{
        background-color: #F8FAFC !important;
    }}
    
    /* Optimizar los márgenes en pantallas de teléfono */
    .block-container {{
        padding-top: 3rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 450px !important;
    }}

    /* CONTENEDOR DE ICONOS (Visualización de Widget iOS) */
    [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 28px;
        padding: 1.8rem 1rem !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
        margin-top: 1rem !important;
        width: 100% !important;
    }}

    /* Forzar que las columnas pesen exactamente lo mismo y no se deformen */
    [data-testid="stHorizontalBlock"] [data-testid="column"] {{
        flex: 1 1 0% !important;
        min-width: 0 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }}

    /* TRANSFORMAR EL BOTÓN EN IMAGEN */
    .stButton>button {{
        width: 85px !important;
        height: 85px !important;
        padding: 0px !important;
        border-radius: 22px !important;
        border: 1px solid #E2E8F0 !important;
        background-color: #F1F5F9 !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        color: transparent !important; /* Oculta el texto nativo del botón */
        font-size: 0px !important;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
        transition: all 0.2s ease-in-out;
        display: block !important;
        margin: 0 auto !important;
    }}
    
    .stButton>button:active {{
        transform: scale(0.92); /* Efecto táctil de pulsación */
    }}

    /* ASIGNACIÓN FIJA POR COLUMNAS (Soluciona el problema de las imágenes transparentes) */
    [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(1) button {{
        background-image: url("data:image/png;base64,{img_pipi_b64}") !important;
    }}
    [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(2) button {{
        background-image: url("data:image/png;base64,{img_caca_b64}") !important;
    }}
    [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(3) button {{
        background-image: url("data:image/png;base64,{img_ambos_b64}") !important;
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #334155; margin-bottom: 1.5rem; font-size: 26px;'>Registro de Pañales 👶</h2>", unsafe_allow_html=True)

# 2. Conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def guardar_registro(tipo):
    tipo_limpio = "Pipi" if tipo == "Pipí" else tipo
    zona_madrid = ZoneInfo("Europe/Madrid")
    ahora = datetime.now(zona_madrid)
    
    fecha = coder = ahora.strftime("%Y-%m-%d")
    hora = ahora.strftime("%H:%M:%S")
    
    try:
        df_existente = conn.read(ttl=0)
        nueva_fila = pd.DataFrame([[fecha, hora, tipo_limpio]], columns=["Fecha", "Hora", "Tipo"])
        df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
        conn.update(data=df_actualizado)
        st.toast(f"💾 Guardado: {tipo_limpio} ({hora})", icon="👶")
    except Exception as e:
        st.error(f"Error: {e}")

# 3. Interfaz Simplificada de 3 Iconos Horizontales
col1, col2, col3 = st.columns(3)

with col1:
    st.button("Pipí", key="btn_pipi", on_click=guardar_registro, args=("Pipí",))

with col2:
    st.button("Caca", key="btn_caca", on_click=guardar_registro, args=("Caca",))

with col3:
    st.button("Ambos", key="btn_ambos", on_click=guardar_registro, args=("Ambos",))
