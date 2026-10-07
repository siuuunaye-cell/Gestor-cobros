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
# Lista de clientes real
clientes = [
    {"nombre": "Ema123", "telefono": "5491165217937", "vencimiento": hoy + timedelta(days=26)},
    {"nombre": "Julieta123", "telefono": "5491123026960", "vencimiento": hoy + timedelta(days=26)},
    {"nombre": "Omar12345", "telefono": "5491137703801", "vencimiento": hoy + timedelta(days=25)},
    {"nombre": "Maria123", "telefono": "5491151190334", "vencimiento": hoy + timedelta(days=21)},
    {"nombre": "Flor12345", "telefono": "5491158521706", "vencimiento": hoy + timedelta(days=3)},
    {"nombre": "Diego1234", "telefono": "5491150577319", "vencimiento": hoy + timedelta(days=30)},
    {"nombre": "Tere12345", "telefono": "5491162663854", "vencimiento": hoy + timedelta(days=13)},
    {"nombre": "Maximo12345", "telefono": "5491133821056", "vencimiento": hoy + timedelta(days=12)},
    {"nombre": "mely12345", "telefono": "5491130740231", "vencimiento": hoy + timedelta(days=15)},
    {"nombre": "Pupi12345", "telefono": "5491140912511", "vencimiento": hoy + timedelta(days=14)},
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
    fecha_str = c['vencimiento'].strftime("%d/%m/%Y")
    st.write(f"**{c['nombre']}** - Vence en {dias} días")
    
    # El mensaje completo que querías
    mensaje = (
        f"🔔 ¡RECORDATORIO IMPORTANTE!%0A%0A"
        f"Hola 👋 Te avisamos que tu cuenta {c['nombre']} está próxima a vencer.%0A%0A"
        f"📅 Fecha de vencimiento: {fecha_str}%0A"
        f"⏳ Días restantes: {dias} días%0A%0A"
        f"⚡ Para evitar que tu servicio se interrumpa, podés renovarlo antes de la fecha de vencimiento.%0A%0A"
        f"📲 ¿Querés renovar? Escribinos y te ayudamos con la renovación.%0A%0A"
        f"🙏 ¡Gracias por seguir confiando en nuestro servicio!"
    )
    
    link = f"https://wa.me/{c['telefono']}?text={mensaje}"
    st.link_button("Enviar WhatsApp", link)