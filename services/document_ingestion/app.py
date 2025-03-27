from fastapi import FastAPI
import requests
from utils import get_content_body, split_text

app = FastAPI()

# To do: add logging
# 
@app.get("/scrape")
def scrape_webpage(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        page_content = response.text
    else:
        print(f"Error processing page: {response.status_code}")

    page_content = get_content_body(page_content)
    content_chunks = split_text(page_content)
    # store in vector db
    

    return {"content": page_content}


@app.get("/question")
def answer_question(question: str):
    '''
    Queries the rag module and returns the answer to the question.
    '''
    return {"question": question, "answer": "answer"}