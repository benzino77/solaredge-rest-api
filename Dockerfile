FROM python:3-alpine

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", ":8080", "--workers" ,"1", "--threads", "8", "--timeout", "0", "server:app" ]