import streamlit as st
import login

login.generarLogin()
if 'usuario' in st.session_state:
    st.header('Re-:red[Training] the Model to add a new student')


    st.subheader("Press the botton to star the Re-Training")

    # Botón para re-entrenar el modelo
    if st.button("Re-Training Model"):
        st.write("Iniciando re-entrenamiento del modelo...")
        
        video_id = "KUCWDdxJUeA"
        video_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1"  #El video se mutea por defecto
        #video_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1"
        
        # Mostrar el video usando iframe
        st.components.v1.html(f"""
            <iframe width="560" height="315" src="{video_url}" frameborder="0" allowfullscreen></iframe>
        """, height=400)
