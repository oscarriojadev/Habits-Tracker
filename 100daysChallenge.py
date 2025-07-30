# ----------------------------------------------------------
# 0. Imports
# ----------------------------------------------------------
import streamlit as st
import calendar
import json
import os
import pandas as pd
from datetime import date

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
# 2. Parse the 100-day syllabus (same as before)
# ----------------------------------------------------------
CSV = """Grupo\t# Aptitud\tAptitud\t# Tema\tTema\tPáginas
Materias Comunes\t1\tProducción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas\t1\tIntroducción a las encuestas y formulación de objetivos y marcos\t20
...
Especialidad II: Ciencias Sociales y Económicas\t4\tModelos Econométricos\t14\tAjuste estacional, desagregación temporal y calibrado de series temporales\t24"""

from io import StringIO
df = pd.read_csv(StringIO(CSV), sep="\t")
df["label"] = (
    df["Grupo"].str[:20] + " | " +
    df["Aptitud"].str[:30] + " | " +
    "Tema " + df["# Tema"].astype(str) + ": " + df["Tema"].str[:40]
)
syllabus = df.set_index("label")["Páginas"].to_dict()

# ----------------------------------------------------------
# 3. Gamification ranks
# ----------------------------------------------------------
RANKS = [
    (0,    "🪙 Copper",    "#cd7f32"),
    (200,  "🥉 Bronze",    "#cd7f32"),
    (500,  "🥈 Silver",    "#c0c0c0"),
    (900,  "🥇 Gold",      "#ffd700"),
    (1400, "💎 Platinum",  "#e5e4e2"),
    (2000, "🔥 Elite",     "#ff4500"),
    (2600, "🌟 Master",    "#9370db"),
    (3000, "🏆 Legend",    "#00ff7f"),
]

def get_rank(pages):
    for threshold, name, _ in RANKS[::-1]:
        if pages >= threshold:
            return threshold, name
    return 0, RANKS[0][1]

def build_pyramid(pages):
    """Tiny ASCII pyramid that fills with █ bricks."""
    total_bricks = 20
    ratio = min(pages / 3000, 1.0)
    filled = int(ratio * total_bricks)
    pyramid = "█" * filled + "░" * (total_bricks - filled)
    return f"`[{pyramid}]`"

# ----------------------------------------------------------
# 4. Sidebar – GLOBAL progress
# ----------------------------------------------------------
st.set_page_config(page_title="100-Day Challenge", page_icon="📚")
st.sidebar.title("📊 Progress")
total_pages = sum(day.get("paginas", 0) for day in data.values())
st.sidebar.metric(label="Pages read", value=f"{total_pages} / 3000")

progress = total_pages / 3000
st.sidebar.progress(progress)

_, current_rank = get_rank(total_pages)
st.sidebar.write(f"**Rank:** {current_rank}")

st.sidebar.markdown(build_pyramid(total_pages))

# ----------------------------------------------------------
# 5. Main page – month / day selector (same)
# ----------------------------------------------------------
st.title("📚 El Reto de los 100 Días")
st.markdown("Estudia 30 páginas diarias y lleva un registro de tu progreso.")

meses = {
    "Agosto 2025": 8,
    "Septiembre 2025": 9,
    "Octubre 2025": 10,
    "Noviembre 2025": 11
}
mes_nombre = st.selectbox("Selecciona el mes:", list(meses.keys()))
mes = mes_nombre.split()[0]
año = 2025
cal = calendar.monthcalendar(año, meses[mes_nombre])
st.subheader(f"📅 {mes} {año}")

dias_del_mes = [d for week in cal for d in week if d != 0]
dia = st.selectbox("Selecciona el día:", dias_del_mes)
clave = f"{año}-{meses[mes_nombre]:02d}-{dia:02d}"

# ----------------------------------------------------------
# 6. Daily registration
# ----------------------------------------------------------
st.markdown("---")
st.subheader(f"📖 Registro del día {dia} de {mes}")

tema_label = st.selectbox("¿Qué tema estudiaste hoy?", options=syllabus.keys())
paginas_tema = syllabus[tema_label]
paginas = st.number_input(
    "¿Cuántas páginas estudiaste hoy?",
    min_value=0,
    max_value=100,
    value=paginas_tema
)
temario = st.text_area("Detalles / notas adicionales:", value=data.get(clave, {}).get("temario", ""))
color = st.color_picker("Elige el color del texto para este día", value=data.get(clave, {}).get("color", "#000000"))

if st.button("💾 Guardar registro"):
    data[clave] = {
        "tema": tema_label,
        "paginas": paginas,
        "temario": temario,
        "color": color
    }
    guardar_datos()

    # ---- Milestone celebration ----
    new_total = total_pages + paginas
    old_threshold, _ = get_rank(total_pages)
    new_threshold, new_rank = get_rank(new_total)

    if new_threshold > old_threshold:
        st.balloons()
        st.success(f"🎉 Milestone reached! You advanced to **{new_rank}**!")
    st.rerun()

# ----------------------------------------------------------
# 7. Calendar visual (unchanged except topic in tooltip)
# ----------------------------------------------------------
st.markdown("---")
st.subheader("📆 Calendario visual")

st.markdown("""
<style>
.tooltip { position:relative; display:inline-block; cursor:pointer; }
.tooltip .tooltiptext { visibility:hidden; width:220px; background-color:black; color:#fff; text-align:left;
  border-radius:6px; padding:8px; position:absolute; z-index:1; bottom:125%; left:50%; margin-left:-110px;
  opacity:0; transition:opacity 0.3s; font-size:12px; white-space:pre-wrap; }
.tooltip:hover .tooltiptext { visibility:visible; opacity:1; }
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
            registro = data.get(clave_dia, {})
            pag = registro.get("paginas", 0)
            tema = registro.get("tema", "")
            tem = registro.get("temario", "")
            color = registro.get("color", "#FFFFFF")
            tooltip_text = f"{tema}\n{tem}" if tem else tema
            html = f"""
            <div class="tooltip" style="color:{color}; font-weight:bold; font-size:18px;">
                {dia_semana}<br>{pag} pág.
                <span class="tooltiptext">{tooltip_text}</span>
            </div>
            """
            cols[i].markdown(html, unsafe_allow_html=True)
