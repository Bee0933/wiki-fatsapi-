FROM python:3.8-slim-buster

RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt && pip install --upgrade pip
EXPOSE 8001
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8001"]
