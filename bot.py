from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent as pd_agent
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from qvd import qvd_reader
import pandas as pd
from datetime import datetime
import locale
# pip install "openai<1.0.0"
import openai
from dotenv import load_dotenv
import os
import time

# Localidad
locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

# OpenAI Api Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


def convert_dtypes(df):
    """
    Conversión numérica
    """
    cols = df.columns
    for c in cols:
        try:
            df[c] = pd.to_numeric(df[c])
        except:
            pass


# Import the QVD file
vp = qvd_reader.read('data/Volumen_Prod.qvd')
pv = qvd_reader.read('data/Precio_venta.qvd')
convert_dtypes(vp)
convert_dtypes(pv)

# Create agent
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
chat = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    temperature=0,
    openai_api_key=api_key,
)
agent = pd_agent(chat, [vp, pv], verbose=True)


def consulta(input_usuario):
    tiempo_inicial = time.time()
    context = """
    Eres un chatbot que responde preguntas sobre el sistema financiero de Arauco.
    Para ello te entrego dos bases de datos: volúmen de productos y ventas de productos.
    A continuación te haré una pregunta sobre estas bases de datos. Quiero que a tu
    respuesta le añadas la consulta que haces a Pandas para encontrar la información solicitada.

    Si no encuentras la respuesta en un df, busca en el otro.

    La pregunta es la siguiente:\n
    """
    output = agent.run(context + input_usuario)
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
