import openai
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()
# Configura tu clave de API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()

completation = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Hey. How are you?",
    max_tokens=7,
    temperature=0
)

answer = completation.choices[0].text
print(answer)
