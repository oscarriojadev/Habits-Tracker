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

# Mostrar semana por semana
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
            col = registro.get("color", "#000000")
            cols[i].markdown(
                f"<div style='color:{col}; font-weight:bold;'>{dia_semana}<br>{pag} pág.</div>",
                unsafe_allow_html=True
            )
