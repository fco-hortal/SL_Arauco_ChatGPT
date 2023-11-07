# SL Arauco ChatGPT

Chatbot inteligente personalizado para el área de finanzas de la empresa Arauco.

---

## Librerías Necesarias

Para el funcionamiento del código, es necesario instalar las siguientes librerías en el sistema.

```bash
# OpenAI para conectar con ChatGPT
# Versión anterior por compatibilidad con Langchain
pip install "openai<1.0.0"
```

```bash
# LangChain para conectar con DB
pip install langchain
```

```bash
# LangChain para conectar con DB
pip install langchain-experimental
```

## Acceso y Uso de API

Para poder funcionar, el chatbot se conecta a la API de OpenAI. Por este motivo es necesario ofrecer mediante una variable de entorno una API KEY.

```py
# Archivo .env
OPENAI_API_KEY =
```
