import os
import openai
from prompt import Prompt
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_sql(prompt: Prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt.get_prompt(),
        temperature=0.7,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["#", ";"]
    )
    return "SELECT" + response.choices[0]["text"]


