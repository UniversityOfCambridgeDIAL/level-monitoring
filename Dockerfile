FROM arm32v7/python:3.7-buster

COPY ./requirements.txt ./app/requirements.txt
COPY ./userInterface ./app/userInterface

WORKDIR /app

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1
#CMD ["python3","./userInterface/app.py"]
ENTRYPOINT python3 ./userInterface/app.py
