from flask import Flask, jsonify, request
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent as pd_agent
from langchain.chat_models import ChatOpenAI
from utils import convert_dtypes, CONTEXT, FORMAT_INSTRUCTIONS
from qvd import qvd_reader
import locale
import openai
from dotenv import load_dotenv
import os
import datetime
import logging

# Localidad
#locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

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

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Define /
@app.route('/', methods=['GET'])
def index():
    return 'Hello World!'

# Define the /api/messages endpoint
@app.route('/api/messages', methods=['POST'])
def messages():
    if request.method == 'POST':
        # Get the user input from the request body
        request_body = request.get_json()
        if request_body is None:
            app.logger.error('Request body is empty or not in JSON format')
            return jsonify({'error': 'Request body is empty or not in JSON format'})
        
        app.logger.debug(f"Request body: {request_body}")
        
        if request_body['type'] != 'message':
            app.logger.error('Request body type is not message')
            return jsonify({'error': 'Request body type is not message'})
        
        user_input = request_body['text']
        app.logger.info(f"User input: {user_input}")
        
        # Run the agent with the user input
        output = agent.run(CONTEXT + user_input + FORMAT_INSTRUCTIONS)
        app.logger.info(f"Agent output: {output}")
        
        response = {
            "type": "message",
            "text": output,
            "from": {
                "id": request_body["from"]["id"],
                "name": request_body["from"]["name"]
            },
            "recipient": {
                "id": request_body["recipient"]["id"],
                "name": request_body["recipient"]["name"]
            },
            "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "conversation": {
                "id": request_body["conversation"]["id"]
            }
        }

        app.logger.info(f"Response: {response}")
        return jsonify(response)
    

# Run the app on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0')