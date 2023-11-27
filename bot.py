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
df = qvd_reader.read('Volumen_Prod.qvd')
# df['Periodo'] = df['Periodo'].astype(
#     str).str[0:4] + df['Periodo'].astype(str).str[5:7]
# df['Periodo'] = pd.to_datetime(df['Periodo'], format='%Y%m')
# df['Periodo'] = df['Periodo'].dt.strftime('%B %Y').str.capitalize()
convert_dtypes(df)


# Convertimos los tipos de datos
convert_dtypes(df)

agent = pd_agent(OpenAI(temperature=0), df, verbose=True)


def consulta(input_usuario):
    """
    Función para realizar consultas a la base de datos
    """
    tiempo_inicial = time.time()
    output = agent.run(input_usuario)
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
