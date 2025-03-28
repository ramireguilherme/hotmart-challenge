from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def call_llm(instructions: str, prompt : str):
    print("Calling LLM ...")
    response = client.responses.create(
    model="gpt-4o",
    instructions=instructions,
    input=prompt,
    )
    response_text = response.output[0].content[0].text 
    return response_text
