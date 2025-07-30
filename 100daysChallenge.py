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
# 2. Complete syllabus (embedded)
# ----------------------------------------------------------
SYLLABUS = [
    ("Materias Comunes", 1, "Producción Estadística Oficial: Principios Básicos", 1, "Introducción a las encuestas y formulación de objetivos", 20),
    ("Materias Comunes", 1, "Producción Estadística Oficial: Principios Básicos", 2, "Ideas básicas sobre estimación en muestreo probabilístico", 22),
    ("Materias Comunes", 1, "Producción Estadística Oficial: Principios Básicos", 3, "Estimación insesgada en diseños muestrales sobre unidades elementales I", 23),
    ("Materias Comunes", 1, "Producción Estadística Oficial: Principios Básicos", 4, "Estimación insesgada en diseños muestrales sobre unidades elementales II", 18),
    ("Materias Comunes", 1, "Producción Estadística Oficial: Principios Básicos", 5, "Estimación insesgada en diseños muestrales sobre unidades elementales III", 17),
    ("Materias Comunes", 1, "Producción Estadística Oficial: Principios Básicos", 6, "Estimación insesgada en diseños muestrales sobre unidades elementales IV", 25),
    ("Materias Comunes", 1, "Producción Estadística Oficial: Principios Básicos", 7, "Estimación insesgada en diseños muestrales por conglomerados I", 17),
    ("Materias Comunes", 1, "Producción Estadística Oficial: Principios Básicos", 8, "Métodos y gestión de la recogida de datos", 20),
    ("Materias Comunes", 1, "Producción Estadística Oficial: Principios Básicos", 9, "Introducción a la depuración e imputación de datos", 29),
    ("Materias Comunes", 1, "Producción Estadística Oficial: Principios Básicos", 10, "Introducción a la estimación con falta de respuesta", 19),
    ("Materias Comunes", 1, "Producción Estadística Oficial: Principios Básicos", 11, "Imputación", 20),
    ("Materias Comunes", 1, "Producción Estadística Oficial: Principios Básicos", 12, "Control del secreto estadístico", 18),
    ("Materias Comunes", 1, "Producción Estadística Oficial: Principios Básicos", 13, "Difusión de datos: Presentación de estadísticas", 20),
    ("Materias Comunes", 1, "Producción Estadística Oficial: Principios Básicos", 14, "Record linkage", 22),
    ("Materias Comunes", 1, "Producción Estadística Oficial: Principios Básicos", 15, "Metadatos de la producción estadística I", 38),
    ("Materias Comunes", 1, "Producción Estadística Oficial: Principios Básicos", 16, "Metadatos de la producción estadística II", 25),
    ("Materias Comunes", 1, "Producción Estadística Oficial: Principios Básicos", 17, "Metadatos de la producción estadística III", 20),
    ("Materias Comunes", 1, "Producción Estadística Oficial: Principios Básicos", 18, "La calidad en la estadística oficial y el Código Europeo", 23),
    ("Materias Comunes", 2, "Inferencia y modelización estadísticas", 1, "Propiedades de una muestra aleatoria", 30),
    ("Materias Comunes", 2, "Inferencia y modelización estadísticas", 2, "Principios de reducción de datos", 14),
    ("Materias Comunes", 2, "Inferencia y modelización estadísticas", 3, "Estimación puntual I", 20),
    ("Materias Comunes", 2, "Inferencia y modelización estadísticas", 4, "Estimación puntual II", 12),
    ("Materias Comunes", 2, "Inferencia y modelización estadísticas", 5, "Tests de hipótesis", 28),
    ("Materias Comunes", 2, "Inferencia y modelización estadísticas", 6, "Estimación por intervalos I", 23),
    ("Materias Comunes", 2, "Inferencia y modelización estadísticas", 7, "Estimación por intervalos II", 13),
    ("Materias Comunes", 2, "Inferencia y modelización estadísticas", 8, "Introducción a modelos lineal y lineal generalizado", 22),
    ("Materias Comunes", 2, "Inferencia y modelización estadísticas", 9, "Modelos lineales: mínimos cuadrados", 20),
    ("Materias Comunes", 2, "Inferencia y modelización estadísticas", 10, "Modelos lineales: Inferencia estadística", 20),
    ("Materias Comunes", 3, "Almacenamiento y Modelos de Datos", 1, "Representación y almacenamiento de la información", 16),
    ("Materias Comunes", 3, "Almacenamiento y Modelos de Datos", 2, "Componentes del hardware de un sistema de computación", 39),
    ("Materias Comunes", 3, "Almacenamiento y Modelos de Datos", 3, "Sistemas operativos", 38),
    ("Materias Comunes", 3, "Almacenamiento y Modelos de Datos", 4, "Bases de datos", 18),
    ("Materias Comunes", 4, "Cuentas", 1, "Objeto y método de la ciencia económica", 21),
    ("Materias Comunes", 4, "Cuentas", 2, "Los sistemas internacionales de Cuentas Nacionales", 17),
    ("Materias Comunes", 4, "Cuentas", 3, "Flujos y stocks en el SEC 2010", 16),
    ("Materias Comunes", 4, "Cuentas", 4, "El sistema de cuentas y los agregados en el SEC 2010 (I)", 28),
    ("Materias Comunes", 4, "Cuentas", 5, "El sistema de cuentas y los agregados en el SEC 2010 (II)", 22),
    ("Materias Comunes", 4, "Cuentas", 6, "Tablas de origen y destino y marco input-output", 26),
    ("Materias Comunes", 4, "Cuentas", 7, "Medición de variaciones de precio y volumen", 20),
    ("Materias Comunes", 4, "Cuentas", 8, "Cuentas nacionales trimestrales y regionales", 19),
    ("Materias Comunes", 4, "Cuentas", 9, "Más allá del marco central del SEC 2010", 32),
    ("Materias Comunes", 5, "Demografía", 1, "La demografía y principios del análisis", 18),
    ("Materias Comunes", 5, "Demografía", 2, "Mortalidad", 23),
    ("Materias Comunes", 5, "Demografía", 3, "Natalidad y fecundidad", 18),
    ("Materias Comunes", 5, "Demografía", 4, "Migraciones", 16),
    ("Materias Comunes", 5, "Demografía", 5, "Estructura y crecimiento de la población", 20),
    ("Materias Comunes", 5, "Demografía", 6, "Proyecciones de población", 20),
    ("Materias Comunes", 5, "Demografía", 7, "Hogares y formas de convivencia", 19),
    ("Materias Comunes", 5, "Demografía", 8, "Nupcialidad y rupturas matrimoniales", 19),
    ("Materias Comunes", 5, "Demografía", 9, "Censos demográficos", 12),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Contabilidad Financiera", 1, "La relevancia de la información contable", 23),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Contabilidad Financiera", 2, "El modelo contable", 26),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Contabilidad Financiera", 3, "La información financiera y no financiera", 27),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Contabilidad Financiera", 4, "Existencias", 23),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Contabilidad Financiera", 5, "El Impuesto de Valor Añadido (IVA)", 21),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Contabilidad Financiera", 6, "Cuentas a cobrar y a pagar", 23),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Contabilidad Financiera", 7, "Activo no corriente", 28),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Contabilidad Financiera", 8, "Otras normas sobre inmovilizado", 23),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Contabilidad Financiera", 9, "Activos y pasivos financieros", 59),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Contabilidad Financiera", 10, "Patrimonio neto", 25),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Contabilidad Financiera", 11, "Provisiones, impuestos, errores", 24),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Contabilidad Financiera", 12, "Cuentas anuales y auditoría", 15),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 1, "El funcionamiento del mercado competitivo", 26),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 2, "Producción y costes", 22),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 3, "Las estructuras de los mercados", 26),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 4, "El mercado de bienes y servicios en economía cerrada", 20),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 5, "Mercado de activos financieros y dinero", 22),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 6, "El modelo IS-LM en economía cerrada", 22),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 7, "Demanda de consumo", 21),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 8, "Demanda de inversión", 25),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 9, "Equilibrio OA-DA", 22),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 10, "El desempleo", 28),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 11, "Perturbaciones de la OA", 20),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 12, "Inflación: medición y causas", 20),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 13, "Curva de Phillips y NAIRU", 16),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 14, "El crecimiento económico", 25),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 15, "Los ciclos económicos", 25),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 16, "El equilibrio externo", 30),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 17, "La política monetaria", 25),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 18, "La política fiscal", 25),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 19, "La política mixta", 25),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 20, "El modelo Mundell-Fleming", 24),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 21, "Crisis financiera", 30),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 22, "Integración europea (I)", 28),
    ("Especialidad II: Ciencias Sociales y Económicas", 1, "Economía General", 23, "Integración europea (II)", 27),
    ("Especialidad II: Ciencias Sociales y Económicas", 3, "Sector Público y Sistema Fiscal", 1, "Presupuestos Generales del Estado", 22),
    ("Especialidad II: Ciencias Sociales y Económicas", 3, "Sector Público y Sistema Fiscal", 2, "Presupuestos autonómicos y locales", 19),
    ("Especialidad II: Ciencias Sociales y Económicas", 3, "Sector Público y Sistema Fiscal", 3, "El sistema fiscal español", 21),
    ("Especialidad II: Ciencias Sociales y Económicas", 3, "Sector Público y Sistema Fiscal", 4, "IRPF", 21),
    ("Especialidad II: Ciencias Sociales y Económicas", 3, "Sector Público y Sistema Fiscal", 5, "IRNR", 19),
    ("Especialidad II: Ciencias Sociales y Económicas", 3, "Sector Público y Sistema Fiscal", 6, "Impuesto de Sociedades", 24),
    ("Especialidad II: Ciencias Sociales y Económicas", 3, "Sector Público y Sistema Fiscal", 7, "IVA", 24),
    ("Especialidad II: Ciencias Sociales y Económicas", 3, "Sector Público y Sistema Fiscal", 8, "Impuestos especiales", 21),
    ("Especialidad II: Ciencias Sociales y Económicas", 3, "Sector Público y Sistema Fiscal", 9, "Imposición autonómica y local", 29),
    ("Especialidad II: Ciencias Sociales y Económicas", 4, "Modelos Econométricos", 1, "Modelos causales y no causales", 21),
    ("Especialidad II: Ciencias Sociales y Económicas", 4, "Modelos Econométricos", 2, "Regresión con datos de sección cruzada I", 18),
    ("Especialidad II: Ciencias Sociales y Económicas", 4, "Modelos Econométricos", 3, "Regresión con datos de sección cruzada II", 17),
    ("Especialidad II: Ciencias Sociales y Económicas", 4, "Modelos Econométricos", 4, "Regresión con datos de sección cruzada III", 13),
    ("Especialidad II: Ciencias Sociales y Económicas", 4, "Modelos Econométricos", 5, "Regresión con datos de sección cruzada IV", 12),
    ("Especialidad II: Ciencias Sociales y Económicas", 4, "Modelos Econométricos", 6, "Otras técnicas de estimación", 10),
    ("Especialidad II: Ciencias Sociales y Económicas", 4, "Modelos Econométricos", 7, "Tests de especificación y selección de modelos", 14),
    ("Especialidad II: Ciencias Sociales y Económicas", 4, "Modelos Econométricos", 8, "Endogeneidad y variables instrumentales", 22),
    ("Especialidad II: Ciencias Sociales y Económicas", 4, "Modelos Econométricos", 9, "Modelos de panel lineales", 15),
    ("Especialidad II: Ciencias Sociales y Económicas", 4, "Modelos Econométricos", 10, "Procesos estocásticos estacionarios", 28),
    ("Especialidad II: Ciencias Sociales y Económicas", 4, "Modelos Econométricos", 11, "Modelos con tendencias", 20),
    ("Especialidad II: Ciencias Sociales y Económicas", 4, "Modelos Econométricos", 12, "Modelos de series temporales multiecuacionales", 13),
    ("Especialidad II: Ciencias Sociales y Económicas", 4, "Modelos Econométricos", 13, "Modelos de cointegración", 9),
    ("Especialidad II: Ciencias Sociales y Económicas", 4, "Modelos Econométricos", 14, "Ajuste estacional y desagregación temporal", 24),
]

# Build nested dicts
grupo_apt = defaultdict(list)          # grupo -> [(id, nombre), ...]
apt_tema  = defaultdict(list)          # (grupo, apt_nombre) -> [(t_id, tema, pages)]
grupos = []
for g, aid, aname, tid, tema, pages in SYLLABUS:
    if (aid, aname) not in grupo_apt[g]:
        grupo_apt[g].append((aid, aname))
    apt_tema[(g, aname)].append((tid, tema, pages))
grupos = sorted(grupo_apt.keys())

# ----------------------------------------------------------
# 3. Gamification helpers
# ----------------------------------------------------------
RANKS = [
    (0, "🪙 Copper"), (200, "🥉 Bronze"), (500, "🥈 Silver"),
    (900, "🥇 Gold"), (1400, "💎 Platinum"), (2000, "🔥 Elite"),
    (2600, "🌟 Master"), (3000, "🏆 Legend")
]
def get_rank(pages):
    for th, name in RANKS[::-1]:
        if pages >= th:
            return th, name
    return 0, RANKS[0][1]

# ----------------------------------------------------------
# 4. Sidebar progress
# ----------------------------------------------------------
st.set_page_config(page_title="100-Day Challenge", page_icon="📚")
st.sidebar.title("📊 Progreso global")
total_pages = sum(d.get("paginas", 0) for d in data.values())
st.sidebar.metric(label="Páginas leídas", value=f"{total_pages} / 3000")
st.sidebar.progress(total_pages / 3000)
_, rank = get_rank(total_pages)
st.sidebar.write(f"**Rango:** {rank}")

# ----------------------------------------------------------
# 5. Month / Day selector
# ----------------------------------------------------------
st.title("📚 El Reto de los 100 Días")
meses = {"Agosto 2025": 8, "Septiembre 2025": 9, "Octubre 2025": 10, "Noviembre 2025": 11}
mes_nombre = st.selectbox("Selecciona el mes:", list(meses.keys()))
mes = mes_nombre.split()[0]
año = 2025
cal = calendar.monthcalendar(año, meses[mes_nombre])
dias = [d for week in cal for d in week if d != 0]
dia = st.selectbox("Selecciona el día:", dias)
clave = f"{año}-{meses[mes_nombre]:02d}-{dia:02d}"

# ----------------------------------------------------------
# 6. Dynamic multi-topic registration with dependent dropdowns
# ----------------------------------------------------------
st.markdown("---")
st.subheader(f"📖 Registro del día {dia} de {mes}")

record = data.get(clave, {})
topics = record.get("topics", [])
rows = st.number_input("¿Cuántos temas estudiaste?", min_value=0, max_value=10, value=max(1, len(topics)))

new_topics = []
total_day = 0

for idx in range(rows):
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    with col1:
        grupo = st.selectbox("Grupo", grupos, key=f"g_{clave}_{idx}")
        aptitudes = [f"{aid} - {aname}" for aid, aname in grupo_apt[grupo]]
    with col2:
        apt_sel = st.selectbox("Aptitud", aptitudes, key=f"a_{clave}_{idx}")
        aid, aname = apt_sel.split(" - ", 1)
        temas = apt_tema[(grupo, aname)]
    with col3:
        tema_sel = st.selectbox("Tema", [f"{tid} - {tema} ({pages} p.)" for tid, tema, pages in temas], key=f"t_{clave}_{idx}")
        tid, rest = tema_sel.split(" - ", 1)
        tema, pages_str = rest.rsplit(" (", 1)
        pages_total = int(pages_str.split(" ")[0])
    with col4:
        pages_read = st.number_input("Páginas", min_value=0, max_value=100, value=pages_total, key=f"p_{clave}_{idx}")
    new_topics.append({"grupo": grupo, "aptitud_id": int(aid), "aptitud_nombre": aname, "tema_id": int(tid), "tema_nombre": tema, "paginas": pages_read})
    total_day += pages_read

notas = st.text_area("Notas adicionales:", value=record.get("notas", ""))
color = st.color_picker("Color para el día", value=record.get("color", "#000000"))

if st.button("💾 Guardar registro"):
    data[clave] = {"topics": new_topics, "paginas": total_day, "notas": notas, "color": color}
    guardar_datos()
    new_total = total_pages + total_day
    _, new_rank = get_rank(new_total)
    if new_total > total_pages:
        st.balloons()
        st.success(f"🎉 ¡Subiste a {new_rank}!")
    st.rerun()

# ----------------------------------------------------------
# 7. Calendar visual WITH tooltip
# ----------------------------------------------------------
st.markdown("---")
st.subheader("📆 Calendario visual")

# CSS for nice tooltips
st.markdown("""
<style>
.tooltip {
  position: relative;
  display: inline-block;
  font-weight: bold;
  font-size: 18px;
  cursor: pointer;
}
.tooltip .tooltiptext {
  visibility: hidden;
  width: 260px;
  background-color: #111;
  color: #fff;
  text-align: left;
  border-radius: 6px;
  padding: 8px;
  position: absolute;
  z-index: 10;
  bottom: 125%;
  left: 50%;
  margin-left: -130px;
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 12px;
  white-space: pre-wrap;
  line-height: 1.2;
}
.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}
</style>
""", unsafe_allow_html=True)

for semana in calendar.monthcalendar(año, meses[mes_nombre]):
    cols = st.columns(7)
    for i, d in enumerate(semana):
        if d == 0:
            cols[i].write("")
            continue
        key = f"{año}-{meses[mes_nombre]:02d}-{d:02d}"
        rec = data.get(key, {})
        pag = rec.get("paginas", 0)
        color = rec.get("color", "#FFFFFF")

        # Build tooltip content
        tips = []
        for t in rec.get("topics", []):
            tips.append(f"• {t['tema_nombre']} ({t['paginas']} p.)")
        if rec.get("notas"):
            tips.append(f"Notas: {rec['notas']}")
        tooltip_body = "\n".join(tips) if tips else "Sin registro"

        html = f"""
        <div class="tooltip" style="color:{color};">
            {d}<br>{pag} pág.
            <span class="tooltiptext">{tooltip_body}</span>
        </div>
        """
        cols[i].markdown(html, unsafe_allow_html=True)
