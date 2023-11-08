from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
# pip install "openai<1.0.0"
import openai
import os
from dotenv import load_dotenv

# OpenAI Api Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Creamos LLM
llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')

# Langchain y base de datos
db = SQLDatabase.from_uri("sqlite:///ecommerce.db")
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# Formato de respuesta
model = """
Dada una pregunta del usuario:
1. Crea una consulta de sqlite3
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
    output = db_chain.run(query)
    return (output)


while True:
    user_input = input("\nIngrese su consulta:\n")
    if user_input.lower() == 'salir':
        break
    else:
        result = consulta(user_input)
        print('')
        print(result)
