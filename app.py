import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Configuración de página móvil
st.set_page_config(page_title="Baby Log", layout="centered")

# Estilos personalizados para vista móvil limpia e interactiva
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton>button {
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        background-color: #F8FAFC;
        font-weight: 600;
        color: #475569;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #F1F5F9;
        border-color: #CBD5E1;
        transform: scale(1.03);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #334155; margin-bottom: 1.5rem;'>Registro de Pañales 👶</h2>", unsafe_allow_html=True)

# 2. Función para escribir en CSV
def guardar_registro(tipo):
    # Eliminar acento para evitar caracteres extraños en entornos con diferente codificación
    tipo_limpio = "Pipi" if tipo == "Pipí" else tipo
    
    ahora = datetime.now()
    fecha = ahora.strftime("%Y-%m-%d")
    hora = ahora.strftime("%H:%M:%S")
    
    df = pd.DataFrame([[fecha, hora, tipo_limpio]], columns=["Fecha", "Hora", "Tipo"])
    df.to_csv("registro_panales.csv", mode='a', header=not os.path.exists("registro_panales.csv"), index=False)
    st.toast(f"💾 Guardado: {tipo_limpio} a las {hora}", icon="👶")

# 3. Grid de botones para el teléfono
col1, col2, col3 = st.columns(3)

with col1:
    st.image("pipiapp.png", use_container_width=True)
    if st.button("Pipí", use_container_width=True, key="btn_pipi"):
        guardar_registro("Pipí")

with col2:
    st.image("cacaapp.png", use_container_width=True)
    if st.button("Caca", use_container_width=True, key="btn_caca"):
        guardar_registro("Caca")

with col3:
    st.image("ambosapp.png", use_container_width=True)
    if st.button("Ambos", use_container_width=True, key="btn_ambos"):
        guardar_registro("Ambos")
