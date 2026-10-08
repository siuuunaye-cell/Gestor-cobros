import streamlit as st
from datetime import datetime

# Configuración
st.set_page_config(page_title="Gestor de Cobros Goku", page_icon="🔔")

# Estilo: El GIF de Goku de fondo + Botones con llamas azules
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { 
    background-image: url("https://media.giphy.com/media/ojPd9AOyqYC35fA2tT/giphy.gif"); 
    background-size: cover; 
    background-position: center; 
    background-repeat: no-repeat;
}
.stApp { background-color: rgba(0, 0, 0, 0.6); color: white; }
.header-box { background: rgba(0, 50, 100, 0.5); padding: 20px; border-radius: 15px; border: 2px solid #00d4ff; text-align: center; }
div.stButton > button {
    width: 100%; height: 60px; border: none; border-radius: 10px; color: white; font-weight: bold;
    background: linear-gradient(45deg, #000428, #004e92, #000428);
    background-size: 200% 200%; animation: fuegoAzul 3s ease infinite; border: 1px solid #00d4ff;
}
@keyframes fuegoAzul { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
h1, p { color: white !important; }
.alerta { color: #ff4b4b !important; font-weight: bold; font-size: 1.2em; }
</style>
""", unsafe_allow_html=True)

# --- PARTE SUPERIOR ---
st.markdown("<div class='header-box'><h1>🔔 GESTOR DE COBROS - MODO GOKU</h1><p>¡Supera tus límites y mantén tus cobros al día!</p></div>", unsafe_allow_html=True)

hoy = datetime.now()

if 'clientes' not in st.session_state:
    st.session_state.clientes = [
        {"nombre": "Ema123", "telefono": "5491165217937", "vencimiento": datetime(2026, 11, 2)},
        {"nombre": "Julieta123", "telefono": "5491123026960", "vencimiento": datetime(2026, 11, 2)},
        {"nombre": "Omar12345", "telefono": "5491137703801", "vencimiento": datetime(2026, 11, 1)},
        {"nombre": "Maria123", "telefono": "5491151190334", "vencimiento": datetime(2026, 10, 28)},
        {"nombre": "Flor12345", "telefono": "5491158521706", "vencimiento": datetime(2026, 10, 10)},
        {"nombre": "Diego1234", "telefono": "5491150577319", "vencimiento": datetime(2026, 11, 6)},
        {"nombre": "Tere12345", "telefono": "5491162663854", "vencimiento": datetime(2026, 10, 20)},
        {"nombre": "Maximo12345", "telefono": "5491133821056", "vencimiento": datetime(2026, 10, 19)},
        {"nombre": "mely12345", "telefono": "5491130740231", "vencimiento": datetime(2026, 10, 22)},
        {"nombre": "Pupi12345", "telefono": "5491140912511", "vencimiento": datetime(2026, 10, 21)},
    ]

# Formulario
with st.expander("➕ Agregar nuevo cliente"):
    with st.form("nuevo_cliente"):
        nombre = st.text_input("Nombre")
        telefono = st.text_input("Teléfono")
        fecha_venc = st.date_input("Fecha de vencimiento")
        if st.form_submit_button("Guardar"):
            st.session_state.clientes.append({"nombre": nombre, "telefono": telefono, "vencimiento": datetime.combine(fecha_venc, datetime.min.time())})
            st.rerun()

# Alertas
st.subheader("⚠️ Alertas de Urgencia")
st.session_state.clientes.sort(key=lambda x: x['vencimiento'])
hay_alertas = False
for c in st.session_state.clientes:
    dias = (c['vencimiento'] - hoy).days
    if dias <= 3:
        hay_alertas = True
        estado = "¡VENCIDO!" if dias < 0 else f"vence en {dias} días"
        st.markdown(f"<p class='alerta'>🚨 {c['nombre']} - {estado}</p>", unsafe_allow_html=True)
if not hay_alertas: st.write("✅ Todo al día.")
st.divider()

# --- REPRODUCTOR DE AUDIO DE GOKU (INTACTO) ---
st.components.html("""
<audio id="goku">
<source src="https://files.catbox.moe/hyvwln.mp3" type="audio/mpeg">
</audio>
<div style="margin: 10px 0;">
<button onclick="document.getElementById('goku').play()" style="padding:10px; cursor:pointer; background-color: #000; color: #fff; border: 1px solid #00f;">❄️ Activar Aura</button>
<button onclick="document.getElementById('goku').pause()" style="padding:10px; cursor:pointer; background-color: #000; color: #fff; border: 1px solid #00f;">🔘 Silencio</button>
</div>
""", height=100)

# Lista
for i, c in enumerate(st.session_state.clientes):
    dias = (c['vencimiento'] - hoy).days
    fecha_str = c['vencimiento'].strftime("%d/%m/%Y")
    st.write(f"**{c['nombre']}** - Vence en {dias} días")
    nueva_fecha = st.date_input("Cambiar fecha:", value=c['vencimiento'], key=f"cal_{i}")
    if nueva_fecha != c['vencimiento'].date():
        st.session_state.clientes[i]['vencimiento'] = datetime.combine(nueva_fecha, datetime.min.time())
        st.rerun()
    
    mensaje = (f"🔔 ¡RECORDATORIO IMPORTANTE!%0A%0AHola 👋 Te avisamos que tu cuenta {c['nombre']} está próxima a vencer.%0A%0A"
               f"📅 Fecha de vencimiento: {fecha_str}%0A⏳ Días restantes: {dias} días%0A%0A"
               f"⚡ Para evitar que tu servicio se interrumpa, podés renovarlo antes de la fecha de vencimiento.%0A%0A"
               f"📲 ¿Querés renovar? Escribinos y te ayudamos con la renovación.%0A%0A🙏 ¡Gracias por seguir confiando en nuestro servicio!")
    st.link_button("Enviar WhatsApp", f"https://wa.me/{c['telefono']}?text={mensaje}")