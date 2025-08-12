FROM python:3.13-slim

EXPOSE 9191

ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "./server_online.py"] 