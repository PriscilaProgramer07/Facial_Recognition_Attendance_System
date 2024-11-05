import streamlit as st
import login

# Generar la sesión de inicio de sesión
login.generarLogin()

# Verificar si el usuario está autenticado
if 'usuario' in st.session_state:
    # Título de la página
    st.title("About Us")

    # Presentación de los miembros del equipo
    st.header("Meet the Team")

    team_members = [
        {"name": "Angel Sansores", "role": "Data Analyst"},
        {"name": "Angel Campos", "role": "Data Analyst"},
        {"name": "Julio Dzul", "role": "Data Engineer"},
        {"name": "Priscila Tzuc", "role": "Data Engineer"},
        {"name": "Luis Martinez", "role": "Data Scientist"},
        {"name": "Antonio Ruis", "role": "Data Scientist"}
    ]

    for member in team_members:
        st.subheader(f"{member['name']}")
        st.text(f"Role: {member['role']}")
        st.markdown("---")  # Separador visual
else:
    st.warning("Please log in to view the 'About Us' page.")
