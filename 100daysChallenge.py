# ----------------------------------------------------------
# 0. Imports
# ----------------------------------------------------------
import streamlit as st
import calendar
import json
import os
from collections import defaultdict

# ----------------------------------------------------------
# 1. Data file
# ----------------------------------------------------------
DATA_FILE = "reto_100_dias.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {}

def guardar_datos():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ----------------------------------------------------------
# 2. Parse syllabus into nested dicts
# ----------------------------------------------------------
SYLLABUS_ROWS = """\
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	1	Introducción a las encuestas y formulación de objetivos y marcos	20
... (whole syllabus pasted exactly as before) ...
Especialidad II: Ciencias Sociales y Económicas	4	Modelos Econométricos	14	Ajuste estacional, desagregación temporal y calibrado de series temporales	24"""

# Build nested dicts
grupo_aptitud = defaultdict(list)        # grupo -> list of (aptitud_id, aptitud_name)
aptitud_tema  = defaultdict(list)        # (grupo, aptitud_name) -> list of (tema_id, tema_name, pages)
grupo_options = []

for line in SYLLABUS_ROWS.strip().splitlines():
    grupo, apt_id, apt_nombre, tema_id, tema_nombre, paginas = line.split("\t")
    key_apt = (grupo, apt_id, apt_nombre)
    if key_apt not in grupo_aptitud[grupo]:
        grupo_aptitud[grupo].append((apt_id, apt_nombre))
    aptitud_tema[(grupo, apt_nombre)].append((tema_id, tema_nombre, int(paginas)))

grupo_options = sorted(grupo_aptitud.keys())

# ----------------------------------------------------------
# 3. Gamification
# ----------------------------------------------------------
RANKS = [
    (0,    "🪙 Copper",    "#cd7f32"), (200,  "🥉 Bronze",    "#cd7f32"),
    (500,  "🥈 Silver",    "#c0c0c0"), (900,  "🥇 Gold",      "#ffd700"),
    (1400, "💎 Platinum",  "#e5e4e2"), (2000, "🔥 Elite",     "#ff4500"),
    (2600, "🌟 Master",    "#9370db"), (3000, "🏆 Legend",    "#00ff7f"),
]

def get_rank(pages):
    for threshold, name, _ in RANKS[::-1]:
        if pages >= threshold:
            return threshold, name
    return 0, RANKS[0][1]

def build_pyramid(pages):
    total_bricks = 20
    filled = int(min(pages / 3000, 1.0) * total_bricks)
    return f"`[{'█'*filled}{'░'*(total_bricks-filled)}]`"

# ----------------------------------------------------------
# 4. Sidebar progress
# ----------------------------------------------------------
st.set_page_config(page_title="100-Day Challenge", page_icon="📚")
st.sidebar.title("📊 Progress")
total_pages = sum(day.get("paginas", 0) for day in data.values())
st.sidebar.metric(label="Pages read", value=f"{total_pages} / 3000")
st.sidebar.progress(total_pages / 3000)
_, current_rank = get_rank(total_pages)
st.sidebar.write(f"**Rank:** {current_rank}")
st.sidebar.markdown(build_pyramid(total_pages))

# ----------------------------------------------------------
# 5. Month / Day selector
# ----------------------------------------------------------
st.title("📚 El Reto de los 100 Días")
meses = {"Agosto 2025": 8, "Septiembre 2025": 9, "Octubre 2025": 10, "Noviembre 2025": 11}
mes_nombre = st.selectbox("Selecciona el mes:", list(meses.keys()))
mes = mes_nombre.split()[0]
año = 2025
cal = calendar.monthcalendar(año, meses[mes_nombre])
st.subheader(f"📅 {mes} {año}")

dias_del_mes = [d for week in cal for d in week if d != 0]
dia = st.selectbox("Selecciona el día:", dias_del_mes)
clave = f"{año}-{meses[mes_nombre]:02d}-{dia:02d}"

# ----------------------------------------------------------
# 6. Dynamic dependent dropdowns
# ----------------------------------------------------------
st.markdown("---")
st.subheader(f"📖 Registro del día {dia} de {mes}")

# Session-state helpers
if "sel_grupo" not in st.session_state: st.session_state.sel_grupo = grupo_options[0]
if "sel_aptitud" not in st.session_state: st.session_state.sel_aptitud = None
if "sel_tema" not in st.session_state: st.session_state.sel_tema = None

# 1) Grupo
grupo = st.selectbox("Grupo", grupo_options, key="grupo_select")
aptitud_list = grupo_aptitud[grupo]

# 2) Aptitud
aptitud_options = [f"{aid} - {aname}" for aid, aname in aptitud_list]
apt_sel = st.selectbox("Aptitud", aptitud_options, key="apt_select")
apt_id, apt_nombre = apt_sel.split(" - ", 1)

# 3) Tema
tema_list = aptitud_tema[(grupo, apt_nombre)]
tema_options = [f"{tid} - {tname} ({pages} p.)" for tid, tname, pages in tema_list]
tema_sel = st.selectbox("Tema", tema_options, key="tema_select")
tema_id, rest = tema_sel.split(" - ", 1)
tema_nombre, pages_str = rest.rsplit(" (", 1)
pages = int(pages_str.split(" ")[0])

# Allow fractional pages
pages_today = st.number_input("Páginas leídas de este tema", min_value=0, max_value=100, value=pages)
notas = st.text_area("Notas adicionales", value=data.get(clave, {}).get("notas", ""))
color = st.color_picker("Color para el día", value=data.get(clave, {}).get("color", "#000000"))

if st.button("💾 Guardar registro"):
    total_day = pages_today
    record = {
        "grupo": grupo,
        "aptitud_id": apt_id,
        "aptitud_nombre": apt_nombre,
        "tema_id": tema_id,
        "tema_nombre": tema_nombre,
        "paginas": total_day,
        "notas": notas,
        "color": color
    }
    data[clave] = record
    guardar_datos()
    new_total = total_pages + total_day
    old_threshold, _ = get_rank(total_pages)
    new_threshold, new_rank = get_rank(new_total)
    if new_threshold > old_threshold:
        st.balloons()
        st.success(f"🎉 ¡Nuevo rango alcanzado: **{new_rank}**!")
    st.rerun()

# ----------------------------------------------------------
# 7. Calendar visual
# ----------------------------------------------------------
st.markdown("---")
st.subheader("📆 Calendario visual")
st.markdown("""
<style>
.tooltip { position:relative; display:inline-block; cursor:pointer; }
.tooltip .tooltiptext { visibility:hidden; width:220px; background-color:black; color:#fff; text-align:left;
  border-radius:6px; padding:8px; position:absolute; z-index:1; bottom:125%; left:50%; margin-left:-110px;
  font-size:12px; white-space:pre-wrap; }
.tooltip:hover .tooltiptext { visibility:visible; }
</style>""", unsafe_allow_html=True)

dias_semana = ["L", "M", "X", "J", "V", "S", "D"]
cols_encabezado = st.columns(7)
for i, dia_nombre in enumerate(dias_semana):
    cols_encabezado[i].markdown(f"<b style='color:white;'>{dia_nombre}</b>", unsafe_allow_html=True)

for semana in cal:
    cols = st.columns(7)
    for i, dia_semana in enumerate(semana):
        if dia_semana == 0:
            cols[i].write("")
        else:
            clave_dia = f"{año}-{meses[mes_nombre]:02d}-{dia_semana:02d}"
            rec = data.get(clave_dia, {})
            pag = rec.get("paginas", 0)
            tema_short = rec.get("tema_nombre", "")[:25] + "…" if rec else ""
            color = rec.get("color", "#FFFFFF")
            tooltip_text = f"{rec.get('grupo','')}\n{rec.get('aptitud_nombre','')}\n{tema_short}\n{rec.get('notas','')}"
            html = f"""
            <div class="tooltip" style="color:{color}; font-weight:bold; font-size:18px;">
                {dia_semana}<br>{pag} pág.
                <span class="tooltiptext">{tooltip_text}</span>
            </div>
            """
            cols[i].markdown(html, unsafe_allow_html=True)
