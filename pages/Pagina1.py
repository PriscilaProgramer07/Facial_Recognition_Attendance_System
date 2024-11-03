import streamlit as st
import login
import cv2
import time


login.generarLogin()
if 'usuario' in st.session_state:
    st.header('Face :blue[Recognition] to pass list')

    # Título de la aplicación
    st.subheader("Press the :blue[botton] to start the recognition")

    if st.button("Start Recognition"):
        st.write("Encendiendo camara...")

        # Iniciar captura de video
        cap = cv2.VideoCapture(0)  # 0 selecciona la cámara predeterminada

        start_time = time.time()
        video_frame = st.image([])  # Lugar donde se mostrará el video

        # Mostrar la cámara durante 5 segundos
        while time.time() - start_time < 5:
            ret, frame = cap.read()  # Leer un frame de la cámara
            if not ret:
                st.write("Error al acceder a la cámara.")
                break
            
            # Convertir el frame de BGR (OpenCV) a RGB (Streamlit)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Actualizar el frame en la aplicación
            video_frame.image(frame, channels="RGB", caption="Reconocimiento en Proceso")

        # Liberar la cámara después de 5 segundos
        cap.release()
        
        # Mostrar mensaje de reconocimiento
        st.success("Estudiante reconocido")