import streamlit as st
import streamlit.components.v1 as components
import login
from db import get_connection  # Asegúrate de tener configurado este módulo para conectarte a MySQL

# Configura el layout en modo wide
st.set_page_config(layout="wide")

archivo = __file__.split("\\")[-1]
login.generarLogin(archivo)

if 'usuario' in st.session_state:
    # Título principal
    st.markdown(
        "<h1 style='font-weight: bold; color: #262730;'>INFORME DE VENTAS</h1>",
        unsafe_allow_html=True
    )
    
    # Consultamos la fecha de la tabla infoTableros para el concepto "Informe Ventas"
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT fecha FROM infoTableros WHERE concepto = %s ORDER BY fecha DESC LIMIT 1"
        cursor.execute(query, ("Informe Ventas",))
        result = cursor.fetchone()
        if result:
            # result[0] es un objeto date; se formatea a DD/MM/AAAA
            fecha_str = result[0].strftime("%d/%m/%Y")
        else:
            fecha_str = "Fecha no disponible"
    except Exception as e:
        fecha_str = "Error al obtener la fecha"
    finally:
        cursor.close()
        connection.close()
    
    # Subtítulo con la fecha obtenida
    st.markdown(
        f"<h5 style='font-weight: bold;'>La información se encuentra actualizada hasta: <span style='color: green;'>{fecha_str}</span></h5>",
        unsafe_allow_html=True
    )
    
    # URL de tu reporte de PowerBI
    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGUyMWI3MDUtOTIxMC00YzQwLTkyM2ItNmU4M2UzMmMyODZlIiwidCI6ImZjMDA1NDdhLTI0YmItNGU0Zi05ZDYxLTczZmNhNWViOWRmMyIsImMiOjR9"
    
    # Código del iframe para incrustar el reporte
    iframe_code = f"""
        <iframe width="100%" height="800" src="{powerbi_url}" frameborder="0" allowFullScreen="true"></iframe>
    """
    
    # Muestra el reporte incrustado en la app
    components.html(iframe_code, height=800)
