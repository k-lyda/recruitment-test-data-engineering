FROM python:3.9

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ingest_data.py ./
ENTRYPOINT ./ingest_data.py
