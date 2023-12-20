import pandas as pd


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

    # Formato de fechas
    df['Periodo'] = df['Periodo'].astype(str)
    df['Periodo'] = df['Periodo'].str[:-2] + df['Periodo'].str[-1:]
    df['Periodo'] = pd.to_datetime(
        df['Periodo'], format='%Y%m').dt.strftime('%b %Y')


CONTEXT = """
You are a chatbot that answers questions about the financial system of Arauco.
To do this, I provide you with two databases: product volume (df1) and product sales (df2).
I will now ask you a question about these databases. I want you to include the Pandas query
you use in your response to find the requested information.

If you don't find the answer in one dataframe, please search in the other.

By the way, You should use the tools below to answer the question posed of you:

Summary of the whole conversation:
{chat_history_summary}

Last few messages between you and user:
{chat_history_buffer}

Entities that the conversation is about:
{chat_history_KG}

The question is as follows:\n
"""

FORMAT_INSTRUCTIONS = """\nUse the following format:
Question: the input question you must answer
Thought: consider the appropriate course of action or query to retrieve the information
Action: python_repl_ast
Action Input: input for the action, without backticks "`" around it
Observation: the result of the action
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: conclude the process with the final answer
Final Answer: provide the ultimate answer to the original question. Respond in Spanish.
"""
