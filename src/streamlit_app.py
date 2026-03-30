# Cargar librerias

import pickle
import pandas as pd
import streamlit as st
from pathlib import Path

#Setteo el inicio

st.set_page_config(page_title="Videogame Top Seller Predictor", page_icon="🎮", layout="centered")

#Configuro el path que uso

MODEL_PATH = Path("src/model.pkl")

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        st.error("No encuentro el archivo model.pkl en la raíz del proyecto.")
        st.stop()
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

model = load_model()

#Diseno basico de la interfaz

st.title("🎮 Videogame Top Seller Predictor")
st.caption("Predice si un juego será Top Seller según plataforma, publisher y año.")

#Parte del modelo predictivo

with st.form("predict_form"):
    platforms = st.text_input("Platform(s)", placeholder="Ej: PC, PS4, Switch…")
    publishers = st.text_input("Publisher(s)", placeholder="Ej: Nintendo, Ubisoft…")
    releaseyear = st.number_input("Release year", min_value=1970, max_value=2035, value=2015, step=1)

    submitted = st.form_submit_button("Predecir")

if submitted:
    if not platforms.strip() or not publishers.strip():
        st.warning("Rellena platform(s) y publisher(s).")
        st.stop()

    input_data = pd.DataFrame([{
        "platforms": platforms,
        "publishers": publishers,
        "releaseyear": int(releaseyear)
    }])

    try:
        prediction = model.predict(input_data)[0]
    except Exception as e:
        st.error(f"Error al predecir. Revisa que el modelo espera exactamente estas columnas: {list(input_data.columns)}.\n\nDetalle: {e}")
        st.stop()

    if prediction == 1:
        st.success("Top Seller 🎮🔥")
    else:
        st.info("Not a Top Seller")