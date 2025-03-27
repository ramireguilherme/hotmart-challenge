FROM python:3.9-slim
RUN pip install -r requirements.txt
EXPOSE 8501
COPY . /app
WORKDIR /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8501"]