FROM python:2.7

RUN mkdir /app
WORKDIR /app

COPY ./app /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]