import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página (Debe ser la primera línea de Streamlit)
st.set_page_config(
    page_title="Tracker de Mercado Automotriz", 
    page_icon="🚗", 
    layout="wide"
)

# Estilos personalizados simples para mejorar la interfaz
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

# 3. Componente de carga de archivos en el panel lateral
st.sidebar.header("📂 Configuración y Filtros")
archivo_subido = st.sidebar.file_uploader("Sube tu archivo de mercado (.csv)", type=["csv"])

if archivo_subido is not None:
    # Leer el dataset cargado por el usuario
    df = pd.read_csv(archivo_subido)
    
    # Asegurar que las columnas requeridas existan
    columnas_requeridas = ["Marca", "Modelo", "Año", "Kilometraje", "Precio_USD"]
    if all(col in df.columns for col in columnas_requeridas):
        
        # --- FILTROS DINÁMICOS EN LA BARRA LATERAL ---
        # Filtro de Marca
        marcas_disponibles = df["Marca"].unique()
        marcas_seleccionadas = st.sidebar.multiselect(
            "Selecciona la(s) Marca(s):", 
            options=marcas_disponibles, 
            default=marcas_disponibles
        )
        
        # Filtrar por marca primero para actualizar los modelos disponibles
        df_filtrado_marca = df[df["Marca"].isin(marcas_seleccionadas)]
        
        # Filtro de Modelo
        modelos_disponibles = df_filtrado_marca["Modelo"].unique()
        modelos_seleccionados = st.sidebar.multiselect(
            "Selecciona el/los Modelo(s):", 
            options=modelos_disponibles, 
            default=modelos_disponibles
        )
        
        # Dataframe final con todos los filtros aplicados
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
        
        # --- SECCIÓN DE GRÁFICOS INTERACTIVOS ---
        if not df_final.empty:
            st.subheader("📈 Análisis de Distribución y Depreciación")
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico 1: Caja y Bigotes para evaluar dispersión de precios por año
                fig_box = px.box(
                    df_final, 
                    x="Año", 
                    y="Precio_USD", 
                    color="Modelo",
                    points="all",
                    title="Distribución de Precios por Año de Fabricación",
                    labels={"Precio_USD": "Precio (USD)", "Año": "Año de Fabricación"}
                )
                fig_box.update_layout(legend_position="bottom")
                st.plotly_chart(fig_box, use_container_width=True)
                
            with col2:
                # Gráfico 2: Dispersión para evaluar depreciación por kilometraje
                fig_scatter = px.scatter(
                    df_final, 
                    x="Kilometraje", 
                    y="Precio_USD", 
                    color="Modelo",
                    size="Precio_USD",
                    hover_data=["Año"],
                    title="Relación Precio vs. Kilometraje",
                    labels={"Precio_USD": "Precio (USD)", "Kilometraje": "Kilometraje Recorrido"}
                )
                fig_scatter.update_layout(legend_position="bottom")
                st.plotly_chart(fig_scatter, use_container_width=True)
                
            st.divider()
            
            # --- VISTA PREVIA DE LA DATA EN TABLA ---
            st.subheader("📋 Datos Detallados")
            with st.expander("Ver tabla completa de registros filtrados"):
                st.dataframe(df_final.sort_values(by="Precio_USD", ascending=True), use_container_width=True)
                
    else:
        st.error(f"El archivo CSV no contiene las columnas requeridas: {', '.join(columnas_requeridas)}")
else:
    # Estado inicial cuando no se ha subido ningún archivo
    st.info("👋 ¡Bienvenido! Para comenzar, arrastra o selecciona tu archivo `autos_prueba.csv` en la barra lateral izquierda.")
    
    # Breve guía visual de qué columnas debe tener
    st.markdown("""
    ### Estructura requerida para el archivo CSV:
    Asegúrate de que tu archivo contenga exactamente las siguientes columnas:
    * `Marca` (Ej. Nissan, Suzuki, Hyundai)
    * `Modelo` (Ej. Versa, Swift, Accent)
    * `Año` (Año de fabricación)
    * `Kilometraje` (Kilómetros recorridos)
    * `Precio_USD` (Valor de venta en dólares)
    """)
