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
# 2. Syllabus (embedded)
# ----------------------------------------------------------
SYLLABUS_ROWS = """\
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	1	Introducción a las encuestas y formulación de objetivos y marcos	20
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	2	Ideas básicas sobre estimación en muestreo probabilístico	22
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	3	Estimación insesgada en diseños muestrales sobre unidades elementales I	23
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	4	Estimación insesgada en diseños muestrales sobre unidades elementales II	18
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	5	Estimación insesgada en diseños muestrales sobre unidades elementales III	17
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	6	Estimación insesgada en diseños muestrales sobre unidades elementales IV	25
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	7	Estimación insesgada en diseños muestrales por conglomerados I	17
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	8	Métodos y gestión de la recogida de datos	20
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	9	Introducción a la depuración e imputación de datos estadísticos en el proceso estadístico	29
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	10	Introducción a la estimación en presencia de falta de respuesta	19
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	11	Imputación	20
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	12	Control del secreto estadístico	18
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	13	Difusión de datos: Presentación de estadísticas	20
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	14	Record linkage	22
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	15	Metadatos de la producción estadística I	38
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	16	Metadatos de la producción estadística II	25
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	17	Metadatos de la producción estadística III	20
Materias Comunes	1	Producción Estadística Oficial: Principios Básicos del Ciclo de Producción de Operaciones Estadísticas	18	La calidad en la estadística oficial y el Código de Buenas Prácticas de las Estadísticas Europeas	23
Materias Comunes	2	Inferencia y modelización estadísticas	1	Propiedades de una muestra aleatoria	30
Materias Comunes	2	Inferencia y modelización estadísticas	2	Principios de reducción de datos	14
Materias Comunes	2	Inferencia y modelización estadísticas	3	Estimación puntual I	20
Materias Comunes	2	Inferencia y modelización estadísticas	4	Estimación puntual II	12
Materias Comunes	2	Inferencia y modelización estadísticas	5	Tests de hipótesis	28
Materias Comunes	2	Inferencia y modelización estadísticas	6	Estimación por intervalos I	23
Materias Comunes	2	Inferencia y modelización estadísticas	7	Estimación por intervalos II	13
Materias Comunes	2	Inferencia y modelización estadísticas	8	Introducción a los modelos lineal y lineal generalizado	22
Materias Comunes	2	Inferencia y modelización estadísticas	9	Modelos lineales: mínimos cuadrados	20
Materias Comunes	2	Inferencia y modelización estadísticas	10	Modelos lineales: Inferencia estadística	20
Materias Comunes	3	Almacenamiento y Modelos de Datos	1	Representación y almacenamiento de la información. Introducción. Bits y bytes. Organización de la memoria principal. Representación de la información como cadena de bits. Inexistencia de "tipos" para los ficheros en disco	16
Materias Comunes	3	Almacenamiento y Modelos de Datos	2	Componentes principales del hardware de un sistema de computación. Introducción	39
Materias Comunes	3	Almacenamiento y Modelos de Datos	3	Sistemas operativos	38
Materias Comunes	3	Almacenamiento y Modelos de Datos	4	Bases de datos	18
Materias Comunes	4	Cuentas	1	Objeto y método de la ciencia económica. Modelización y análisis gráfico. Microeconomía y macroeconomía. La medición de la actividad económica. El flujo circular de la renta	21
Materias Comunes	4	Cuentas	2	Los sistemas internacionales de Cuentas Nacionales	17
Materias Comunes	4	Cuentas	3	Flujos y stocks en el SEC 2010. Flujos. Propiedades y tipos de operaciones. Otras variaciones de los activos. Stocks. Tipos de activos y pasivos. Frontera de activos y pasivos. Stocks de población y empleo. Asalariados y no asalariados: personas, puestos de trabajo, puestos de trabajo equivalentes y horas totales trabajadas	16
Materias Comunes	4	Cuentas	4	El sistema de cuentas y los agregados en el SEC 2010 (I)	28
Materias Comunes	4	Cuentas	5	El sistema de cuentas y los agregados en el SEC 2010 (II)	22
Materias Comunes	4	Cuentas	6	Tablas de origen y destino y el marco input-output en el SEC 2010. Descripción detallada de las tablas de origen y destino y de las tablas input-output. Herramientas estadísticas y de análisis	26
Materias Comunes	4	Cuentas	7	Medición de las variaciones de precio y volumen en el SEC 2010. Campo de aplicación. Principios generales y problemas concretos. Medición de la renta real para el total de la economía. Índices de precios y volumen interespaciales	20
Materias Comunes	4	Cuentas	8	Las cuentas nacionales trimestrales y regionales en el SEC 2010. Especificidades de las cuentas nacionales trimestrales. Especificidades de las cuentas regionales	19
Materias Comunes	4	Cuentas	9	Más allá del marco central del SEC 2010. Cuentas satélite: características y ejemplos. Medidas de bienestar. La globalización y el comercio internacional en términos de valor añadido	32
Materias Comunes	5	Demografía	1	La demografía. Principios del análisis demográfico. Esquema de Lexis. Análisis longitudinal y análisis transversal. Indicadores demográficos: tasas, cocientes, proporciones	18
Materias Comunes	5	Demografía	2	Mortalidad. Análisis de la mortalidad: tasas brutas y tasas específicas. Mortalidad infantil. Tablas de mortalidad. Tablas completas y abreviadas. Esperanza de vida. Tablas-tipo de mortalidad. La mortalidad por causas y morbilidad	23
Materias Comunes	5	Demografía	3	Natalidad y fecundidad. Tasas. Intensidad y calendario. Descendencia e índice sintético de fecundidad. Edad media a la maternidad, curva de fecundidad. Reproducción y reemplazo	18
Materias Comunes	5	Demografía	4	Migraciones. Principales conceptos. Tipos de movilidad espacial. Migraciones interiores y exteriores. Tasas e indicadores asociados a los movimientos migratorios	16
Materias Comunes	5	Demografía	5	Estructura y crecimiento de la población. Indicadores de estructura. Pirámides de población. Indicadores y tasas de crecimiento. El envejecimiento de la población. Población estacionaria y población estable	20
Materias Comunes	5	Demografía	6	Proyecciones de población. Procedimientos matemáticos de estimación. El método de los componentes. Proyección de componentes. Estimadores intercensales de población	20
Materias Comunes	5	Demografía	7	Hogares y formas de convivencia. Hogares: conceptos y tipología. Estructura de hogares. Dinámica de hogares. Proyecciones de hogares	19
Materias Comunes	5	Demografía	8	Nupcialidad y rupturas matrimoniales. Tasas e indicadores sobre nupcialidad y divorcialidad. Intensidad y calendario. Relación entre fecundidad y nupcialidad	19
Materias Comunes	5	Demografía	9	Censos demográficos. Población, viviendas y edificios. Objetivos. Métodos de recogida. Características investigadas. Diferencia con la población registrada en los padrones municipales	12
Especialidad II: Ciencias Sociales y Económicas	1	Contabilidad Financiera	1	La relevancia de la información contable: regulación y marco conceptual	23
Especialidad II: Ciencias Sociales y Económicas	1	Contabilidad Financiera	2	El modelo contable: patrimonio, método contable. Resultado. Ciclo contable	26
Especialidad II: Ciencias Sociales y Económicas	1	Contabilidad Financiera	3	La información financiera y no financiera de las empresas. Las cuentas anuales	27
Especialidad II: Ciencias Sociales y Económicas	1	Contabilidad Financiera	4	Existencias: tipología, métodos de valoración y registro	23
Especialidad II: Ciencias Sociales y Económicas	1	Contabilidad Financiera	5	El Impuesto de Valor Añadido (IVA)	21
Especialidad II: Ciencias Sociales y Económicas	1	Contabilidad Financiera	6	Cuentas a cobrar y cuentas a pagar por la actividad. Cuentas relacionadas con el personal	23
Especialidad II: Ciencias Sociales y Económicas	1	Contabilidad Financiera	7	Activo no corriente: Inmovilizado material e inversiones inmobiliarias. Inmovilizado intangible	28
Especialidad II: Ciencias Sociales y Económicas	1	Contabilidad Financiera	8	Otras normas relacionadas con el inmovilizado. Arrendamientos. Subvenciones, donaciones y legados	23
Especialidad II: Ciencias Sociales y Económicas	1	Contabilidad Financiera	9	Activos financieros: derechos de cobro e inversiones financieras. Pasivos financieros: obligaciones corrientes de pago, préstamos, empréstitos y otras operaciones financieras	59
Especialidad II: Ciencias Sociales y Económicas	1	Contabilidad Financiera	10	Patrimonio neto y operaciones de capital	25
Especialidad II: Ciencias Sociales y Económicas	1	Contabilidad Financiera	11	Otras cuestiones de contabilidad financiera: provisiones y contingencias, impuesto sobre sociedades, errores y cambios en las estimaciones contables	24
Especialidad II: Ciencias Sociales y Económicas	1	Contabilidad Financiera	12	Cuentas anuales: regulación legal, informe anual, auditoría	15
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	1	El funcionamiento del mercado competitivo	26
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	2	Producción y costes	22
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	3	Las estructuras de los mercados	26
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	4	El mercado de bienes y servicios en una economía cerrada. El modelo renta-gasto. La determinación de la producción de equilibrio. Inversión igual al ahorro	20
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	5	El mercado de activos financieros y el dinero. La demanda de dinero. Conceptos y funciones del dinero. Teorías de la demanda de dinero. La oferta monetaria: las magnitudes monetarias básicas. El proceso de creación de dinero	22
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	6	El modelo IS-LM en una economía cerrada. La curva IS. La curva LM. Equilibrio conjunto de los dos mercados. Variaciones del equilibrio: una primera aproximación a la política económica	22
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	7	La demanda de consumo: principales aportaciones teóricas e implicaciones de política económica. La elección intertemporal. La teoría del ciclo vital. La teoría de la renta permanente. El consumo en condiciones de incertidumbre. La hipótesis del paseo aleatorio. El tirón de la gratificación inmediata	21
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	8	La demanda de inversión: principales aportaciones teóricas e implicaciones de política económica. La demanda de stock de capital y los flujos de inversión	25
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	9	El equilibrio conjunto a corto plazo: el modelo de OA y DA. La relación de DA. La relación de OA. El equilibrio a corto plazo. La dinámica de la producción hacia el nivel de la producción natural. El equilibrio a medio plazo	22
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	10	El desempleo. Conceptos básicos, indicadores y flujos de mercado. Tipos de desempleo: friccional, estructural y cíclico. La medición del desempleo. Análisis macroeconómico del mercado de trabajo. Principales explicaciones teóricas. La política de empleo	28
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	11	La relación de OA: perturbaciones de la OA y sus efectos a corto y medio plazo. Las variaciones del precio del petróleo. Cambios institucionales del mercado de trabajo. Cambios en la productividad media del trabajo	20
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	12	La inflación: medición, causas y efectos económicos. Principales explicaciones teóricas. La política anti-inflacionista y los costes de la desinflación	20
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	13	Inflación y desempleo en una economía cerrada: la curva de Phillips. La crítica monetarista a la curva de Phillips. La NAIRU. Las expectativas racionales y la curva de Phillips	16
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	14	El crecimiento económico	25
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	15	Los ciclos económicos	25
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	16	El equilibrio externo. La balanza de pagos. El mercado de divisas y el tipo de cambio. Sistemas de tipos de cambio: flexibles, fijos y mixtos. Teorías de ajuste de la Balanza de Pagos	30
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	17	La política monetaria	25
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	18	La política fiscal	25
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	19	La política mixta	25
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	20	El equilibrio en una economía abierta. El modelo Mundell-Fleming. El funcionamiento de la política fiscal y monetaria con tipos de cambio fijo y tipos de cambio flexible	24
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	21	[Tema no especificado]	0
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	22	La crisis financiera y las vinculaciones entre los mercados financieros y la economía real	30
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	23	La integración económica y monetaria europea (I). La Unión Europea: principales etapas del proceso de integración. El Pacto de estabilidad y crecimiento y el Tratado de Maastricht. El Sistema Monetario Europeo: el euro	28
Especialidad II: Ciencias Sociales y Económicas	1	Economía General	24	La integración económica y monetaria europea (II). La política monetaria y el Banco Central Europeo. El procedimiento del déficit excesivo. La crisis financiera y el "Procedimiento sobre los desequilibrios macroeconómicos" de los países	27
Especialidad II: Ciencias Sociales y Económicas	3	Sector Público y Sistema Fiscal	1	Los Presupuestos Generales del Estado. Concepto de presupuesto. Principios presupuestarios. Fases (elaboración, aprobación, ejecución y control). Estructuras de gasto (orgánica, económica y por programas). Estructuras de ingreso (orgánica y económica). Estabilidad presupuestaria	22
Especialidad II: Ciencias Sociales y Económicas	3	Sector Público y Sistema Fiscal	2	Los presupuestos autonómicos y locales	19
Especialidad II: Ciencias Sociales y Económicas	3	Sector Público y Sistema Fiscal	3	El sistema fiscal español. Principios generales. Tipos de tributos. Elementos básicos de los tributos. Clasificación de los impuestos (directos/indirectos, periódicos/instantáneos, progresivos/proporcionales). Domicilio fiscal. Métodos de determinación de la base imponible. Escalas progresivas de gravamen y mínimo exento. La armonización	21
Especialidad II: Ciencias Sociales y Económicas	3	Sector Público y Sistema Fiscal	4	El Impuesto sobre la Renta de las Personas Físicas. Naturaleza, objeto y ámbito de aplicación. Sujeción al impuesto. La Base Imponible. El proceso de liquidación. La base imponible y la base liquidable. Cuota líquida y diferencial. Tributación familiar. Regímenes especiales. Declaraciones, pagos a cuenta y obligaciones formales	21
Especialidad II: Ciencias Sociales y Económicas	3	Sector Público y Sistema Fiscal	5	El Impuesto sobre la Renta de no residentes. Ámbito de aplicación. Elementos personales. Sujeción al impuesto. Rentas obtenidas mediante establecimiento permanente y sin él. Gravamen especial sobre bienes inmuebles de entidades no residentes	19
Especialidad II: Ciencias Sociales y Económicas	3	Sector Público y Sistema Fiscal	6	El Impuesto sobre Sociedades. Naturaleza y ámbito de aplicación. Hecho imponible. Base imponible. Reducciones en la base imponible y compensación de bases imponibles negativas. La deuda tributaria. La gestión del impuesto. Regímenes tributarios especiales	24
Especialidad II: Ciencias Sociales y Económicas	3	Sector Público y Sistema Fiscal	7	El Impuesto sobre el Valor Añadido. Concepto, naturaleza y ámbito de aplicación. Hecho imponible. Sujeto pasivo. Base imponible. Tipos de gravamen. Deuda tributaria. La gestión del impuesto. Regímenes especiales	24
Especialidad II: Ciencias Sociales y Económicas	3	Sector Público y Sistema Fiscal	8	Impuestos Especiales. Los Impuestos Especiales de Fabricación. Concepto, naturaleza y ámbito de aplicación. Hecho imponible. Bases y tipos. Impuesto especial sobre el carbón. Impuesto especial sobre determinados medios de transporte	21
Especialidad II: Ciencias Sociales y Económicas	3	Sector Público y Sistema Fiscal	9	Imposición autonómica y local. Sistema fiscal autonómico: tributos cedidos y propios. Sistema impositivo local: Impuesto de Bienes Inmuebles, Impuesto sobre Actividades Económicas, Impuesto sobre Vehículos de Tracción Mecánica, Impuestos potestativos	29
Especialidad II: Ciencias Sociales y Económicas	4	Modelos Econométricos	1	Modelos causales y no causales. Datos	21
Especialidad II: Ciencias Sociales y Económicas	4	Modelos Econométricos	2	Análisis de regresión con datos de sección cruzada I	18
Especialidad II: Ciencias Sociales y Económicas	4	Modelos Econométricos	3	Análisis de regresión con datos de sección cruzada II	17
Especialidad II: Ciencias Sociales y Económicas	4	Modelos Econométricos	4	Análisis de regresión con datos de sección cruzada III	13
Especialidad II: Ciencias Sociales y Económicas	4	Modelos Econométricos	5	Análisis de regresión con datos de sección cruzada IV	12
Especialidad II: Ciencias Sociales y Económicas	4	Modelos Econométricos	6	Otras técnicas de estimación	10
Especialidad II: Ciencias Sociales y Económicas	4	Modelos Econométricos	7	Tests de especificación y selección de modelos	14
Especialidad II: Ciencias Sociales y Económicas	4	Modelos Econométricos	8	Endogeneidad y estimación con variables instrumentales	22
Especialidad II: Ciencias Sociales y Económicas	4	Modelos Econométricos	9	Modelos de panel lineales	15
Especialidad II: Ciencias Sociales y Económicas	4	Modelos Econométricos	10	Procesos estocásticos estacionarios	28
Especialidad II: Ciencias Sociales y Económicas	4	Modelos Econométricos	11	Modelos con tendencias	20
Especialidad II: Ciencias Sociales y Económicas	4	Modelos Econométricos	12	Modelos de series temporales multiecuacionales	13
Especialidad II: Ciencias Sociales y Económicas	4	Modelos Econométricos	13	Modelos de cointegración y de corrección del error	9
Especialidad II: Ciencias Sociales y Económicas	4	Modelos Econométricos	14	Ajuste estacional, desagregación temporal y calibrado de series temporales	24"""

# Build nested dicts
grupo_apt = defaultdict(list)          # grupo -> [(id, nombre), ...]
apt_tema  = defaultdict(list)          # (grupo, apt_nombre) -> [(t_id, tema, pages)]

for g, aid, aname, tid, tema, pages in SYLLABUS:
    if (aid, aname) not in grupo_apt[g]:
        grupo_apt[g].append((aid, aname))
    apt_tema[(g, aname)].append((tid, tema, pages))

grupos = list(grupo_apt.keys())

# ----------------------------------------------------------
# 3. Gamification helpers
# ----------------------------------------------------------
RANKS = [
    (0,    "🪙 Copper"), (200,  "🥉 Bronze"), (500,  "🥈 Silver"),
    (900,  "🥇 Gold"),   (1400, "💎 Platinum"), (2000, "🔥 Elite"),
    (2600, "🌟 Master"), (3000, "🏆 Legend"),
]
def get_rank(pages):
    for th, name in RANKS[::-1]:
        if pages >= th:
            return th, name
    return 0, RANKS[0][1]

# ----------------------------------------------------------
# 4. Sidebar progress
# ----------------------------------------------------------
st.set_page_config(page_title="100-Day Challenge")
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
# 6. Dynamic multi-topic registration
# ----------------------------------------------------------
st.markdown("---")
st.subheader(f"📖 Registro del día {dia} de {mes}")

# Retrieve existing record
record = data.get(clave, {})
topics = record.get("topics", [])

# How many topics today?
rows = st.number_input("¿Cuántos temas estudiaste?", min_value=0, max_value=10, value=max(1, len(topics)))

new_topics = []
total_day = 0

for idx in range(rows):
    cols = st.columns([2, 2, 2, 1])
    with cols[0]:
        grupo = st.selectbox("Grupo", grupos, key=f"g_{clave}_{idx}")
        aptitudes = [f"{aid} - {aname}" for aid, aname in grupo_apt[grupo]]
    with cols[1]:
        apt_sel = st.selectbox("Aptitud", aptitudes, key=f"a_{clave}_{idx}")
        aid, aname = apt_sel.split(" - ", 1)
        temas = [(tid, tema, pages) for tid, tema, pages in apt_tema[(grupo, aname)]]
    with cols[2]:
        tema_sel = st.selectbox("Tema", [f"{tid} - {tema} ({pages} p.)" for tid, tema, pages in temas], key=f"t_{clave}_{idx}")
        tid, rest = tema_sel.split(" - ", 1)
        tema, pages_str = rest.rsplit(" (", 1)
        pages_total = int(pages_str.split(" ")[0])
    with cols[3]:
        pages_read = st.number_input("Páginas", min_value=0, max_value=100, value=pages_total, key=f"p_{clave}_{idx}")
    new_topics.append({
        "grupo": grupo,
        "aptitud_id": int(aid),
        "aptitud_nombre": aname,
        "tema_id": int(tid),
        "tema_nombre": tema,
        "paginas": pages_read
    })
    total_day += pages_read

notas = st.text_area("Notas adicionales:", value=record.get("notas", ""))
color = st.color_picker("Color para el día", value=record.get("color", "#000000"))

if st.button("💾 Guardar registro"):
    data[clave] = {"topics": new_topics, "paginas": total_day, "notas": notas, "color": color}
    guardar_datos()
    new_total = total_pages + total_day
    old_th, _ = get_rank(total_pages)
    new_th, new_rank = get_rank(new_total)
    if new_th > old_th:
        st.balloons()
        st.success(f"🎉 ¡Subiste a {new_rank}!")
    st.rerun()

# ----------------------------------------------------------
# 7. Calendar visual
# ----------------------------------------------------------
st.markdown("---")
st.subheader("📆 Calendario visual")

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
        cols[i].markdown(
            f'<div style="color:{color}; font-weight:bold; font-size:18px;">{d}<br>{pag} pág.</div>',
            unsafe_allow_html=True
        )
