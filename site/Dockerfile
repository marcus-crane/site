FROM python:3.6-alpine

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt
COPY . /code/

CMD ["python", "app.py"]
