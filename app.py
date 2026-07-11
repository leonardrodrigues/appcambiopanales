import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from streamlit_gsheets import GSheetsConnection

# 1. Configuración de página móvil
st.set_page_config(page_title="Baby Log", layout="centered")

# Estilos CSS avanzados para transformar los botones en imágenes
st.markdown("""
    <style>
    /* Ocultar elementos nativos innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Optimizar los márgenes en pantallas de teléfono */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 480px !important;
    }

    /* FILA CONTENEDORA (Forzar siempre horizontal en móvil) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important; 
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 24px;
        padding: 0.8rem 1.2rem !important;
        margin-bottom: 0.8rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
    }

    /* Columna de la Imagen/Botón (Ancho fijo) */
    [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(1) {
        flex: 0 0 65px !important;
        min-width: 65px !important;
    }
    
    /* Columna del Texto (Ocupa el resto de la pantalla) */
    [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(2) {
        flex: 1 1 auto !important;
        padding-left: 0.5rem !important;
    }

    /* TRANSFORMAR EL BOTÓN EN IMAGEN */
    .stButton>button {
        width: 55px !important;
        height: 55px !important;
        padding: 0px !important;
        border-radius: 16px !important;
        border: none !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        color: transparent !important; /* Oculta el texto nativo del botón */
        font-size: 0px !important;
        cursor: pointer;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.1s ease-in-out;
    }
    
    .stButton>button:active {
        transform: scale(0.95); /* Efecto táctil al pulsar */
    }

    /* Asignar cada imagen de fondo correspondiente a su botón */
    div.stButton button[key*="btn_pipi"] {
        background-image: url("app/pipiapp.png") !important;
    }
    div.stButton button[key*="btn_caca"] {
        background-image: url("app/cacaapp.png") !important;
    }
    div.stButton button[key*="btn_ambos"] {
        background-image: url("app/ambosapp.png") !important;
    }

    /* Corrección de márgenes del texto */
    [data-testid="stMarkdownContainer"] p {
        margin-bottom: 0px !important;
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

# 3. Interfaz de Dos Columnas (El botón ES la imagen)

# Fila 1: Pipí
col_btn1, col_txt1 = st.columns([1, 4])
with col_btn1:
    # El texto "Pipí" dentro del botón no se verá, se reemplaza por la imagen en el CSS
    st.button("Pipí", key="btn_pipi") 
with col_txt1:
    st.markdown('<div style="display:flex; flex-direction:column;"><span style="font-weight:700; font-size:18px; color:#334155;">Pipí</span><span style="font-size:12px; color:#64748B;">Registrar pañal mojado</span></div>', unsafe_allow_html=True)

# Fila 2: Caca
col_btn2, col_txt2 = st.columns([1, 4])
with col_btn2:
    st.button("Caca", key="btn_caca")
with col_txt2:
    st.markdown('<div style="display:flex; flex-direction:column;"><span style="font-weight:700; font-size:18px; color:#334155;">Caca</span><span style="font-size:12px; color:#64748B;">Registrar deposición</span></div>', unsafe_allow_html=True)

# Fila 3: Ambos
col_btn3, col_txt3 = st.columns([1, 4])
with col_btn3:
    st.button("Ambos", key="btn_ambos")
with col_txt3:
    st.markdown('<div style="display:flex; flex-direction:column;"><span style="font-weight:700; font-size:18px; color:#334155;">Ambos</span><span style="font-size:12px; color:#64748B;">Registrar pipí y caca</span></div>', unsafe_allow_html=True)
