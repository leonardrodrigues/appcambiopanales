import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from streamlit_gsheets import GSheetsConnection

# 1. Configuración de página móvil
st.set_page_config(page_title="Baby Log", layout="centered")

# Estilos CSS limpios, forzando colores fijos para evitar que el Modo Oscuro los altere
st.markdown("""
    <style>
    /* Ocultar elementos nativos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* BLINDAR COLORES: Forzar fondo claro general en toda la app */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #F8FAFC !important;
        color: #334155 !important;
    }
    
    /* Optimizar el contenedor principal del teléfono */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
        max-width: 400px !important;
    }
    
    /* Tarjeta blanca fija (No cambia con el modo oscuro) */
    .card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 24px !important;
        padding: 1.2rem !important;
        margin-bottom: 0.8rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02) !important;
        text-align: center !important;
    }
    
    /* Separación sutil debajo de la imagen */
    .card-image-container {
        margin-bottom: 0.8rem !important;
        display: flex;
        justify-content: center;
    }

    /* Estilo del botón Registrar fijo (Texto oscuro, fondo claro) */
    .stButton>button {
        width: 100% !important;
        border-radius: 14px !important;
        border: 1px solid #CBD5E1 !important;
        background-color: #F8FAFC !important;
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        padding: 0.5rem 1rem !important;
        transition: background-color 0.1s ease-in-out !important;
    }
    
    /* Comportamiento al pulsar el botón */
    .stButton>button:active, .stButton>button:focus {
        background-color: #E2E8F0 !important;
        color: #334155 !important;
        border-color: #94A3B8 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título de la aplicación con color gris oscuro forzado
st.markdown("<h2 style='text-align: center; color: #334155; margin-bottom: 1.8rem; font-size: 26px; font-weight: 700;'>Registro de Pañales 👶</h2>", unsafe_allow_html=True)

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

# 3. Interfaz Minimalista: Solo Imagen y Botón

# Tarjeta 1: Pipí
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-image-container">', unsafe_allow_html=True)
st.image("pipiapp.png", width=65)
st.markdown('</div>', unsafe_allow_html=True)
st.button("Registrar Pipí", key="btn_pipi", on_click=guardar_registro, args=("Pipí",))
st.markdown('</div>', unsafe_allow_html=True)

# Tarjeta 2: Caca
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-image-container">', unsafe_allow_html=True)
st.image("cacaapp.png", width=65)
st.markdown('</div>', unsafe_allow_html=True)
st.button("Registrar Caca", key="btn_caca", on_click=guardar_registro, args=("Caca",))
st.markdown('</div>', unsafe_allow_html=True)

# Tarjeta 3: Ambos
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-image-container">', unsafe_allow_html=True)
st.image("ambosapp.png", width=65)
st.markdown('</div>', unsafe_allow_html=True)
st.button("Registrar Ambos", key="btn_ambos", on_click=guardar_registro, args=("Ambos",))
st.markdown('</div>', unsafe_allow_html=True)
