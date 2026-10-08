import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import urllib.parse

# Configuración de la página
st.set_page_config(page_title="Gestor de Cobros", page_icon="🔔")

# Estilo
st.markdown("""
<style>
/* ===== AURA AZUL / FUEGO ===== */
[data-testid="stAppViewContainer"] {
    background-image:
        linear-gradient(rgba(0, 0, 20, 0.72), rgba(0, 0, 20, 0.82)),
        url("https://media.giphy.com/media/ojPd9AOyqYC35fA2tT/giphy.gif");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.stApp {
    background-color: transparent;
    color: white;
}

/* Letras con brillo azul */
h1, h2, h3 {
    color: #ffffff !important;
    text-shadow:
        0 0 5px #00bfff,
        0 0 12px #008cff,
        0 0 25px #0055ff;
    font-weight: 900 !important;
}

/* Texto general */
p, label, .stMarkdown, .stText, div {
    color: #f5fbff;
}

/* Título principal */
h1 {
    background: linear-gradient(90deg, #ffffff, #5ee7ff, #168cff, #ffffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 10px #008cff);
}

/* Contenedores */
[data-testid="stVerticalBlock"] {
    background: linear-gradient(
        145deg,
        rgba(0, 120, 255, 0.14),
        rgba(0, 0, 30, 0.55)
    );
    padding: 15px;
    border-radius: 18px;
    border: 1px solid rgba(0, 183, 255, 0.65);
    box-shadow:
        0 0 8px rgba(0, 153, 255, 0.45),
        inset 0 0 18px rgba(0, 80, 255, 0.08);
}

/* Botones */
.stButton > button,
.stLinkButton > a,
button[kind="secondary"],
button[kind="primary"] {
    background: linear-gradient(135deg, #001b44, #006eff, #00cfff) !important;
    color: white !important;
    border: 1px solid #62eaff !important;
    border-radius: 14px !important;
    font-weight: 900 !important;
    text-shadow: 0 0 6px #001eff;
    box-shadow:
        0 0 6px #00aaff,
        0 0 16px rgba(0, 119, 255, 0.65),
        inset 0 0 8px rgba(255,255,255,0.15);
    transition: all 0.2s ease-in-out;
}

/* Efecto al pasar el dedo/mouse */
.stButton > button:hover,
.stLinkButton > a:hover {
    transform: translateY(-2px) scale(1.02);
    border-color: #ffffff !important;
    box-shadow:
        0 0 10px #00d9ff,
        0 0 28px #006eff,
        0 0 45px rgba(0, 128, 255, 0.7);
}

/* Campos */
.stTextInput input,
.stNumberInput input,
.stDateInput input {
    background: rgba(0, 10, 35, 0.85) !important;
    color: white !important;
    border: 1px solid #008cff !important;
    border-radius: 10px !important;
    box-shadow: 0 0 8px rgba(0, 140, 255, 0.35);
}

/* Expanders */
[data-testid="stExpander"] {
    border: 1px solid rgba(0, 183, 255, 0.6) !important;
    border-radius: 15px !important;
    box-shadow: 0 0 12px rgba(0, 119, 255, 0.25);
}

/* Separadores */
hr {
    border-color: rgba(0, 183, 255, 0.55) !important;
    box-shadow: 0 0 8px #008cff;
}

/* Mensajes */
.stAlert {
    border-radius: 12px !important;
    box-shadow: 0 0 12px rgba(0, 153, 255, 0.35);
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

# =========================
# GESTIÓN DE CLIENTES
# =========================
import json
from pathlib import Path

hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
ARCHIVO_CLIENTES = Path("clientes.json")

# Clientes iniciales del archivo original.
CLIENTES_INICIALES = [
    {"nombre": "Ema123", "telefono": "5491165217937", "vencimiento": (hoy + timedelta(days=26)).strftime("%Y-%m-%d")},
    {"nombre": "Julieta123", "telefono": "5491123026960", "vencimiento": (hoy + timedelta(days=26)).strftime("%Y-%m-%d")},
    {"nombre": "Omar12345", "telefono": "5491137703801", "vencimiento": (hoy + timedelta(days=25)).strftime("%Y-%m-%d")},
    {"nombre": "Maria123", "telefono": "5491151190334", "vencimiento": (hoy + timedelta(days=21)).strftime("%Y-%m-%d")},
    {"nombre": "Flor12345", "telefono": "5491158521706", "vencimiento": (hoy + timedelta(days=3)).strftime("%Y-%m-%d")},
    {"nombre": "Diego1234", "telefono": "5491150577319", "vencimiento": (hoy + timedelta(days=30)).strftime("%Y-%m-%d")},
    {"nombre": "Tere12345", "telefono": "5491162663854", "vencimiento": (hoy + timedelta(days=13)).strftime("%Y-%m-%d")},
    {"nombre": "Maximo12345", "telefono": "5491133821056", "vencimiento": (hoy + timedelta(days=12)).strftime("%Y-%m-%d")},
    {"nombre": "mely12345", "telefono": "5491130740231", "vencimiento": (hoy + timedelta(days=15)).strftime("%Y-%m-%d")},
    {"nombre": "Pupi12345", "telefono": "5491140912511", "vencimiento": (hoy + timedelta(days=14)).strftime("%Y-%m-%d")},
]

def guardar_clientes(clientes):
    with ARCHIVO_CLIENTES.open("w", encoding="utf-8") as f:
        json.dump(clientes, f, ensure_ascii=False, indent=2)

def cargar_clientes():
    if not ARCHIVO_CLIENTES.exists():
        guardar_clientes(CLIENTES_INICIALES)
        return CLIENTES_INICIALES.copy()

    try:
        with ARCHIVO_CLIENTES.open("r", encoding="utf-8") as f:
            datos = json.load(f)

        if not isinstance(datos, list):
            raise ValueError("Formato inválido")

        return datos
    except Exception:
        guardar_clientes(CLIENTES_INICIALES)
        return CLIENTES_INICIALES.copy()

clientes = cargar_clientes()

# -------------------------
# NUEVOS USUARIOS
# -------------------------
with st.expander("➕ Nuevos usuarios", expanded=False):
    st.subheader("Agregar nuevo cliente")

    with st.form("form_nuevo_cliente", clear_on_submit=True):
        nombre_nuevo = st.text_input("👤 Nombre / usuario")
        telefono_nuevo = st.text_input("📱 Teléfono (con código de país)")
        fecha_nueva = st.date_input("📅 Fecha de vencimiento", value=hoy.date())
        dias_nuevo = st.number_input(
            "O agregar días desde hoy",
            min_value=0,
            value=30,
            step=1
        )

        agregar = st.form_submit_button("💾 Agregar cliente")

        if agregar:
            nombre_nuevo = nombre_nuevo.strip()
            telefono_nuevo = telefono_nuevo.strip()

            if not nombre_nuevo:
                st.error("⚠️ Escribí el nombre o usuario.")
            elif any(c["nombre"].lower() == nombre_nuevo.lower() for c in clientes):
                st.error("⚠️ Ya existe un cliente con ese nombre.")
            else:
                nuevo = {
                    "nombre": nombre_nuevo,
                    "telefono": telefono_nuevo,
                    "vencimiento": (
                        hoy + timedelta(days=int(dias_nuevo))
                    ).strftime("%Y-%m-%d")
                }

                # Si el usuario cambió manualmente la fecha, usamos esa fecha.
                if fecha_nueva != hoy.date():
                    nuevo["vencimiento"] = fecha_nueva.strftime("%Y-%m-%d")

                clientes.append(nuevo)
                guardar_clientes(clientes)
                st.success(f"✅ {nombre_nuevo} agregado correctamente.")
                st.rerun()

# -------------------------
# CLIENTES
# -------------------------
st.subheader("👥 Todos los clientes")

if not clientes:
    st.info("Todavía no hay clientes cargados.")

# Mostrar clientes
for i, c in enumerate(clientes):
    try:
        vencimiento = datetime.strptime(c["vencimiento"], "%Y-%m-%d")
    except (KeyError, ValueError):
        vencimiento = hoy

    dias = (vencimiento - hoy).days
    fecha_str = vencimiento.strftime("%d/%m/%Y")

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

        st.write(f"📱 Teléfono: {c.get('telefono', '')}")
        st.write(f"📅 Fecha de vencimiento: {fecha_str}")

        # Editar fecha directamente.
        with st.expander("⚙️ Editar cliente"):
            nueva_fecha = st.date_input(
                "Nueva fecha de vencimiento",
                value=vencimiento.date(),
                key=f"fecha_{i}"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("💾 Guardar fecha", key=f"guardar_{i}"):
                    clientes[i]["vencimiento"] = nueva_fecha.strftime("%Y-%m-%d")
                    guardar_clientes(clientes)
                    st.success("✅ Fecha actualizada.")
                    st.rerun()

            with col2:
                if st.button("🗑️ Eliminar", key=f"eliminar_{i}"):
                    clientes.pop(i)
                    guardar_clientes(clientes)
                    st.success("Cliente eliminado.")
                    st.rerun()

        # Renovación rápida.
        st.markdown("**🔄 Renovar servicio**")
        col1, col2, col3 = st.columns(3)

        with col1:
            dias_renovar = st.number_input(
                "Días",
                min_value=1,
                value=30,
                step=1,
                key=f"renovar_dias_{i}"
            )

        with col2:
            if st.button("➕ Sumar días", key=f"sumar_{i}"):
                clientes[i]["vencimiento"] = (
                    vencimiento + timedelta(days=int(dias_renovar))
                ).strftime("%Y-%m-%d")
                guardar_clientes(clientes)
                st.success(
                    f"✅ Se agregaron {int(dias_renovar)} días a {c['nombre']}."
                )
                st.rerun()

        with col3:
            if st.button("🔄 Renovar desde hoy", key=f"renovar_hoy_{i}"):
                clientes[i]["vencimiento"] = (
                    hoy + timedelta(days=int(dias_renovar))
                ).strftime("%Y-%m-%d")
                guardar_clientes(clientes)
                st.success(
                    f"✅ {c['nombre']} renovado por {int(dias_renovar)} días."
                )
                st.rerun()

        mensaje = (
            f"🔔 ¡RECORDATORIO IMPORTANTE!\n\n"
            f"Hola 👋 Te avisamos que tu cuenta {c['nombre']} está próxima a vencer.\n\n"
            f"📅 Fecha de vencimiento: {fecha_str}\n"
            f"⏳ Días restantes: {dias} días\n\n"
            f"⚡ Para evitar que tu servicio se interrumpa, podés renovarlo antes de la fecha de vencimiento.\n\n"
            f"📲 ¿Querés renovar? Escribinos y te ayudamos con la renovación.\n\n"
            f"🙏 ¡Gracias por seguir confiando en nuestro servicio!"
        )

        telefono = c.get("telefono", "").strip()
        if telefono:
            link = (
                f"https://wa.me/{telefono}"
                f"?text={urllib.parse.quote(mensaje)}"
            )
            st.link_button("📲 Enviar WhatsApp", link)
        else:
            st.warning("⚠️ Este cliente no tiene teléfono cargado.")

        st.divider()
