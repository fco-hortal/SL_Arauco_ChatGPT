from flask import Flask, jsonify, request
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent as pd_agent
from langchain.chat_models import ChatOpenAI
from utils import convert_dtypes, CONTEXT, FORMAT_INSTRUCTIONS
from qvd import qvd_reader
import locale
import openai
from dotenv import load_dotenv
import os

# Localidad
locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

# OpenAI Api Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Import the QVD file
vp = qvd_reader.read('data/Volumen_Prod.qvd')
pv = qvd_reader.read('data/Precio_venta.qvd')
convert_dtypes(vp)
convert_dtypes(pv)

# Create agent
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
chat = ChatOpenAI(
    model_name='gpt-3.5-turbo-0613',
    temperature=0,
    openai_api_key=api_key,
)

agent = pd_agent(chat, [vp, pv], verbose=True)

# Create Flask app
app = Flask(__name__)

# Define /
@app.route('/', methods=['GET'])
def index():
    return 'Hello World!'

# Define the /api/messages endpoint
@app.route('/api/messages', methods=['POST'])
def messages():
    if request.method == 'POST':
        # Get the user input from the request body
        user_input = request.get_json().get('input')
        # Run the agent with the user input
        output = agent.run(CONTEXT + user_input + FORMAT_INSTRUCTIONS)
        # Return the output as JSON
        return jsonify(output)

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0')
