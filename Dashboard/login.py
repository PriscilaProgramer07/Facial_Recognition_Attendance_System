import streamlit as st
import pandas as pd
import bcrypt

# URL to the raw GitHub CSV file
CSV_URL = 'https://raw.githubusercontent.com/PriscilaProgramer07/Facial_Recognition_Attendance_System/refs/heads/main/Dashboard/usuarios.csv'

# Validación simple de usuario y clave con un archivo csv desde un enlace
def validarUsuario(usuario, clave):    
    """Permite la validación de usuario y clave desde un enlace de GitHub

    Args:
        usuario (str): usuario a validar
        clave (str): clave del usuario

    Returns:
        bool: True usuario valido, False usuario invalido
    """    
    try:
        dfusuarios = pd.read_csv(CSV_URL)
        # Filtra el usuario en el dataframe
        user_data = dfusuarios[dfusuarios['usuario'] == usuario]
        if not user_data.empty:
            hashed_password = user_data['clave'].values[0].encode('utf-8')
            # Verifica la contraseña
            if bcrypt.checkpw(clave.encode('utf-8'), hashed_password):
                return True
    except Exception as e:
        st.error(f"Error loading user data: {str(e)}")
    return False

def generarMenu(usuario):
    """Genera el menú dependiendo del usuario

    Args:
        usuario (str): usuario utilizado para generar el menú
    """        
    with st.sidebar:
        # Cargamos la tabla de usuarios desde el enlace
        try:
            dfusuarios = pd.read_csv(CSV_URL)
            # Filtramos la tabla de usuarios
            dfUsuario = dfusuarios[(dfusuarios['usuario'] == usuario)]
            # Cargamos el nombre del usuario
            nombre = dfUsuario['nombre'].values[0]
            # Mostramos el nombre del usuario
            st.write(f"Hello **:blue-background[{nombre}]** ")
            # Mostramos los enlaces de páginas
            st.page_link("inicio.py", label="Student List", icon=":material/book:")
            st.subheader("Another Things")
            st.page_link("pages/pagina1.py", label="Attendance", icon=":material/camera:")
            st.page_link("pages/pagina3.py", label="Attendance Report", icon=":material/assignment:")
            st.page_link("pages/pagina2.py", label="New Student", icon=":material/person_add:")
            st.page_link("pages/pagina4.py", label="About", icon=":material/person_add:")

            # Botón para cerrar la sesión
            btnSalir = st.button("Log out")
            if btnSalir:
                st.session_state.clear()
                # Luego de borrar el Session State reiniciamos la app para mostrar la opción de usuario y clave
                st.rerun()
        except Exception as e:
            st.error(f"Error loading user data: {str(e)}")

def generarLogin():
    """Genera la ventana de login o muestra el menú si el login es valido
    """    
    # Validamos si el usuario ya fue ingresado    
    if 'usuario' in st.session_state:
        generarMenu(st.session_state['usuario'])  # Si ya hay usuario cargamos el menu        
    else: 
        # Cargamos el formulario de login       
        with st.form('frmLogin'):
            parUsuario = st.text_input('Usuario')
            parPassword = st.text_input('Password', type='password')
            btnLogin = st.form_submit_button('Ingresar', type='primary')
            if btnLogin:
                if validarUsuario(parUsuario, parPassword):
                    st.session_state['usuario'] = parUsuario
                    # Si el usuario es correcto reiniciamos la app para que se cargue el menú
                    st.rerun()
                else:
                    # Si el usuario es invalido, mostramos el mensaje de error
                    st.error("Usuario o clave inválidos", icon=":material/gpp_maybe:")