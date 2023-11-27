from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent as pd_agent
from langchain.llms import OpenAI
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from qvd import qvd_reader
import pandas as pd
import openai
from dotenv import load_dotenv
import os
import time

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
pv = qvd_reader.read('data/Precio_venta.qvd')
vp = qvd_reader.read('data/Volumen_Prod.qvd')
convert_dtypes(pv)
convert_dtypes(vp)

agent = pd_agent(
    OpenAI(temperature=0),
    [pv, vp],
    verbose=True
)


def consulta(input_usuario):
    """
    Función para realizar consultas a la base de datos
    """
    output = agent.run(input_usuario)
    return (output)