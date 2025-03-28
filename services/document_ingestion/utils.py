from langchain_text_splitters import MarkdownHeaderTextSplitter, HTMLHeaderTextSplitter, CharacterTextSplitter
from bs4 import BeautifulSoup
from typing import List
# to do: change chunking strategy
def split_text(text: str) -> List[str]:
    """
    Splits a text into chunks of a given size.

    Args:
        text: The text to be split.
        chunk_size: The size of each chunk.

    Returns:
        A list of text chunks.
    """
    text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
    )
    chunks = text_splitter.create_documents([text])
    return chunks

def get_content_body(html_text: str) -> str:
    '''
    Receives a pure html text and return the content body with the relevant text.
    '''
    soup = BeautifulSoup(html_text, "html.parser")
    content = soup.find(class_="content__body")
    return content.get_text()
