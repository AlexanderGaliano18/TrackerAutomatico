import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(
    page_title="Tracker de Mercado Automotriz", 
    page_icon="🚗", 
    layout="wide"
)

# Estilos personalizados
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #1E1E1E; }
    .subtitle { font-size: 16px; color: #555555; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# 2. Encabezado principal
st.markdown('<div class="main-title">🚗 Tracker de Mercado Automotriz</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Fase 1: Análisis y Visualización Estática de Depreciación de Vehículos</div>', unsafe_allow_html=True)
st.divider()

# --- NUEVA LÓGICA: DATA POR DEFECTO ---
@st.cache_data
def cargar_data_defecto():
    """Crea un DataFrame de prueba si el usuario no sube nada"""
    data = {
        "Marca": ["Nissan", "Nissan", "Suzuki", "Suzuki", "Hyundai", "Hyundai"],
        "Modelo": ["Versa", "Versa", "Swift", "Swift", "Accent", "Accent"],
        "Año": [2018, 2021, 2019, 2022, 2017, 2020],
        "Kilometraje": [65000, 25000, 50000, 15000, 80000, 35000],
        "Precio_USD": [10500, 14000, 11000, 13500, 9500, 12800]
    }
    return pd.DataFrame(data)

# 3. Componente de carga de archivos
st.sidebar.header("📂 Configuración de Datos")
archivo_subido = st.sidebar.file_uploader("Sube tu archivo de mercado (.csv)", type=["csv"])

# Decidir qué data usar: la subida o la por defecto
if archivo_subido is not None:
    df = pd.read_csv(archivo_subido)
    st.sidebar.success("¡Archivo cargado correctamente!")
else:
    df = cargar_data_defecto()
    st.sidebar.info("Mostrando datos de prueba. Sube tu propio CSV para sobreescribirlos.")

# Asegurar que las columnas requeridas existan
columnas_requeridas = ["Marca", "Modelo", "Año", "Kilometraje", "Precio_USD"]

if all(col in df.columns for col in columnas_requeridas):
    
    st.sidebar.divider()
    st.sidebar.header("🔍 Filtros")
    
    # --- FILTROS DINÁMICOS ---
    marcas_disponibles = df["Marca"].unique()
    marcas_seleccionadas = st.sidebar.multiselect(
        "Selecciona la(s) Marca(s):", 
        options=marcas_disponibles, 
        default=marcas_disponibles
    )
    
    df_filtrado_marca = df[df["Marca"].isin(marcas_seleccionadas)]
    
    modelos_disponibles = df_filtrado_marca["Modelo"].unique()
    modelos_seleccionados = st.sidebar.multiselect(
        "Selecciona el/los Modelo(s):", 
        options=modelos_disponibles, 
        default=modelos_disponibles
    )
    
    df_final = df_filtrado_marca[df_filtrado_marca["Modelo"].isin(modelos_seleccionados)]
    
    # --- SECCIÓN DE MÉTRICAS CLAVE ---
    st.subheader("📊 Indicadores Clave del Mercado")
    m1, m2, m3 = st.columns(3)
    
    if not df_final.empty:
        total_autos = len(df_final)
        precio_promedio = df_final["Precio_USD"].mean()
        km_promedio = df_final["Kilometraje"].mean()
        
        m1.metric("Autos en Análisis", f"{total_autos} u.")
        m2.metric("Precio Promedio", f"${precio_promedio:,.2f} USD")
        m3.metric("Kilometraje Promedio", f"{km_promedio:,.0f} km")
    else:
        st.warning("No hay datos que coincidan con los filtros seleccionados.")
        
    st.divider()
    
    # --- SECCIÓN DE GRÁFICOS INTERACTIVOS (Bugs corregidos) ---
    if not df_final.empty:
        st.subheader("📈 Análisis de Distribución y Depreciación")
        col1, col2 = st.columns(2)
        
        with col1:
            fig_box = px.box(
                df_final, 
                x="Año", 
                y="Precio_USD", 
                color="Modelo",
                points="all",
                title="Distribución de Precios por Año",
                labels={"Precio_USD": "Precio (USD)", "Año": "Año"}
            )
            # Solución al error: Usamos la sintaxis correcta para la leyenda horizontal
            fig_box.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
            st.plotly_chart(fig_box, use_container_width=True)
            
        with col2:
            fig_scatter = px.scatter(
                df_final, 
                x="Kilometraje", 
                y="Precio_USD", 
                color="Modelo",
                size="Precio_USD",
                hover_data=["Año"],
                title="Relación Precio vs. Kilometraje",
                labels={"Precio_USD": "Precio (USD)", "Kilometraje": "Kilometraje"}
            )
            fig_scatter.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        st.divider()
        
        # --- VISTA PREVIA DE LA DATA ---
        st.subheader("📋 Datos Detallados")
        with st.expander("Ver tabla completa de registros"):
            st.dataframe(df_final.sort_values(by="Precio_USD", ascending=True), use_container_width=True)
            
else:
    st.error(f"El dataset no tiene las columnas requeridas: {', '.join(columnas_requeridas)}")
