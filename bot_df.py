from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
# pip install "openai<1.0.0"
import openai
from langchain.llms import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv
from qvd import qvd_reader


# OpenAI Api Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Cargamos el QVD
df = qvd_reader.read('Precio_venta.qvd')

agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
    df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

# Formato de respuesta
model = """
Dada una pregunta del usuario:
1. Revisa los datos
2. Revisa los resultados
3. Devuelve la información solicitada
4. Todas tus respuestas deben ser en español
# {request}
"""


def consulta(input_usuario):
    """
    Función para realizar consultas a la base de datos
    """
    query = model.format(request=input_usuario)
    output = agent.run(query)
    return (output)


while True:
    user_input = input("\nIngrese su consulta:\n")
    if user_input.lower() == 'salir':
        break
    else:
        result = consulta(user_input)
        print('')
        print(result)
