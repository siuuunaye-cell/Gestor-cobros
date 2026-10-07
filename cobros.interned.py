import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(page_title="Gestor de Cobros", page_icon="🔔")
# Estilo con la animación de Goku
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://media.giphy.com/media/ojPd9AOyqYC35fA2tT/giphy.gif");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
.stApp {
    background-color: rgba(0, 0, 0, 0.6);
    color: white;
}
.stButton>button {
    width: 100%;
    height: 60px;
    background-color: #3366ff;
    color: white;
    border-radius: 10px;
}
h1, p {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🔔 Gestor de Cobros")
hoy = datetime(2026, 10, 7)

# Lista completa de clientes
clientes = [
    {"nombre": "Ema123", "telefono": "5491165217937", "vencimiento": hoy + timedelta(days=26)},
    {"nombre": "Julieta123", "telefono": "5491123026960", "vencimiento": hoy + timedelta(days=26)},
    {"nombre": "Omar12345", "telefono": "5491137703801", "vencimiento": hoy + timedelta(days=26)},
    {"nombre": "Nahiara", "telefono": "5491130635489", "vencimiento": hoy + timedelta(days=15)},
    {"nombre": "Valen", "telefono": "5491161683416", "vencimiento": hoy + timedelta(days=10)},
    {"nombre": "Meli", "telefono": "5491122849501", "vencimiento": hoy + timedelta(days=5)},
    {"nombre": "Santi", "telefono": "5491155667788", "vencimiento": hoy + timedelta(days=20)},
    {"nombre": "Agus", "telefono": "5491144332211", "vencimiento": hoy + timedelta(days=12)},
    {"nombre": "Tomi", "telefono": "5491199887766", "vencimiento": hoy + timedelta(days=8)},
    {"nombre": "Lu", "telefono": "5491111223344", "vencimiento": hoy + timedelta(days=2)}
]

# Reproductor de audio
components.html("""
    <audio id="goku">
      <source src="https://files.catbox.moe/hyvwln.mp3" type="audio/mpeg">
    </audio>
    <div style="margin: 10px 0;">
        <button onclick="document.getElementById('goku').play()" style="padding:10px; cursor:pointer; background-color: #000; color: #fff; border: 1px solid #00f;">❄️ Activar Aura</button>
        <button onclick="document.getElementById('goku').pause()" style="padding:10px; cursor:pointer; background-color: #000; color: #fff; border: 1px solid #00f;">🌑 Silencio</button>
    </div>
    """, height=100)

# Lógica de clientes
for c in clientes:
    dias = (c['vencimiento'] - hoy).days
    msg = f"Hola {c['nombre']}, te escribo para recordarte que tu pago vence en {dias} días. ¡Saludos!"
    url = f"https://wa.me/{c['telefono']}?text={msg}"

    if st.button(f"{c['nombre']} - Vence en {dias} días"):
        st.link_button("Enviar WhatsApp", url)