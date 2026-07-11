import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from streamlit_gsheets import GSheetsConnection

# 1. Configuración de página móvil
st.set_page_config(page_title="Baby Log", layout="centered")

# Estilos CSS básicos (Solo para ocultar menús y dar forma a las tarjetas)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        max-width: 450px !important;
    }
    
    /* Contenedor tipo tarjeta blanca para cada opción */
    .card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        text-align: center;
    }
    
    /* Espaciado del texto del título del pañal */
    .card-title {
        font-weight: 700;
        font-size: 18px;
        color: #334155;
        margin-top: 0.5rem;
        margin-bottom: 0.8rem;
        display: block;
    }

    /* Botón Registrar adaptado al ancho de la tarjeta */
    .stButton>button {
        width: 100% !important;
        border-radius: 12px !important;
        border: 1px solid #CBD5E1 !important;
        background-color: #F8FAFC !important;
        font-weight: 600 !important;
        color: #475569 !important;
        padding: 0.5rem 1rem !important;
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

# 3. Interfaz Vertical Nativa Segura (Sin columnas que se desborden)

# Tarjeta 1: Pipí
st.markdown('<div class="card">', unsafe_allow_html=True)
st.image("pipiapp.png", width=60)
st.markdown('<span class="card-title">Pipí</span>', unsafe_allow_html=True)
st.button("Registrar Pipí", key="btn_pipi", on_click=guardar_registro, args=("Pipí",))
st.markdown('</div>', unsafe_allow_html=True)

# Tarjeta 2: Caca
st.markdown('<div class="card">', unsafe_allow_html=True)
st.image("cacaapp.png", width=60)
st.markdown('<span class="card-title">Caca</span>', unsafe_allow_html=True)
st.button("Registrar Caca", key="btn_caca", on_click=guardar_registro, args=("Caca",))
st.markdown('</div>', unsafe_allow_html=True)

# Tarjeta 3: Ambos
st.markdown('<div class="card">', unsafe_allow_html=True)
st.image("ambosapp.png", width=60)
st.markdown('<span class="card-title">Ambos</span>', unsafe_allow_html=True)
st.button("Registrar Ambos", key="btn_ambos", on_click=guardar_registro, args=("Ambos",))
st.markdown('</div>', unsafe_allow_html=True)
