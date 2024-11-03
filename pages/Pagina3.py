import streamlit as st
import login


login.generarLogin()
if 'usuario' in st.session_state:
    st.header('About :green[US]')
    st.subheader('This GUI is only posible thanks to the Analyst Team')
    st.write('Angel Campos')
    st.write('Angel Sansores')