import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import urllib.parse

# Configuración de la página
st.set_page_config(page_title="Gestor de Cobros", page_icon="🔔")

# Estilo
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://media.giphy.com/media/ojPd9AOyqYC35fA2tT/giphy.gif");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    .stApp {
        background-color: rgba(0, 0, 0, 0.7);
        color: white;
    }

    h1, h2, h3, p, div {
        color: white !important;
    }

    [data-testid="stVerticalBlock"] {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #00f;
    }

    .stLinkButton > a {
        background-color: #25D366 !important;
        color: white !important;
        border-radius: 20px !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔔 Gestor de Cobros ⚡")

# Reproductor de audio
components.html("""
    <audio id="goku">
        <source src="https://files.catbox.moe/hyvwln.mp3" type="audio/mpeg">
    </audio>
    <div style="margin: 10px 0;">
        <button onclick="document.getElementById('goku').play()"
                style="padding:10px; cursor:pointer; background-color:#000;
                       color:#fff; border:1px solid #00f; border-radius:5px;">
            ❄️ Activar Aura
        </button>
        <button onclick="document.getElementById('goku').pause()"
                style="padding:10px; cursor:pointer; background-color:#000;
                       color:#fff; border:1px solid #00f; border-radius:5px;">
            🌑 Silencio
        </button>
    </div>
""", height=80)

# Fecha actual automática
hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

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

# Mostrar clientes
for c in clientes:
    dias = (c["vencimiento"] - hoy).days
    fecha_str = c["vencimiento"].strftime("%d/%m/%Y")

    with st.container():
        if dias < 0:
            st.markdown(f"### ❌ {c['nombre']} - ¡VENCIDO!")
        elif dias == 0:
            st.markdown(f"### 🚨 {c['nombre']} - ¡VENCE HOY!")
        elif dias <= 3:
            st.markdown(f"### ⚠️ {c['nombre']} - ¡VENCE EN {dias} DÍAS!")
        elif dias <= 7:
            st.markdown(f"### 🔔 {c['nombre']} - Vence en {dias} días")
        else:
            st.markdown(f"### ✅ {c['nombre']} - Vence en {dias} días")

        st.write(f"📅 Fecha: {fecha_str}")

        mensaje = (
            f"🔔 ¡RECORDATORIO IMPORTANTE!\n\n"
            f"Hola 👋 Te avisamos que tu cuenta {c['nombre']} está próxima a vencer.\n\n"
            f"📅 Fecha de vencimiento: {fecha_str}\n"
            f"⏳ Días restantes: {dias} días\n\n"
            f"⚡ Para evitar que tu servicio se interrumpa, podés renovarlo antes de la fecha de vencimiento.\n\n"
            f"📲 ¿Querés renovar? Escribinos y te ayudamos con la renovación.\n\n"
            f"🙏 ¡Gracias por seguir confiando en nuestro servicio!"
        )

        link = (
            f"https://wa.me/{c['telefono']}"
            f"?text={urllib.parse.quote(mensaje)}"
        )

        st.link_button("📲 Enviar WhatsApp", link)
