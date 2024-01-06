FROM python:3.10-slim

WORKDIR /app

COPY ./app /app
COPY ./requirements.txt /app

RUN pip install -r requirements.txt

EXPOSE 8501

ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV OPENAI_MODEL=${OPENAI_MODEL}
ENV POOL_ID=${POOL_ID}
ENV APP_CLIENT_ID=${APP_CLIENT_ID}
ENV APP_CLIENT_SECRET=${APP_CLIENT_SECRET}

ENTRYPOINT ["streamlit", "run", "/app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]