import streamlit as st
import login

# Generar la sesión de inicio de sesión
login.generarLogin()

# Verificar si el usuario está autenticado
if 'usuario' in st.session_state:
    # Título de la página
    st.title("About :violet[Us]")

    # Presentación de los miembros del equipo
    st.header("Meet the Team")

    # Estilos personalizados en CSS
    st.markdown("""
        <style>
        .profile-card {
            border: 1px solid #d1d1d1;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
        }
        .profile-header {
            font-size: 30px;
            font-weight: bold;
        }
        .profile-subtitle {
            font-size: 22px;
            color: #b89e6b;
            margin-bottom: 10px;
        }
        .separator {
            margin: 20px 0;
            border-top: 1px solid #e0e0e0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Información de los miembros del equipo
    team_members = [
        {
            "name": "Angel Sansores",
            "role": "Data Analyst",
            "description": "Hello! My name is Angel, a 21-year-old passionate data engineering student currently working as a Data Analyst on this project. I enjoy exploring information and extracting valuable insights from data sets. I continually improve my skills in analysis, programming, data manipulation, and visualization."
        },
        {
            "name": "Priscila Tzuc",
            "role": "Data Engineer",
            "description": "Data engineering student at the Polytechnic University of Yucatan, with skills and knowledge in data analysis, programming, and database management; as well as analytical skills, attention to detail, and constant curiosity to address complex problems and find effective solutions."
        },
        {
            "name": "Antonio Ruíz",
            "role": "Data Scientist",
            "description": "Hello, my name is Antonio Ruiz Nolasco. I am a dedicated data engineering enthusiast with hands-on experience in data analysis, machine learning, and project management. Skilled in tools like Power BI and Google Colab, I have worked on projects ranging from social network analysis to facial recognition systems. I’m passionate about leveraging data to drive impactful solutions and eager to bring my expertise to innovative teams as I advance in my data engineering career."
        },
        {
            "name": "Luis Martinez",
            "role": "Data Scientist",
            "description": "Data Engineering student with a strong passion for data analysis and interpretation, with a specialization in Data Science. Ability to work with large volumes of data and extract valuable information through analysis and visualization techniques. Knowledge of programming and database management. Looking for an opportunity to apply my skills and grow in the field of data engineering."
        },
        {
            "name": "Angel Campos",
            "role": "Data Analyst",
            "description": "Hello! I'm Angel Campos, a 25 years old student of Data Engineering career. Now I am part of the Data Analysis Team for this project. I find the visualization, interpretation and the discovery of patterns entertaining. In my free time I improve my skills in programming, visualization and analysis to make better strategic decisions."
        },
        {
            "name": "Julio Dzul",
            "role": "Data Engineer",
            "description": "Hi, I’m Julio Dzul, a 22-year-old data engineering enthusiast. For this project, I modeled and integrated the DynamoDB database with the dashboard functions. It was a great experience that boosted my skills and supported efficient data analysis, combining my love for technology and problem-solving."
        }
    ]

    # Mostrar la información
    for member in team_members:
        st.markdown(f"""
            <div class="profile-card">
                <div class="profile-header">{member['name']}</div>
                <div class="profile-subtitle">{member['role']}</div>
                <p>{member['description']}</p>
            </div>
            <div class="separator"></div>
        """, unsafe_allow_html=True)

else:
    st.warning("Please log in to view the 'About Us' page.")

