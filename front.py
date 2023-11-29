import bot_front
import streamlit as st
from streamlit_chat import message
from datetime import datetime

# Título y descripción de la aplicación
st.title("App prueba Arauco Chat")
st.write("¡Sin Límites!")

# Inicializar la lista de conversación si no existe en el estado de la sesión
if 'conversacion' not in st.session_state:
    st.session_state.conversacion = []

# Función para manejar el clic en el botón de enviar
def click():
    if st.session_state.user != '':
        # Obtener la pregunta del usuario y obtener la respuesta del bot
        pregunta = st.session_state.user
        respuesta = bot_front.consulta(pregunta)

        # Añadir pregunta y respuesta a la conversación con marca de tiempo
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.conversacion.append(("Usuario", pregunta, now))
        st.session_state.conversacion.append(("Bot", respuesta, now))

        # Limpiar el input de usuario después de enviar la pregunta
        st.session_state.user = ''

# Formulario para la entrada de usuario
with st.form('my-form'):
    query = st.text_input('¿En qué te puedo ayudar?:', key='user', help='Pulsa Enviar para hacer la pregunta')
    submit_button = st.form_submit_button('Enviar', on_click=click)

# Mostrar la conversación
if st.session_state.conversacion:
    for i, (autor, mensaje, timestamp) in enumerate(st.session_state.conversacion):
        st.markdown("---")  # Separador
        if autor == "Usuario":
            st.text_area(f"{autor} ({timestamp}):", mensaje, key=f"{i}_user")
        else:
            message(f"{autor} ({timestamp}): {mensaje}", key=f"{i}_bot")

    st.markdown("---")  # Separador
    # Opción para continuar la conversación o borrar historial
    continuar_conversacion = st.checkbox('¿Borrar historial?')
    if not continuar_conversacion:
        st.session_state.conversacion = []
