FROM python:3.9.10-slim-buster
RUN apt install chromium-chromedriver -y
RUN apt install tesseract-ocr -y
WORKDIR /app
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
ENV PYTHONPATH=/app
COPY . .