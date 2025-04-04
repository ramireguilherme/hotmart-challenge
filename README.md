# Hotmart ML Engineer Challenge

## Arquitetura

O sistema é composto por três serviços:

document_ingestion: Um microsserviço que recebe o link da página da Hotmart, processa o conteúdo do blog post, quebra o texto em trechos menores utilizando os splitter nativos do langchain e os armazena em um banco de vetores.

vector_db: Utiliza o chromadb para armazenar e recuperar embeddings.

llm: recebe perguntas, realiza a consulta no vector_db para recuperar os trechos de texto mais relevantes para a pergunta e responder de maneira adequada.

## Tecnologias Utilizadas

Linguagem: Python

Frameworks: FastAPI por ser facilmente integrável com os modelos de ML e vector databases.

Banco de Vetores: ChromaDB (optei por utilizar esta ferramenta por ser open source e ter fácil implementação, além de já ter utilizado em projetos anteriormente)

Modelos de ML: LangChain + OpenAI API (A princípios estava utilizando modelos da huggingface, contudo o desempenho em minha máquina estava sendo um gargalo na aplicação).
Para armazenar os embeddings no vector_db o ChromaDB utiliza o MiniLM por padrão, que é um modelo leve e que exige poucos recursos computacionais, contudo o desempenho deste modelo em queries na língua portuguesa estava sendo inferior ao Ada (modelo nativo da openAI) então optei por trocá-lo também.

Containerização: Docker + Docker Compose seguindo os requisitos do desafio.

## Instruções de build
Crie uma key para a APi da openAI, em seguida crie um arquivo .env na pasta base do projeto com o seguinte conteúdo:
```
OPENAI_API_KEY=<sua chave da OpenAi aqui>
```

Para testar basta abrir o terminal e buildar a aplicação com 
```
docker compose build
```
Depois, rode a aplicação com:
```
docker compose up
```

## Testar a API
Para testar a ingestão de dados da página, use o seguinte comeando do cURL
```
curl -X GET "http://127.0.0.1:8000/scrape?url=https://hotmart.com/pt-br/blog/como-funciona-hotmart"
```
Após a ingestão, você pode fazer uma pergunta para a base de conhecimento de maneira similar, por exemplo: 
```
curl -G "http://localhost:8002/answer" -H "Content-Type: application/json" --data-urlencode "question=quais são os tipos de produtos digitais?"
```

```
curl -G "http://localhost:8002/answer" -H "Content-Type: application/json" --data-urlencode "question=Quem fundou a Hotmart"
```