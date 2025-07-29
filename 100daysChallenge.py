import streamlit as st
import calendar
from datetime import date
import json
import os

# Archivo para guardar los datos
DATA_FILE = "reto_100_dias.json"

# Cargar datos previos
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {}

# Función para guardar datos
def guardar_datos():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Título de la app
st.title("📚 El Reto de los 100 Días")
st.markdown("Estudia 30 páginas diarias y lleva un registro de tu progreso.")

# Selector de mes
meses = {
    "Agosto 2025": 8,
    "Septiembre 2025": 9,
    "Octubre 2025": 10,
    "Noviembre 2025": 11
}
mes_nombre = st.selectbox("Selecciona el mes:", list(meses.keys()))
mes = mes_nombre.split()[0]
año = 2025

# Días del mes seleccionado
cal = calendar.monthcalendar(año, meses[mes_nombre])
st.subheader(f"📅 {mes} {año}")

# Selector de día
dias_del_mes = [d for week in cal for d in week if d != 0]
dia = st.selectbox("Selecciona el día:", dias_del_mes)

# Clave única para el día
clave = f"{año}-{meses[mes_nombre]:02d}-{dia:02d}"

# Mostrar entrada si ya hay datos
st.markdown("---")
st.subheader(f"📖 Registro del día {dia} de {mes}")

paginas = st.number_input("¿Cuántas páginas estudiaste hoy?", min_value=0, max_value=100, value=data.get(clave, {}).get("paginas", 0))
temario = st.text_area("Temario estudiado:", value=data.get(clave, {}).get("temario", ""))
color = st.color_picker("Elige el color del texto para este día", value=data.get(clave, {}).get("color", "#000000"))

if st.button("💾 Guardar registro"):
    data[clave] = {
        "paginas": paginas,
        "temario": temario,
        "color": color
    }
    guardar_datos()
    st.success("Registro guardado correctamente.")

# Mostrar calendario visual con resumen
st.markdown("---")
st.subheader("📆 Calendario visual")

# Estilo CSS para tooltips
st.markdown("""
<style>
.tooltip {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 220px;
  background-color: black;
  color: #fff;
  text-align: left;
  border-radius: 6px;
  padding: 8px;
  position: absolute;
  z-index: 1;
  bottom: 125%;
  left: 50%;
  margin-left: -110px;
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 12px;
  white-space: pre-wrap;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}
</style>
""", unsafe_allow_html=True)

# Mostrar semana por semana
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
            tem = registro.get("temario", "")
            color = registro.get("color", "#FFFFFF")
            if tem:
                html = f"""
                <div class="tooltip" style="color:{color}; font-weight:bold; font-size:18px;">
                    {dia_semana}<br>{pag} pág.
                    <span class="tooltiptext">{tem}</span>
                </div>
                """
            else:
                html = f"""
                <div style="color:{color}; font-weight:bold; font-size:18px;">
                    {dia_semana}<br>{pag} pág.
                </div>
                """
            cols[i].markdown(html, unsafe_allow_html=True)
