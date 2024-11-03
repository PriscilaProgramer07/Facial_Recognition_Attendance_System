import streamlit as st
import login as login
from PIL import Image

st.header('LIST of :orange[Students]')
login.generarLogin()
if 'usuario' in st.session_state:
    st.subheader('Student List of Attendance')

    # Cargar la imagen
    image = Image.open(r"C:\Users\Angel\Documents\Programacion\HPC\Streamlit\Web_Page_Login\Si_tuviera_uno1.jpg")
    
    # Mostrar la imagen en la aplicación
    st.image(image, caption="Imagen de Reconocimiento Facial", use_column_width=True)


