FROM python:3.10-slim

# Libs essenciais
RUN apt-get update && apt-get install -y \
    git wget libgl1 libglib2.0-0 \
    && apt-get clean

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
