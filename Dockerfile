FROM python:3.10-slim

WORKDIR /app

COPY ./app /app
COPY ./requirements.txt /app

RUN pip install -r requirements.txt

EXPOSE 8501

ENV API_KEY=${API_KEY}
ENV AI_MODEL=${AI_MODEL}

ENTRYPOINT ["streamlit", "run", "/app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]