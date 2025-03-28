from fastapi import FastAPI
import requests
from llm import call_llm

PROMPT = '''
Você possui acesso à informações retiradas do site oficial da empresa, esse conteúdo está delimitado pelas tags <infos> </infos>. Seu conhecimento é limitado a essas informações e elas devem ser utilizadas para responder as questões do usuário.
Sua tarefa é utilizar as informações dos documentos para responder a pergunta do usuário da forma mais direta e técnica possível, com base unicamente nas informações fornecidas.
Dessa forma, você pode utilizar as informações referentes ao documento que mais ajuda a responder à pergunta do usuário, dentro do tema que ele está perguntando.
Quanto mais assertiva e embasada nos documentos for a resposta, melhor será a satisfação do usuário. Por isso, apenas responda a requisição do usuário e não invente nem crie informações.
As informações que você pode se embasar para responder a dúvida do usuário são: 
<infos>
{context}
</infos>
Com base nas informações em <infos>, responda adequadamente ao usuário.

'''

app = FastAPI()

@app.get("/answer")
def answer_question(question: str):
    '''
    Queries the rag module and returns the answer to the question.
    '''

    # format the question with context
    vec_db_url = "http://vector_db:8001/query"
    vector_db_response = requests.get(vec_db_url, json={"query": question, "k": 10})
    retrieved_chunks = vector_db_response.json().get("results")
    chunk_list = retrieved_chunks['documents'][0]
    # transform the list into a string
    chunk_list = " ".join(chunk_list)
    print("Formating question ...")
    instructions = PROMPT.format(context=chunk_list)
    print("Instructions", instructions)
    # query the llm
    answer = call_llm(instructions, question)


    return {"question": question, "answer": answer}
