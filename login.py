# login.py
import streamlit as st
from db import get_connection
from streamlit_cookies_controller import CookieController

# Instancia para manejo de cookies
controller = CookieController()

def validarUsuario(usuario, clave):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM usuarios WHERE usuario = %s AND clave = %s"
    cursor.execute(query, (usuario, clave))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user is not None

def getUsuario(usuario):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM usuarios WHERE usuario = %s"
    cursor.execute(query, (usuario,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user

def getPaginas():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM rol_paginas"
    cursor.execute(query)
    paginas = cursor.fetchall()
    cursor.close()
    connection.close()
    return paginas

def generarMenu(usuario):
    with st.sidebar:
        st.markdown(
            """
            <style>
            .stButton>button, .stFormSubmitButton>button {
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                color: #FFFFFF;
                background-color: #262730;
                border: none;
                width: 100%;
                margin-top: 1rem;
                cursor: pointer;
            }
            .stButton>button:hover, .stFormSubmitButton>button:hover {
                background-color: #444656;
                color: #fdfaf4 !important;
            }
            .stButton>button:active, .stFormSubmitButton>button:active {
                background-color: #b2aba4 !important;
                color: #262730 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    with st.sidebar:
        user = getUsuario(usuario)
        if user:
            nombre = user['nombre']
            rol = user['rol']
            st.write(f"Hola **:blue-background[{nombre}]** ")
            st.caption(f"Rol: {rol}")
            st.page_link("inicio.py", label="Inicio", icon=":material/home:")
            st.subheader("Tableros")
            if rol in ['ventas','admin','comercial']:
                st.page_link("pages/paginaVentas.py", label="Ventas", icon=":material/sell:")
            if rol in ['compras','admin','comercial']:
                st.page_link("pages/paginaCompras.py", label="Compras", icon=":material/shopping_cart:")
            if rol in ['personal','admin','compras']:
                st.page_link("pages/paginaPersonal.py", label="Personal", icon=":material/group:")
            if rol in ['contabilidad','admin']:
                st.page_link("pages/paginaContabilidad.py", label="Contabilidad", icon=":material/payments:")
            btnSalir = st.button("Salir")
            if btnSalir:
                st.session_state.clear()
                st.rerun()

def generarMenuRoles(usuario):
    with st.sidebar:
        st.markdown(
            """
            <style>
            .stButton>button, .stFormSubmitButton>button {
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                color: #FFFFFF;
                background-color: #262730;
                border: none;
                width: 100%;
                margin-top: 1rem;
                cursor: pointer;
            }
            .stButton>button:hover, .stFormSubmitButton>button:hover {
                background-color: #444656;
                color: #fdfaf4 !important;
            }
            .stButton>button:active, .stFormSubmitButton>button:active {
                background-color: #b2aba4 !important;
                color: #262730 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    with st.sidebar:
        user = getUsuario(usuario)
        paginas = getPaginas()
        if user:
            nombre = user['nombre']
            rol = user['rol']
            
            cols = st.columns([1, 8, 1])  # Ampliamos la columna central
            with cols[1]:
                st.image("resources/logo.png", width=250)

            st.write(f"Hola **:blue-background[{nombre}]** ")
            st.caption(f"Rol: {rol}")
            st.markdown("---")
            st.subheader("Sitios")
            if st.secrets["ocultarOpciones"] == "True":
                if rol != 'admin':
                    paginas = [p for p in paginas if rol in p['roles'].split('|')]
                for row in paginas:
                    icono = row['icono']
                    st.page_link(row['pagina'], label=row['nombre'], icon=f":material/{icono}:")
            else:
                for row in paginas:
                    deshabilitarOpcion = True
                    if rol in row["roles"].split('|') or rol == "admin":
                        deshabilitarOpcion = False
                    icono = row['icono']
                    st.page_link(row['pagina'], label=row['nombre'], icon=f":material/{icono}:", disabled=deshabilitarOpcion)
            btnSalir = st.button("Salir")
            if btnSalir:
                st.session_state.clear()
                controller.remove('usuario')
                st.rerun()

def validarPagina(pagina, usuario):
    user = getUsuario(usuario)
    if not user:
        return False
    rol = user['rol']
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM rol_paginas WHERE pagina LIKE %s"
    cursor.execute(query, (f"%{pagina}%",))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    if row:
        if rol in row['roles'].split('|') or rol == "admin" or st.secrets["tipoPermiso"] == "rol":
            return True
        else:
            return False
    else:
        return False

def generarLogin(archivo):
    usuario = controller.get('usuario')
    if usuario:
        st.session_state['usuario'] = usuario

    estilos = """
    <style>
    .block-container {
        width: 400px;
        max-width: 90%;
        margin: 120px auto;     
        background-color: #fdfaf4;
        padding: 40px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .block-container h2, .block-container h1 {
        text-align: center;
    }
    .stTextInput>div>div>input {
        background-color: #F2F2F2 !important;
        border: none !important;      
        border-radius: 0 !important;
        padding: 10px !important;
        font-size: 12px !important;
        width: 100% !important;
        text-align: left !important;
        box-sizing: border-box !important;
        color: #333 !important;
    }
    .stTextInput>div>div>input::placeholder {
        color: #999 !important;
        text-align: left !important;
        font-size: 16px !important;
    }
    .stTextInput>div>div>input:focus {
        outline: none !important;
        border: none !important;
        box-shadow: none !important;
    }
    .stTextInput [data-testid="stPasswordVisibleButton"] {
        display: none !important;
    }
    .stButton>button, .stFormSubmitButton>button {
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
        font-weight: bold;
        color: #FFFFFF;
        background-color: #262730;
        border: none;
        width: 100%;
        margin-top: 1rem;
        cursor: pointer;
    }
    .stButton>button:hover, .stFormSubmitButton>button:hover {
        background-color: #444656;
        color: #fdfaf4 !important;
    }
    .stButton>button:active, .stFormSubmitButton>button:active {
        background-color: #b2aba4 !important;
        color: #262730 !important;
    }
    </style>
    """
    
    if 'usuario' in st.session_state:
        user = getUsuario(st.session_state['usuario'])
        if user and user['clave'] == "optisalud" and not st.session_state.get("password_updated", False):
            st.markdown(estilos, unsafe_allow_html=True)
            st.info("Debe cambiar su contraseña por motivos de seguridad.")
            with st.container():
                new_password = st.text_input("Nueva contraseña", type="password")
                new_password_confirm = st.text_input("Confirmar nueva contraseña", type="password")
                if st.button("Actualizar contraseña"):
                    if new_password == "" or new_password_confirm == "":
                        st.error("La contraseña no puede estar vacía")
                    elif new_password != new_password_confirm:
                        st.error("Las contraseñas no coinciden")
                    else:
                        connection = get_connection()
                        cursor = connection.cursor()
                        query = "UPDATE usuarios SET clave = %s WHERE usuario = %s"
                        cursor.execute(query, (new_password, st.session_state['usuario']))
                        connection.commit()
                        cursor.close()
                        connection.close()
                        st.success("Contraseña actualizada correctamente")
                        st.session_state["password_updated"] = True
                        st.rerun()
            st.stop()
        else:
            if st.secrets["tipoPermiso"] == "rolpagina":
                generarMenuRoles(st.session_state['usuario'])
            else:
                generarMenu(st.session_state['usuario'])
            if not validarPagina(archivo, st.session_state['usuario']):
                st.error(f"No tiene permisos para acceder a esta página {archivo}", icon=":material/gpp_maybe:")
                st.stop()
    else:
        st.markdown(estilos, unsafe_allow_html=True)
        with st.form('frmLogin'):
            st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
            st.image("resources/logo.png", width=300)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<h1 style='text-align: center; font-size:30px; color: #262730;'>Iniciar sesión</h1>", unsafe_allow_html=True)
            parUsuario = st.text_input('Usuario', placeholder="empleado@optisalud.co")
            parPassword = st.text_input('Password', type='password', placeholder="********")
            btnLogin = st.form_submit_button('Ingresar', type='primary')
            if btnLogin:
                if validarUsuario(parUsuario, parPassword):
                    st.session_state['usuario'] = parUsuario
                    controller.set('usuario', parUsuario)
                    st.rerun()
                else:
                    st.error("Usuario o clave inválidos", icon=":material/gpp_maybe:")
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    generarLogin(__file__.split("\\")[-1])
