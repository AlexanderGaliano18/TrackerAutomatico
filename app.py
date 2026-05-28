import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página (Siempre debe ser la primera línea de Streamlit)
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

# --- DATA POR DEFECTO ---
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

# 3. Componente de carga de archivos en la barra lateral
st.sidebar.header("📂 Configuración de Datos")
archivo_subido = st.sidebar.file_uploader("Sube tu archivo de mercado (.csv)", type=["csv"])

# Decidir qué conjunto de datos utilizar
if archivo_subido is not None:
    df = pd.read_csv(archivo_subido)
    st.sidebar.success("¡Archivo cargado correctamente!")
else:
    df = cargar_data_defecto()
    st.sidebar.info("Mostrando datos de prueba. Sube tu propio CSV para sobreescribirlos.")

# Asegurar que las columnas requeridas existan antes de procesar
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
    
    # --- SECCIÓN DE GRÁFICOS INTERACTIVOS ---
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
            
    # --- ZONA DE EXPLORACIÓN Y ASESORÍA ---
    st.divider()
    st.markdown('<div class="main-title">🚘 Zona de Exploración y Asesoría</div>', unsafe_allow_html=True)

    col_3d, col_chat = st.columns([1.2, 1])

    with col_3d:
        st.subheader("Visor 3D del Vehículo")
        st.markdown("Explora el diseño exterior e interior del modelo seleccionado.")
        
        # Iframe con modelo funcional activo para evitar errores de carga
        st.components.v1.html(
            '''
            <div class="sketchfab-embed-wrapper">
                <iframe title="Nissan 3D Model" 
                    frameborder="0" 
                    allowfullscreen 
                    mozallowfullscreen="true" 
                    webkitallowfullscreen="true" 
                    allow="autoplay; fullscreen; xr-spatial-tracking" 
                    src="https://sketchfab.com/models/e2b7988d402a4af6af9cf51144daa798/embed?autostart=1&ui_theme=dark" 
                    height="450" 
                    width="100%"> 
                </iframe>
            </div>
            ''',
            height=470,
        )

    with col_chat:
        st.subheader("💬 Asistente Automotriz AI")
        st.markdown("Pregúntame sobre aciertos, desaciertos o comparativas.")
        
        mensaje_usuario = st.chat_input("Ej: ¿Por qué elegir un Swift sobre un Accent?")
        
        with st.container(height=350):
            with st.chat_message("assistant"):
                st.write("¡Hola! Soy tu asistente de datos. Pronto estaré conectado a tu base de datos para darte recomendaciones exactas. 🛠️")
                
            if mensaje_usuario:
                with st.chat_message("user"):
                    st.write(mensaje_usuario)
                
                with st.chat_message("assistant"):
                    st.write(f"Has preguntado: '{mensaje_usuario}'.")
                    st.info("💡 Modo demostración: Necesitamos conectar una API para que empiece a analizar y responder con datos reales.")

else:
    st.error(f"El dataset no tiene las columnas requeridas: {', '.join(columnas_requeridas)}")
