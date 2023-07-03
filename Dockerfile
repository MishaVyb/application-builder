FROM python:3.11-slim

LABEL author='misha.vybornyy@gmail.com'

WORKDIR /code

COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
