from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory, ConversationKGMemory, CombinedMemory
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent as pd_agent
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from utils import convert_dtypes, CONTEXT, FORMAT_INSTRUCTIONS
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

# Localidad para el formato de fechas
locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

# OpenAI Api Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Leer datos
vp = qvd_reader.read('data/Volumen_Prod.qvd')
pv = qvd_reader.read('data/Precio_venta.qvd')
convert_dtypes(vp)
convert_dtypes(pv)

# Crear agente
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
chat = ChatOpenAI(
    model_name='gpt-3.5-turbo-0613',
    temperature=0,
    openai_api_key=api_key,
)

# Lo comentado a continuación es una opción para guardar en memoria, pero es necesario
# cambiar el código fuente de la librería Langchain.

# chat_history_buffer = ConversationBufferWindowMemory(
#     k=5, memory_key="chat_history_buffer", input_key="input")
# chat_history_summary = ConversationSummaryMemory(
#     llm=llm, memory_key="chat_history_summary", input_key="input")
# chat_history_KG = ConversationKGMemory(
#     llm=llm, memory_key="chat_history_KG", input_key="input")
# memory = CombinedMemory(
#     memories=[chat_history_buffer, chat_history_summary, chat_history_KG])

agent = pd_agent(chat, [vp, pv], verbose=True,
                 # agent_executor_kwargs={"memory": memory},
                 # input_variables=['df_head', 'input', 'agent_scratchpad', 'chat_history_buffer', 'chat_history_summary', 'chat_history_KG']
                 )

# Ejecutar agente para una consulta


def consulta(input_usuario):
    tiempo_inicial = time.time()
    output = agent.run(CONTEXT +
                       input_usuario + FORMAT_INSTRUCTIONS)
    tiempo_final = time.time()
    print(f"Tiempo de ejecución: {tiempo_final - tiempo_inicial}")
    return (output)
