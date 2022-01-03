# pull official base image
FROM python:3.9

WORKDIR /backend
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE = 1
ENV PYTHONUNBUFFERED = 1

ENV DIALOGFLOW_PROJECT_ID=jarvis-sqri
ENV GOOGLE_APPLICATION_CREDENTIALS=jarvis-sqri-db7648fb066e.json

COPY . .

CMD ["gunicorn", "-b","0.0.0.0:5000", "-w 1","application:app"]