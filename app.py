import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai  # <-- Librería de IA

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

# --- DICCIONARIO DE MODELOS 3D ACTUALIZADO ---
MAPA_MODELOS_3D = {
    "Versa": "https://sketchfab.com/models/18af87c9490e4acb80a46b70ca8d86ed/embed?autostart=1&ui_theme=dark",
    "Swift": "https://sketchfab.com/models/218c3c0c6afd4d0eb343bd50d8868fd0/embed?autostart=1&ui_theme=dark",
    "Accent": "https://sketchfab.com/models/cec6b04b06724f1088129c1054ccb1ec/embed?autostart=1&ui_theme=dark"
}
URL_POR_DEFECTO = "https://sketchfab.com/models/18af87c9490e4acb80a46b70ca8d86ed/embed?autostart=1&ui_theme=dark"

# --- DATA POR DEFECTO ---
@st.cache_data
def cargar_data_defecto():
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

if archivo_subido is not None:
    df = pd.read_csv(archivo_subido)
    st.sidebar.success("¡Archivo cargado correctamente!")
else:
    df = cargar_data_defecto()
    st.sidebar.info("Mostrando datos de prueba. Sube tu propio CSV para sobreescribirlos.")

columnas_requeridas = ["Marca", "Modelo", "Año", "Kilometraje", "Precio_USD"]

if all(col in df.columns for col in columnas_requeridas):
    
    st.sidebar.divider()
    st.sidebar.header("🔍 Filtros")
    
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
        st.subheader("Visor 3D Dinámico")
        
        if not df_final.empty:
            modelos_filtrados = df_final["Modelo"].unique()
            
            modelo_seleccionado_3d = st.selectbox(
                "🔍 Selecciona el vehículo específico para inspeccionar en 3D:",
                options=modelos_filtrados
            )
            
            url_gltf = MAPA_MODELOS_3D.get(modelo_seleccionado_3d, URL_POR_DEFECTO)
            
            st.components.v1.html(
                f'''
                <div class="sketchfab-embed-wrapper">
                    <iframe title="Visor 3D - {modelo_seleccionado_3d}" 
                        frameborder="0" 
                        allowfullscreen 
                        mozallowfullscreen="true" 
                        webkitallowfullscreen="true" 
                        allow="autoplay; fullscreen; xr-spatial-tracking" 
                        src="{url_gltf}" 
                        height="420" 
                        width="100%"> 
                    </iframe>
                </div>
                ''',
                height=440,
            )
        else:
            st.info("Aplica filtros válidos en la barra lateral para activar el visor 3D.")

    with col_chat:
        st.subheader("💬 Asistente Automotriz AI")
        st.markdown("Pregúntame sobre aciertos, desaciertos o comparativas.")
        
        # --- LECTURA SEGURA DE LA API KEY DESDE LA BÓVEDA ---
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except KeyError:
            st.warning("⚠️ Falta configurar GEMINI_API_KEY en los Secrets de Streamlit.")
            api_key = None
        
        if "mensajes" not in st.session_state:
            st.session_state.mensajes = [{"role": "assistant", "content": "¡Hola! Ya estoy conectado a los datos. Pregúntame qué auto te conviene más. 🛠️"}]
            
        with st.container(height=300):
            for msg in st.session_state.mensajes:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
                    
        mensaje_usuario = st.chat_input("Ej: ¿Qué carro tiene el mejor precio y menor kilometraje?")
        
        if mensaje_usuario:
            st.session_state.mensajes.append({"role": "user", "content": mensaje_usuario})
            with st.chat_message("user"):
                st.write(mensaje_usuario)
                
            with st.chat_message("assistant"):
                if not api_key:
                    st.error("⚠️ No se detectó la llave API. Revisa los Secrets en la nube.")
                else:
                    try:
                        genai.configure(api_key=api_key)
                      # PON ESTA LÍNEA EN SU LUGAR:
modelo = genai.GenerativeModel('gemini-pro')
                        
                        contexto_tabla = df_final.head(50).to_string(index=False)
                        prompt_sistema = f"""
                        Eres un experto asesor automotriz de segunda mano.
                        Responde a la pregunta del usuario basándote ESTRICTAMENTE en esta base de datos de mercado:
                        
                        {contexto_tabla}
                        
                        Pregunta del usuario: {mensaje_usuario}
                        Responde de forma concisa, analítica y amigable.
                        """
                        
                        respuesta = modelo.generate_content(prompt_sistema)
                        texto_ia = respuesta.text
                        
                        st.write(texto_ia)
                        st.session_state.mensajes.append({"role": "assistant", "content": texto_ia})
                        
                    except Exception as e:
                        st.error(f"Error de conexión: Verifica tu API Key o conexión a internet. Detalles: {e}")

else:
    st.error(f"El dataset no tiene las columnas requeridas: {', '.join(columnas_requeridas)}")
