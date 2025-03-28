from fastapi import FastAPI
import requests
from utils import get_content_body, split_text
import logging

app = FastAPI()
VECTOR_DB_ENDPOINT = "http://vector_db:8001/add"

logging.basicConfig(level=logging.INFO)

@app.get("/scrape")
def scrape_webpage(url: str):
    """
    Scrapes the content of a webpage, processes it into smaller chunks, and stores the chunks in a vector database.
    Args:
        url (str): The URL of the webpage to scrape.
    Returns:
        dict: A dictionary containing the full processed content of the webpage under the key "content".
    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request.
        Exception: If there is an error during the storage of text chunks in the vector database.
    Notes:
        - The function fetches the webpage content using an HTTP GET request.
        - The content is extracted and split into smaller chunks for further processing.
        - Each chunk is stored in a vector database via an HTTP POST request.
        - Errors during the HTTP requests are logged to the console.
    """
    response = requests.get(url)
    if response.status_code == 200:
        page_content = response.text
    else:
        print(f"Error processing page: {response.status_code}")

    page_content = get_content_body(page_content)
    content_chunks = split_text(page_content)
    # store in vector db
    for text_chunk in content_chunks:
        data = {"text_chunk": text_chunk.page_content}
        response = requests.post(VECTOR_DB_ENDPOINT, json=data)
        if response.status_code != 200:
            logging.error(f"Error storing text chunk: {response.status_code}")

    return {"content": page_content}
