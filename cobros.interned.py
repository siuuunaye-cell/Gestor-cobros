import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import urllib.parse
import sqlite3
import hashlib
import secrets
from pathlib import Path

# =========================
# CONFIGURACIÓN
# =========================
st.set_page_config(page_title="Gestor de Cobros", page_icon="⚡", layout="wide")

DB = Path("gestor_cobros.db")

# Credenciales iniciales del administrador.
# Cambialas desde el panel de administración una vez que ingreses.
DEFAULT_ADMIN_USER = "admin"
DEFAULT_ADMIN_PASSWORD = "erick2026"

# =========================
# BASE DE DATOS
# =========================
def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_db():
    conn = db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'revendedor',
        active INTEGER NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT DEFAULT '',
        vencimiento TEXT NOT NULL,
        reseller_id INTEGER,
        created_at TEXT NOT NULL,
        FOREIGN KEY(reseller_id) REFERENCES users(id)
    );
    """)
    admin = conn.execute(
        "SELECT id FROM users WHERE username=?",
        (DEFAULT_ADMIN_USER,)
    ).fetchone()
    if not admin:
        conn.execute(
            "INSERT INTO users(username,password_hash,role) VALUES(?,?,?)",
            (DEFAULT_ADMIN_USER, hash_password(DEFAULT_ADMIN_PASSWORD), "admin")
        )
    conn.commit()
    conn.close()

init_db()

# =========================
# RECUPERAR CLIENTES ORIGINALES
# =========================
CLIENTES_ORIGINALES = [
    ("Ema123", "5491165217937", 26),
    ("Julieta123", "5491123026960", 26),
    ("Omar12345", "5491137703801", 25),
    ("Maria123", "5491151190334", 21),
    ("Flor12345", "5491158521706", 3),
    ("Diego1234", "5491150577319", 30),
    ("Tere12345", "5491162663854", 13),
    ("Maximo12345", "5491133821056", 12),
    ("mely12345", "5491130740231", 15),
    ("Pupi12345", "5491140912511", 14),
]

def recuperar_clientes_originales():
    """
    Recupera solamente los clientes originales que todavía no estén
    en la base de datos. No borra ni modifica clientes existentes.
    """
    conn = db()

    admin = conn.execute(
        "SELECT id FROM users WHERE username=? AND role='admin'",
        (DEFAULT_ADMIN_USER,)
    ).fetchone()

    if admin:
        hoy_inicial = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        for nombre, telefono, dias in CLIENTES_ORIGINALES:
            # Buscar por teléfono o nombre para no crear duplicados.
            existe = conn.execute(
                """SELECT id FROM clients
                   WHERE telefono=? OR nombre=? LIMIT 1""",
                (telefono, nombre)
            ).fetchone()

            if not existe:
                fecha = (
                    hoy_inicial + timedelta(days=dias)
                ).strftime("%Y-%m-%d")

                conn.execute(
                    """INSERT INTO clients
                       (nombre, telefono, vencimiento, reseller_id, created_at)
                       VALUES (?, ?, ?, ?, ?)""",
                    (
                        nombre,
                        telefono,
                        fecha,
                        admin["id"],
                        datetime.now().isoformat(timespec="seconds")
                    )
                )

        conn.commit()

    conn.close()

recuperar_clientes_originales()

# =========================
# ESTILO AURA / RAYOS
# =========================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background:
      radial-gradient(circle at 50% 0%, rgba(0,130,255,.22), transparent 35%),
      linear-gradient(rgba(0,0,18,.68), rgba(0,0,18,.88)),
      url("https://media.giphy.com/media/ojPd9AOyqYC35fA2tT/giphy.gif");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.stApp { background: transparent; color: #fff; }

h1, h2, h3 {
    color: #fff !important;
    font-weight: 950 !important;
    text-shadow: 0 0 6px #00d9ff, 0 0 16px #0077ff, 0 0 30px #004cff;
}

/* Título con gradiente animado */
h1 {
    font-family: Impact, Haettenschweiler, "Arial Black", sans-serif !important;
    letter-spacing: 2px;
    background: linear-gradient(90deg,#fff,#00d9ff,#4f7cff,#fff,#00d9ff);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: auraText 3s linear infinite;
    position: relative;
    filter: drop-shadow(0 0 8px #008cff);
}
h1::after {
    content: "⚡";
    -webkit-text-fill-color: #63eaff;
    margin-left: 10px;
    animation: bolt 0.65s infinite alternate;
}
@keyframes auraText {
    to { background-position: 300% center; }
}
@keyframes bolt {
    from { opacity:.35; transform: scale(.8) rotate(-8deg); }
    to { opacity:1; transform: scale(1.15) rotate(8deg); }
}

[data-testid="stVerticalBlock"] {
    background: linear-gradient(145deg,rgba(0,100,255,.14),rgba(0,0,30,.58));
    border: 1px solid rgba(0,200,255,.55);
    border-radius: 18px;
    box-shadow: 0 0 14px rgba(0,120,255,.28), inset 0 0 20px rgba(0,100,255,.06);
}

.stButton > button, .stLinkButton > a {
    background: linear-gradient(135deg,#001a45,#006eff,#00d9ff) !important;
    color: #fff !important;
    border: 1px solid #72edff !important;
    border-radius: 14px !important;
    font-weight: 900 !important;
    text-shadow: 0 0 7px #002cff;
    box-shadow: 0 0 7px #00aaff, 0 0 20px rgba(0,120,255,.55);
    transition: .2s;
}
.stButton > button:hover, .stLinkButton > a:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 0 12px #00eaff, 0 0 32px #006eff;
}

.stTextInput input, .stNumberInput input, .stDateInput input {
    background: rgba(0,8,30,.9) !important;
    color: #fff !important;
    border: 1px solid #008cff !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] {
    border: 1px solid rgba(0,190,255,.55) !important;
    border-radius: 15px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN
# =========================
if "user" not in st.session_state:
    st.session_state.user = None

def login():
    st.markdown("## 🔐 ACCESO AL PANEL")
    st.markdown("### ⚡ GESTOR DE COBROS ⚡")
    with st.form("login_form"):
        username = st.text_input("👤 Usuario")
        password = st.text_input("🔑 Contraseña", type="password")
        entrar = st.form_submit_button("⚡ ENTRAR AL PANEL")
        if entrar:
            conn = db()
            row = conn.execute(
                "SELECT * FROM users WHERE username=? AND active=1",
                (username.strip(),)
            ).fetchone()
            conn.close()

            if row and row["password_hash"] == hash_password(password):
                st.session_state.user = dict(row)
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos.")


login_needed = st.session_state.user is None
if login_needed:
    login()
    st.stop()

user = st.session_state.user

# =========================
# CABECERA + GOKU
# =========================
st.title("⚡ GESTOR DE COBROS ⚡")
st.caption(
    f"Panel {'ADMINISTRADOR' if user['role']=='admin' else 'REVENDEDOR'} · "
    f"Usuario: {user['username']}"
)

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
""", height=95)

if st.button("🚪 Cerrar sesión"):
    st.session_state.user = None
    st.rerun()

# =========================
# FUNCIONES CLIENTES
# =========================
def add_client(nombre, telefono, fecha, reseller_id):
    conn = db()
    conn.execute(
        """INSERT INTO clients(nombre,telefono,vencimiento,reseller_id,created_at)
           VALUES(?,?,?,?,?)""",
        (nombre, telefono, fecha, reseller_id,
         datetime.now().isoformat(timespec="seconds"))
    )
    conn.commit()
    conn.close()

def get_clients():
    conn = db()
    if user["role"] == "admin":
        rows = conn.execute("""
            SELECT c.*, u.username AS revendedor
            FROM clients c
            LEFT JOIN users u ON u.id=c.reseller_id
            ORDER BY c.vencimiento ASC
        """).fetchall()
    else:
        rows = conn.execute("""
            SELECT c.*, u.username AS revendedor
            FROM clients c
            LEFT JOIN users u ON u.id=c.reseller_id
            WHERE c.reseller_id=?
            ORDER BY c.vencimiento ASC
        """, (user["id"],)).fetchall()
    conn.close()
    return rows

# =========================
# ADMIN: REVENDEDORES
# =========================
if user["role"] == "admin":
    st.subheader("👑 CONTROL DE REVENDEDORES")

    with st.expander("➕ Crear nuevo revendedor", expanded=False):
        with st.form("crear_revendedor"):
            nuevo_usuario = st.text_input("👤 Usuario del revendedor")
            nueva_clave = st.text_input("🔑 Contraseña", type="password")
            crear = st.form_submit_button("💾 Crear revendedor")
            if crear:
                if not nuevo_usuario.strip() or not nueva_clave:
                    st.error("Completá usuario y contraseña.")
                else:
                    conn = db()
                    try:
                        conn.execute(
                            "INSERT INTO users(username,password_hash,role) VALUES(?,?,?)",
                            (nuevo_usuario.strip(), hash_password(nueva_clave), "revendedor")
                        )
                        conn.commit()
                        st.success(f"✅ Revendedor {nuevo_usuario.strip()} creado.")
                    except sqlite3.IntegrityError:
                        st.error("❌ Ese usuario ya existe.")
                    finally:
                        conn.close()

    conn = db()
    revendedores = conn.execute(
        "SELECT id,username,active FROM users WHERE role='revendedor' ORDER BY username"
    ).fetchall()
    conn.close()

    if revendedores:
        st.markdown("**Revendedores registrados:**")
        for r in revendedores:
            st.write(
                f"👤 **{r['username']}** · "
                f"{'🟢 Activo' if r['active'] else '🔴 Desactivado'}"
            )

    # =========================
    # CONTROL DE CLIENTES DE REVENDEDORES
    # =========================
    st.subheader("🧑‍💼 CLIENTES DE MIS REVENDEDORES")
    st.caption("Acá podés controlar quién tiene cada cliente y qué clientes agregó cada revendedor.")

    conn = db()
    clientes_reventa = conn.execute("""
        SELECT c.*, u.username AS revendedor
        FROM clients c
        INNER JOIN users u ON u.id = c.reseller_id
        WHERE c.reseller_id != ?
          AND u.role = 'revendedor'
        ORDER BY u.username, c.vencimiento ASC
    """, (user["id"],)).fetchall()
    conn.close()

    if not clientes_reventa:
        st.info("Todavía no hay clientes cargados por tus revendedores.")
    else:
        for cr in clientes_reventa:
            venc_cr = datetime.strptime(cr["vencimiento"], "%Y-%m-%d")
            dias_cr = (venc_cr - datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0
            )).days

            with st.container():
                st.markdown(
                    f"### 🧑‍💼 {cr['revendedor']}  →  👤 {cr['nombre']}"
                )
                st.write(f"📱 Teléfono: **{cr['telefono'] or 'Sin teléfono'}**")
                st.write(f"📅 Vencimiento: **{venc_cr.strftime('%d/%m/%Y')}**")
                st.write(f"⏳ Días restantes: **{dias_cr}**")
                st.divider()

    # =========================
    # SEGURIDAD DEL ADMINISTRADOR
    # =========================
    with st.expander("🔐 Cambiar acceso de administrador", expanded=False):
        st.caption("Podés cambiar el usuario y la contraseña con los que entrás al panel.")

        with st.form("cambiar_acceso_admin"):
            nuevo_usuario_admin = st.text_input(
                "👤 Nuevo usuario",
                value=user["username"]
            )
            nueva_clave_admin = st.text_input(
                "🔑 Nueva contraseña",
                type="password"
            )
            confirmar_clave_admin = st.text_input(
                "🔑 Confirmar nueva contraseña",
                type="password"
            )

            cambiar_acceso = st.form_submit_button("💾 GUARDAR NUEVO ACCESO")

            if cambiar_acceso:
                nuevo_usuario_admin = nuevo_usuario_admin.strip()

                if not nuevo_usuario_admin:
                    st.error("⚠️ El usuario no puede quedar vacío.")
                elif not nueva_clave_admin:
                    st.error("⚠️ Escribí una nueva contraseña.")
                elif nueva_clave_admin != confirmar_clave_admin:
                    st.error("❌ Las contraseñas no coinciden.")
                elif len(nueva_clave_admin) < 6:
                    st.error("⚠️ La contraseña debe tener al menos 6 caracteres.")
                else:
                    conn = db()
                    existe = conn.execute(
                        "SELECT id FROM users WHERE username=? AND id<>?",
                        (nuevo_usuario_admin, user["id"])
                    ).fetchone()

                    if existe:
                        st.error("❌ Ese usuario ya está siendo utilizado.")
                    else:
                        conn.execute(
                            """UPDATE users
                               SET username=?, password_hash=?
                               WHERE id=?""",
                            (
                                nuevo_usuario_admin,
                                hash_password(nueva_clave_admin),
                                user["id"]
                            )
                        )
                        conn.commit()
                        conn.close()

                        # Actualizar la sesión actual para no expulsar al administrador.
                        st.session_state.user["username"] = nuevo_usuario_admin
                        st.success("✅ Acceso de administrador actualizado correctamente.")
                        st.rerun()

    st.markdown("---")
    st.subheader("📊 CONTROL GENERAL")
    all_clients = get_clients()
    st.metric("👥 Clientes totales", len(all_clients))
    st.metric("🧑‍💼 Revendedores", len(revendedores))

# =========================
# NUEVO CLIENTE
# =========================
st.subheader("➕ Nuevos usuarios")

with st.expander("Agregar cliente", expanded=False):
    with st.form("nuevo_cliente"):
        nombre = st.text_input("👤 Nombre / usuario")
        telefono = st.text_input("📱 Teléfono")
        fecha = st.date_input(
            "📅 Fecha de vencimiento",
            value=(datetime.now() + timedelta(days=30)).date()
        )

        # Admin puede asignar el cliente a un revendedor.
        asignado = user["id"]
        if user["role"] == "admin" and revendedores:
            opciones = {r["username"]: r["id"] for r in revendedores}
            elegido = st.selectbox("🧑‍💼 Revendedor responsable", ["Administrador"] + list(opciones))
            asignado = opciones.get(elegido, user["id"])

        guardar = st.form_submit_button("💾 AGREGAR CLIENTE")

        if guardar:
            if not nombre.strip():
                st.error("⚠️ Escribí el nombre/usuario.")
            else:
                add_client(
                    nombre.strip(),
                    telefono.strip(),
                    fecha.strftime("%Y-%m-%d"),
                    asignado
                )
                st.success("✅ Cliente agregado correctamente.")
                st.rerun()

# =========================
# MIS CLIENTES
# =========================
st.subheader("👤 MIS CLIENTES")

if user["role"] == "admin":
    conn = db()
    clientes = conn.execute("""
        SELECT c.*, u.username AS revendedor
        FROM clients c
        LEFT JOIN users u ON u.id = c.reseller_id
        WHERE c.reseller_id=?
        ORDER BY c.vencimiento ASC
    """, (user["id"],)).fetchall()
    conn.close()
else:
    clientes = get_clients()


if not clientes:
    st.info("Todavía no hay clientes.")

for c in clientes:
    vencimiento = datetime.strptime(c["vencimiento"], "%Y-%m-%d")
    hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    dias = (vencimiento - hoy).days
    fecha_str = vencimiento.strftime("%d/%m/%Y")

    with st.container():
        if dias < 0:
            st.markdown(f"### ❌ {c['nombre']} · VENCIDO")
        elif dias == 0:
            st.markdown(f"### 🚨 {c['nombre']} · VENCE HOY")
        elif dias <= 3:
            st.markdown(f"### ⚠️ {c['nombre']} · VENCE EN {dias} DÍAS")
        elif dias <= 7:
            st.markdown(f"### 🔔 {c['nombre']} · Vence en {dias} días")
        else:
            st.markdown(f"### ✅ {c['nombre']} · Vence en {dias} días")

        st.write(f"📅 Vencimiento: **{fecha_str}**")
        st.write(f"📱 Teléfono: **{c['telefono'] or 'Sin teléfono'}**")

        with st.expander("⚙️ Administrar cliente"):
            nueva_fecha = st.date_input(
                "Nueva fecha",
                value=vencimiento.date(),
                key=f"fecha_{c['id']}"
            )
            dias_renovar = st.number_input(
                "Días para renovar",
                min_value=1,
                value=30,
                step=1,
                key=f"dias_{c['id']}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("💾 Guardar fecha", key=f"save_{c['id']}"):
                    conn = db()
                    conn.execute(
                        "UPDATE clients SET vencimiento=? WHERE id=?",
                        (nueva_fecha.strftime("%Y-%m-%d"), c["id"])
                    )
                    conn.commit()
                    conn.close()
                    st.rerun()

            with col2:
                if st.button("➕ Sumar días", key=f"add_{c['id']}"):
                    nueva = vencimiento + timedelta(days=int(dias_renovar))
                    conn = db()
                    conn.execute(
                        "UPDATE clients SET vencimiento=? WHERE id=?",
                        (nueva.strftime("%Y-%m-%d"), c["id"])
                    )
                    conn.commit()
                    conn.close()
                    st.rerun()

            with col3:
                if st.button("🔄 Renovar desde hoy", key=f"renew_{c['id']}"):
                    nueva = hoy + timedelta(days=int(dias_renovar))
                    conn = db()
                    conn.execute(
                        "UPDATE clients SET vencimiento=? WHERE id=?",
                        (nueva.strftime("%Y-%m-%d"), c["id"])
                    )
                    conn.commit()
                    conn.close()
                    st.rerun()

            if user["role"] == "admin":
                if st.button("🗑️ Eliminar cliente", key=f"delete_{c['id']}"):
                    conn = db()
                    conn.execute("DELETE FROM clients WHERE id=?", (c["id"],))
                    conn.commit()
                    conn.close()
                    st.rerun()

        mensaje = (
            f"🔔 ¡RECORDATORIO IMPORTANTE!\\n\\n"
            f"Hola 👋 Te avisamos que tu cuenta {c['nombre']} está próxima a vencer.\\n\\n"
            f"📅 Fecha de vencimiento: {fecha_str}\\n"
            f"⏳ Días restantes: {dias} días\\n\\n"
            f"⚡ Para evitar que tu servicio se interrumpa, podés renovarlo antes de la fecha de vencimiento.\\n\\n"
            f"📲 ¿Querés renovar? Escribinos y te ayudamos con la renovación.\\n\\n"
            f"🙏 ¡Gracias por seguir confiando en nuestro servicio!"
        )

        if c["telefono"].strip():
            link = (
                f"https://wa.me/{c['telefono'].strip()}"
                f"?text={urllib.parse.quote(mensaje)}"
            )
            st.link_button("📲 Enviar WhatsApp", link)

        st.divider()
