import openai
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()
# Configura tu clave de API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY") 

# Example OpenAI Python library request
MODEL = "gpt-3.5-turbo"
response = openai.completions.create(
    model=MODEL,
    prompt=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Knock knock."},
        {"role": "assistant", "content": "Who's there?"},
        {"role": "user", "content": "Orange."},
    ],
    temperature=0,
)

response
