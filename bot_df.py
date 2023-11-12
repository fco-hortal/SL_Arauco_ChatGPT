from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent as pd_agent
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from qvd import qvd_reader
# pip install "openai<1.0.0"
import openai
from dotenv import load_dotenv
import os
import time


# OpenAI Api Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Cargamos el QVD
df = qvd_reader.read('Precio_venta.qvd')

agent = pd_agent(
    ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
    df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

# Formato de respuesta
model = """
Dada una pregunta del usuario sobre el DataFrame proporcionado:
1. Revisa el DataFrame de Pandas según lo preguntado.
2. Analiza los resultados de lo encontrado.
3. Proporciona los resultados esperados por el usuario.
4. Todas tus respuestas deben ser en español.
# {request}
"""


def consulta(input_usuario):
    """
    Función para realizar consultas a la base de datos
    """
    tiempo_inicial = time.time()
    query = model.format(request=input_usuario)
    output = agent.run(query)
    tiempo_final = time.time()
    print(f"Tiempo de ejecución: {tiempo_final - tiempo_inicial}")
    return (output)


while True:
    user_input = input("\nIngrese su consulta:\n")
    if user_input.lower() == 'salir':
        break
    else:
        result = consulta(user_input)
        print('')
        print(result)
