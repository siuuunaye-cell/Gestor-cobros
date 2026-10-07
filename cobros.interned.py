import streamlit as st
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(page_title="Gestor de Cobros", page_icon="🔔")

# Estilo con el fondo de Goku integrado
st.markdown("""<style>[data-testid="stAppViewContainer"]{background-image: url("https://media.giphy.com/media/ojPd9AOyqYC35fA2tT/giphy.gif"); background-size: cover; background-position:center;background-repeat: no-repeat;}.stApp{background-color:rgba(0, 0, 0, 0.6); color:white;}.stButton>button{ width:100%;height:60px;background-color:#3366ff;color:white;border-radius: 10px;}h1,p{color:white !important; }<style>""",unsafe_allow_html=True)

st.title("🔔 Gestor de Cobros")
hoy = datetime(2026, 10, 7)

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

clientes_ordenados = sorted(clientes, key=lambda x: x['vencimiento'])

for c in clientes_ordenados:
    dias = (c["vencimiento"] - hoy).days
    fecha_str = c['vencimiento'].strftime("%d/%m/%Y")
    
    msg = f"🔔 ¡RECORDATORIO IMPORTANTE!%0A%0AHola 👋 Te avisamos que tu cuenta {c['nombre']} está próxima a vencer.%0A%0A📅 Fecha de vencimiento: {fecha_str}%0A⏳ Días restantes: {dias} días%0A%0A⚡ Para evitar que tu servicio se interrumpa, podés renovarlo antes de la fecha de vencimiento.%0A%0A📲 ¿Querés renovar? Escribinos y te ayudamos con la renovación.%0A%0A🙏 ¡Gracias por seguir confiando en nuestro servicio!"
    
    url = f"https://wa.me/{c['telefono']}?text={msg}"
    
    if st.button(f"{c['nombre']} - Vence en {dias} días"):
        st.link_button("Enviar WhatsApp", url)